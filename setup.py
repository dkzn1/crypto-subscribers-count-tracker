from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()


with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="crypto-subscribers-count-tracker",
    version="1.0",
    description="",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dkzn1/crypto-subscribers-count-tracker",
    author="dkzn1",
    author_email="dkzn1",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires=">=3.11",
)
