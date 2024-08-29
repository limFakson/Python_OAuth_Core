from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

DESCRIPTION = """
A Python library for handling OAuth authentication, designed for use in third-party applications. 
This package simplifies the process of obtaining authorization from Google, 
exchanging authorization codes for access tokens, 
refreshing access tokens, and retrieving user information.
"""

setup(
    name="oauth-core-lib",
    version="1.0.0",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="limFakson",
    author_email="fakeyejoshua2005@gmail.com",
    url="https://github.com/limFakson/Python_OAuth_Core",
    packages=find_packages(),
    install_requires=[
        "python-dotenv>=1.0.1",
        "requests>=2.25.1",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
