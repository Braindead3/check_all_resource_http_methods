import pytest
from test_project.main import parse_string_to_url, check_all_http_methods
import httpx



@pytest.mark.asyncio
@pytest.mark.parametrize(
    'url', ['https://google.com']
)
async def test_url_parser(url):
    assert url == await parse_string_to_url(url)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'url', ['not valid url']
)
async def test_url_parser_with_wrong_url(url):
    assert await parse_string_to_url(url) is None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'url', ['https://google.com']
)
async def test_check_method_function(client, url):
    res_dict = {'https://google.com': {'GET': 301, 'HEAD': 301}}
    assert await check_all_http_methods(client, url) == res_dict
