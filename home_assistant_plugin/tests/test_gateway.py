"""Tests for home_assistant_plugin.gateway.Gateway.

Covers:
- writer(): skip when not connected (the regression we fixed), send
  Command/Notifier messages, skip unknown message types, id increment
- associate_triggers(): registers entity_id and setup trigger objects
- associate_commands(): documented no-op
- run(): auth handshake, trigger dispatch, connection-failure retry
- disconnect(): closes session; safe when session is None
"""

import asyncio
import json
import unittest
from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp

from home_assistant_plugin.gateway import Gateway
from home_assistant_plugin.message import Command
from home_assistant_plugin.service.notify.command import Command as Notifier

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_text_msg(payload: dict) -> MagicMock:
    """Return a mock websocket message with TEXT type."""
    msg = MagicMock()
    msg.type = aiohttp.WSMsgType.TEXT
    msg.data = json.dumps(payload)
    return msg


def _make_error_msg() -> MagicMock:
    msg = MagicMock()
    msg.type = aiohttp.WSMsgType.ERROR
    return msg


class _MockWebSocket:
    """Async-iterable mock websocket with a send_str recorder."""

    def __init__(self, messages):
        self._messages = messages
        self.sent: list[dict] = []

    def __aiter__(self):
        return self._gen()

    async def _gen(self):
        for m in self._messages:
            yield m

    async def send_str(self, data: str) -> None:
        self.sent.append(json.loads(data))

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass


def _patch_session(mock_ws: _MockWebSocket):
    """Return a patcher that injects *mock_ws* as the connected websocket."""

    class _CM:
        async def __aenter__(self_inner):
            return mock_ws

        async def __aexit__(self_inner, *args):
            pass

    mock_session = MagicMock()
    mock_session.ws_connect.return_value = _CM()

    class _SessionCM:
        async def __aenter__(self_inner):
            return mock_session

        async def __aexit__(self_inner, *args):
            pass

    return patch(
        "home_assistant_plugin.gateway.aiohttp.ClientSession",
        return_value=_SessionCM(),
    )


# ---------------------------------------------------------------------------
# writer()
# ---------------------------------------------------------------------------


class TestGatewayWriter(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.gw = Gateway("test_token", "localhost", 8123)

    async def test_writer_returns_immediately_when_not_connected(self):
        """Regression: writer must NOT spin forever when websocket is None.

        Before the fix writer() did `while not self._websocket:
        await asyncio.sleep(0.1)` which blocked indefinitely and
        prevented all subsequent protocol writers from running.
        """
        self.assertIsNone(self.gw._websocket)
        cmd = MagicMock(spec=Command)
        cmd.message = {"type": "call_service"}
        # Must complete instantly — if it hangs the test times out.
        await self.gw.writer([cmd])

    async def test_writer_skips_non_command_messages(self):
        mock_ws = AsyncMock()
        self.gw._websocket = mock_ws
        await self.gw.writer([MagicMock()])  # not Command or Notifier
        mock_ws.send_str.assert_not_called()

    async def test_writer_sends_command_message(self):
        mock_ws = AsyncMock()
        mock_ws.closed = False
        self.gw._websocket = mock_ws
        cmd = MagicMock(spec=Command)
        cmd.message = {"type": "call_service", "domain": "light"}

        await self.gw.writer([cmd])

        mock_ws.send_str.assert_called_once()
        sent = json.loads(mock_ws.send_str.call_args[0][0])
        self.assertEqual(sent["type"], "call_service")
        self.assertIn("id", sent)

    async def test_writer_sends_notifier_message(self):
        mock_ws = AsyncMock()
        mock_ws.closed = False
        self.gw._websocket = mock_ws
        notif = MagicMock(spec=Notifier)
        notif.message = {"type": "call_service", "domain": "notify"}

        await self.gw.writer([notif])

        mock_ws.send_str.assert_called_once()

    async def test_writer_increments_id_per_message(self):
        mock_ws = AsyncMock()
        mock_ws.closed = False
        self.gw._websocket = mock_ws

        for _ in range(3):
            cmd = MagicMock(spec=Command)
            cmd.message = {"type": "call_service"}
            await self.gw.writer([cmd])

        self.assertEqual(self.gw._id, 8)  # starts at 5, +1 three times

    async def test_writer_skips_empty_message_list(self):
        mock_ws = AsyncMock()
        self.gw._websocket = mock_ws
        await self.gw.writer([])
        mock_ws.send_str.assert_not_called()

    async def test_writer_skips_when_websocket_is_closed(self):
        """Regression: writer must not attempt send_str on a closed websocket.

        When HA closes the connection gracefully, the aiohttp websocket object
        remains non-None but .closed becomes True.  Before the fix writer()
        would call send_str() and raise 'Cannot write to closing transport'.
        """
        mock_ws = MagicMock()
        mock_ws.closed = True
        self.gw._websocket = mock_ws
        cmd = MagicMock(spec=Command)
        cmd.message = {"type": "call_service"}
        await self.gw.writer([cmd])
        mock_ws.send_str.assert_not_called()


# ---------------------------------------------------------------------------
# associate_triggers() / associate_commands()
# ---------------------------------------------------------------------------


class TestGatewayAssociate(unittest.TestCase):

    def setUp(self):
        self.gw = Gateway("token", "localhost", 8123)

    def test_associate_triggers_registers_entity_ids(self):
        t1 = MagicMock()
        t1.entity_id = "sensor.temperature"
        t2 = MagicMock()
        t2.entity_id = "light.kitchen"

        self.gw.associate_triggers([t1, t2])

        self.assertIn(t1, self.gw._setup_triggers)
        self.assertIn(t2, self.gw._setup_triggers)
        self.assertIn("sensor.temperature", self.gw._triggers)
        self.assertIn("light.kitchen", self.gw._triggers)

    def test_associate_triggers_empty_list(self):
        self.gw.associate_triggers([])
        self.assertEqual(len(self.gw._setup_triggers), 0)
        self.assertEqual(len(self.gw._triggers), 0)

    def test_associate_commands_is_noop(self):
        self.gw.associate_commands([MagicMock(), MagicMock()])
        self.assertEqual(self.gw._commands, set())


# ---------------------------------------------------------------------------
# run() — auth handshake
# ---------------------------------------------------------------------------


class TestGatewayRunAuth(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.gw = Gateway("secret_token", "ha-host", 8123)

    async def _run_once(self, messages):
        """Run the gateway for a single websocket session then stop."""
        mock_ws = _MockWebSocket(messages)
        with _patch_session(mock_ws):
            with patch(
                "home_assistant_plugin.gateway.asyncio.sleep",
                side_effect=asyncio.CancelledError,
            ):
                try:
                    await self.gw.run([])
                except asyncio.CancelledError:
                    pass
        return mock_ws

    async def test_run_sends_auth_on_auth_required(self):
        mock_ws = await self._run_once(
            [_make_text_msg({"type": "auth_required"})]
        )
        self.assertEqual(len(mock_ws.sent), 1)
        self.assertEqual(mock_ws.sent[0]["type"], "auth")
        self.assertEqual(mock_ws.sent[0]["access_token"], "secret_token")

    async def test_run_subscribes_on_auth_ok(self):
        mock_ws = await self._run_once([_make_text_msg({"type": "auth_ok"})])
        types = [m["type"] for m in mock_ws.sent]
        self.assertIn("subscribe_events", types)
        self.assertIn("get_services", types)

    async def test_run_continues_on_successful_result(self):
        mock_ws = await self._run_once(
            [_make_text_msg({"type": "result", "success": True, "id": 1})]
        )
        self.assertEqual(len(mock_ws.sent), 0)

    async def test_run_logs_error_on_failed_result(self):
        with self.assertLogs(
            "home_assistant_plugin.gateway", level="ERROR"
        ) as cm:
            await self._run_once(
                [_make_text_msg({"type": "result", "success": False, "id": 1})]
            )
        self.assertTrue(
            any("result" in line or "received" in line for line in cm.output)
        )


# ---------------------------------------------------------------------------
# run() — trigger dispatch
# ---------------------------------------------------------------------------


class TestGatewayRunDispatch(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.gw = Gateway("token", "localhost", 8123)
        trigger_stub = MagicMock()
        trigger_stub.entity_id = "sensor.wind"
        self.gw.associate_triggers([trigger_stub])

    async def _run_with_event(self, event_data):
        dispatched = []

        async def task(trigger):
            dispatched.append(trigger)

        mock_ws = _MockWebSocket([_make_text_msg(event_data)])

        with patch(
            "home_assistant_plugin.factory.trigger.Factory.get_triggers_from"
        ) as mock_factory:
            stub_trigger = MagicMock()
            stub_trigger.entity_id = "sensor.wind"
            mock_factory.return_value = [stub_trigger]

            with _patch_session(mock_ws):
                with patch(
                    "home_assistant_plugin.gateway.asyncio.sleep",
                    side_effect=asyncio.CancelledError,
                ):
                    try:
                        await self.gw.run([task])
                    except asyncio.CancelledError:
                        pass

        await asyncio.sleep(0)  # let create_task callbacks run
        return dispatched

    async def test_run_dispatches_matching_trigger(self):
        event_payload = {
            "type": "event",
            "event": {
                "event_type": "state_changed",
                "data": {"entity_id": "sensor.wind"},
            },
        }
        dispatched = await self._run_with_event(event_payload)
        self.assertEqual(len(dispatched), 1)

    async def test_run_skips_non_matching_entity(self):
        with patch(
            "home_assistant_plugin.factory.trigger.Factory.get_triggers_from"
        ) as mock_factory:
            stub = MagicMock()
            stub.entity_id = "sensor.OTHER"  # not registered
            mock_factory.return_value = [stub]

            dispatched = []

            async def task(t):
                dispatched.append(t)

            msg_data = {"type": "event", "event": {}}
            mock_ws = _MockWebSocket([_make_text_msg(msg_data)])
            with _patch_session(mock_ws):
                with patch(
                    "home_assistant_plugin.gateway.asyncio.sleep",
                    side_effect=asyncio.CancelledError,
                ):
                    try:
                        await self.gw.run([task])
                    except asyncio.CancelledError:
                        pass

            self.assertEqual(dispatched, [])


# ---------------------------------------------------------------------------
# run() — connection-failure retry (the scenario that broke commands)
# ---------------------------------------------------------------------------


class TestGatewayRunReconnect(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.gw = Gateway("token", "localhost", 8123)

    async def test_run_resets_websocket_on_connection_failure(self):
        """When ws_connect raises, _websocket must be reset to None so
        writer() skips gracefully instead of blocking forever."""

        class _FailingCM:
            async def __aenter__(self):
                raise aiohttp.ClientConnectorError(
                    MagicMock(), OSError("connection refused")
                )

            async def __aexit__(self, *args):
                pass

        class _SessionCM:
            async def __aenter__(self_inner):
                s = MagicMock()
                s.ws_connect.return_value = _FailingCM()
                return s

            async def __aexit__(self_inner, *args):
                pass

        sleep_calls = []

        async def fake_sleep(seconds):
            sleep_calls.append(seconds)
            if len(sleep_calls) >= 1:
                raise asyncio.CancelledError

        with patch(
            "home_assistant_plugin.gateway.aiohttp.ClientSession",
            return_value=_SessionCM(),
        ):
            with patch(
                "home_assistant_plugin.gateway.asyncio.sleep",
                side_effect=fake_sleep,
            ):
                with self.assertLogs(
                    "home_assistant_plugin.gateway", level="WARNING"
                ) as cm:
                    try:
                        await self.gw.run([])
                    except asyncio.CancelledError:
                        pass

        self.assertIsNone(self.gw._websocket)
        self.assertTrue(any("retrying" in line for line in cm.output))
        self.assertEqual(sleep_calls[0], 60)

    async def test_run_resets_websocket_after_normal_close(self):
        """Regression: _websocket must be reset to None when HA closes the
        WebSocket gracefully (no exception).

        Before the fix the finally block was missing; _websocket kept pointing
        to the closed socket, so the next writer() call would raise
        'Cannot write to closing transport'.
        """
        mock_ws = _MockWebSocket([])  # empty message list — loop exits cleanly
        with _patch_session(mock_ws):
            with patch(
                "home_assistant_plugin.gateway.asyncio.sleep",
                side_effect=asyncio.CancelledError,
            ):
                try:
                    await self.gw.run([])
                except asyncio.CancelledError:
                    pass
        self.assertIsNone(self.gw._websocket)

    async def test_writer_does_not_block_after_connection_failure(self):
        """After a failed connection, writer() must return instantly (not hang)
        because _websocket is None — the root cause of the commands bug."""
        self.gw._websocket = None
        cmd = MagicMock(spec=Command)
        cmd.message = {"type": "call_service"}
        # If this hangs, the test will time out.
        await asyncio.wait_for(self.gw.writer([cmd]), timeout=1.0)


# ---------------------------------------------------------------------------
# disconnect()
# ---------------------------------------------------------------------------


class TestGatewayDisconnect(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.gw = Gateway("token", "localhost", 8123)

    async def test_disconnect_closes_session(self):
        mock_session = AsyncMock()
        self.gw._session = mock_session
        await self.gw.disconnect()
        mock_session.close.assert_called_once()

    async def test_disconnect_is_safe_when_no_session(self):
        self.assertIsNone(self.gw._session)
        await self.gw.disconnect()  # must not raise


if __name__ == "__main__":
    unittest.main()
