"""Smoke test: the environment has every core dependency installed."""

import importlib

import pytest

CORE_PACKAGES = ["pandas", "pyarrow", "duckdb", "requests", "yfinance", "dotenv"]


@pytest.mark.parametrize("name", CORE_PACKAGES)
def test_core_package_importable(name):
    importlib.import_module(name)


def test_src_importable():
    import src.data  # noqa: F401
