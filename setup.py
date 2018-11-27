from setuptools import setup, find_packages
import re


def getVersion():
    version = '0.0.0'
    with open('drvschema/__init__.py', 'r') as f:
        contents = f.read().strip()

    m = re.search(r"__version__ = '([\d\.]+)'", contents)
    if m:
        version = m.group(1)
    return version


setup(
    name="drvschema",
    version=getVersion(),
    author='Aaron Kitzmiller <aaron_kitzmiller@harvard.edu>',
    author_email='aaron_kitzmiller@harvard.edu',
    description='Convert a Cerberus schema into validation code for Django models, DRF serializers, and Vuelidate validations',
    license='LICENSE.txt',
    include_package_data=True,
    url='http://pypi.python.org/pypi/goalchemy/',
    packages=find_packages(),
    long_description='Convert a Cerberus schema into validation code for Django models, DRF serializers, and Vuelidate validations',
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
    ],
    install_requires=[
        'Cerberus==1.2',
    ],
)
