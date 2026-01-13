"""
Setup script for RCM Process Mining Demo
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rcm-process-mining",
    version="1.0.0",
    author="Your Organization",
    description="Interactive process mining visualization for healthcare revenue cycle management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Topic :: Scientific/Engineering :: Visualization",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[
        "dash>=2.18.1",
        "dash-cytoscape>=1.0.2",
        "plotly>=5.24.1",
        "databricks-sdk>=0.35.0",
        "databricks-sql-connector>=3.5.0",
        "pandas>=2.2.3",
        "numpy>=2.1.3",
    ],
)
