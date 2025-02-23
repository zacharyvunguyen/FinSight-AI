from setuptools import setup, find_packages

setup(
    name="finsight-ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.109.2",
        "uvicorn[standard]==0.27.1",
        "pydantic-settings==2.1.0"
    ]
)