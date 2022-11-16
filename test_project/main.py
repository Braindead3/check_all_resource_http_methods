from urllib.parse import urlparse
import asyncio

import httpx

HTTP_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE', 'HEAD', 'OPTIONS']

test_strings = ['https://google.com', 'https://www.facebook.com', 'vlad', 'malosay21@gmail.com', 'tochno_ne_silka']


async def check_all_http_methods(client: httpx.AsyncClient(), url) -> dict:
    """
    Проверяет все http методы у ресурса.

    :param client: Httpx асинхронный клент
    :param url: Ссылка не ресурс
    :return: Возращает словарь с ссылкой и методами которые разрешены.
    """
    result_dict = {url: {}}
    for http_method in HTTP_METHODS:
        response = await client.request(http_method, url)
        if response.status_code != httpx.codes.METHOD_NOT_ALLOWED:
            result_dict[url][http_method] = response.status_code

    return result_dict


async def parse_string_to_url(string: str) -> str:
    """
    Проверяет строку на то ссылка ли она или нет.
    Если да, возвращает ссылку, если нет, то пишет в консоль, что это не ссылка.

    :param string:
    :return: Возвращает ссылку
    """
    parsed_string = urlparse(string)

    if parsed_string.scheme and parsed_string.netloc:
        return parsed_string.geturl()
    else:
        print(f'Строка {string} не является ссылкой.')


async def main() -> None:
    async with httpx.AsyncClient() as client:
        strings = input().split()
        tasks = []
        for string in strings:
            url = await parse_string_to_url(string)
            if url:
                tasks.append(asyncio.create_task(check_all_http_methods(client, url)))
        group_task = asyncio.gather(*tasks)
        try:
            result = await group_task
        except asyncio.CancelledError:
            print("Gather was cancelled")
        print(result)


if __name__ == '__main__':
    asyncio.run(main())
