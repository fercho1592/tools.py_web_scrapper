from setuptools import setup, find_pakages

setup(name="web_scrapper", version="1.0.0", packages=find_pakages["src"],
      entry_points = {"console_scripts": ["src = src.main.py"]})
