from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in allocate_batch/__init__.py
from allocate_batch import __version__ as version

setup(
	name="allocate_batch",
	version=version,
	description="aloocates batches for items with transactions already",
	author="gatura",
	author_email="gaturanjenga@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
