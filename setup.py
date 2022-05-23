from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in waba_integration/__init__.py
from waba_integration import __version__ as version

setup(
	name="waba_integration",
	version=version,
	description="Work with WhatsApp Bussiness Cloud API from your Frappe site",
	author="Hussain Nagaria",
	author_email="hussain@frappe.io",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)