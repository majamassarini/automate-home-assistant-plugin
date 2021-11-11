from setuptools import setup, find_packages

setup(name="home-assistant-plugin",
      version="0.9",
      description="A Home Assistant plugin for homino",
      long_description="",
      author="Maja Massarini",
      author_email="maja.massarini@gmail.com",
      license="All rights reserved",
      packages=find_packages(exclude=[]),
      include_package_data=True,
      install_requires=['home', 'aiohttp'],
)
