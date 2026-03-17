"""
Mini Uber Data Platform
A production-grade data platform for processing and analyzing ride-sharing trip data.
"""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="mini-uber-data-platform",
    version="1.0.0",
    author="Rohit Verma",
    author_email="rohitverma9407@gmail.com",
    description="A production-grade data platform for ride-sharing analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Rohit898989/mini-uber-data-platform",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "uber-etl=pipelines.etl_pipeline:main",
            "uber-test=test_connection:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)