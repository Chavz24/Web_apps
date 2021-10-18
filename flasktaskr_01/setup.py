try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    "Description": "project_name",
    "Author": "Chavez24",
    "url": "None yet",
    "Author e-Mail": "N/A",
    "Version": "0.1",
    "install _requieres": ["nose"],
    "packages": ["NAME"],
    "scripts": [],
    "name:": "project_name",
}

setup(**config)
