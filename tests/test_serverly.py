import pytest
import serverly
import json


def test_get_server_address():
    valid = ("localhost", 8080)
    assert serverly.Server._get_server_address(
        ("localhost", 8080)) == valid
    assert serverly.Server._get_server_address("localhost,8080") == valid
    assert serverly.Server._get_server_address("localhost, 8080") == valid
    assert serverly.Server._get_server_address("localhost;8080") == valid
    assert serverly.Server._get_server_address("localhost; 8080") == valid


def test_get_server_address_2():
    valid = ("localhost", 8080)
    with pytest.raises(Exception):
        with pytest.warns(UserWarning, match="bostname and port are in the wrong order. Ideally, the addresses is a tuple[str, int]."):
            serverly.Server._get_server_address((8080, "local#ost"))


def test_sitemap():
    serverly.register_get(lambda data: ({"code": 200}, "hello world!"), "/")
    assert serverly._sitemap.get_content("GET", "/")[1] == "hello world!"
    assert serverly._sitemap.get_content(
        "GET", "/notavalidurlactuallyitisvalid")[1] == "404 - Page not found"
