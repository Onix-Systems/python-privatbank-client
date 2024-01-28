from setuptools import setup, find_namespace_packages


def readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()


setup(
    name="privatbank_api_client",
    version="1.1.3",
    author="ihor.sotnyk",
    author_email="ihor.sotnyk@onix-systems.com",
    description="This module is designed for quick interaction with the privatbank API.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://gitlab.onix.ua/onix-systems/python-internal-privat",
    packages=find_namespace_packages(where="privatbank_api_client"),
    package_dir={"": "privatbank_api_client"},
    package_data={
        "privat_config": ["*.py"],
        "async_privat": ["*.py"],
        "sync_privat": ["*.py"],
        "drf_privat": ["*.py"],
        "fastapi_privat": ["*.py"],
    },
    install_requires=["python-dotenv==1.0.0"],
    extras_require={
        "http": ["requests>=2.25.1"],
        "aio": ["aiohttp==3.9.1"],
        "drf": ["Django>=4,<5", "djangorestframework", "requests>=2.25.1"],
        "fastapi": ["fastapi[all]", "sqlalchemy", "psycopg2", "asyncpg"],
        "all": [
            "Django>=4,<5",
            "djangorestframework",
            "requests>=2.25.1",
            "fastapi[all]",
            "aiohttp==3.9.1",
            "sqlalchemy",
            "psycopg2",
            "asyncpg",
            "alembic",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="files speedfiles ",
    python_requires=">=3.6",
)
