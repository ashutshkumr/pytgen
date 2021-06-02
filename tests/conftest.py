import pytest


@pytest.fixture
def src_port():
    return "pytgen-vtx"


@pytest.fixture
def dst_port():
    return "pytgen-vrx"
