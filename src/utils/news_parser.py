import requests
import re
from markdownify import markdownify

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


class ParserException(Exception):
    """Custom exception for errors encountered during parsing."""

    pass


def get(url: str) -> str:
    """
    Sends a GET request to the specified URL and retrieves the response content.

    :param url: The URL to send the GET request to.
    :return: The response content as a string.
    :raises requests.RequestException: If there is an issue with the HTTP request.
    """
    response = requests.get(url, headers=REQUEST_HEADERS)
    if not response.ok:
        raise requests.RequestException(
            f"Request failed with status code: {response.status_code}"
        )
    return response.text


def extract_body(html: str) -> str:
    """
    Extracts the content of the <body> tag from an HTML string.

    :param html: A string containing the HTML content.
    :return: The content inside the <body> tag as a string.
    :raises ParserException: If the <body> tag is not found in the HTML.
    """
    match = re.search(r"<body[^>]*>([\s\S]*?)<\/body>", html, flags=re.IGNORECASE)
    if match is None:
        raise ParserException("HTML body not found")
    return match.group(1)


def exclude_unwanted(html: str) -> str:
    """
    Removes unwanted elements such as <script>, <style>, <noscript>, comments,
    and other media tags from the provided HTML string.

    :param html: A string containing the HTML content.
    :return: The cleaned HTML string with unwanted elements removed.
    """
    return re.sub(
        r"<script[^>]*>([\s\S]*?)<\/script>|"
        r"<style[^>]*>([\s\S]*?)<\/style>|"
        r"<noscript[^>]*>([\s\S]*?)<\/noscript>|"
        r"<!--[\s\S]*?-->|"
        r"<iframe[^>]*>([\s\S]*?)<\/iframe>|"
        r"<object[^>]*>([\s\S]*?)<\/object>|"
        r"<embed[^>]*>([\s\S]*?)<\/embed>|"
        r"<video[^>]*>([\s\S]*?)<\/video>|"
        r"<audio[^>]*>([\s\S]*?)<\/audio>|"
        r"<svg[^>]*>([\s\S]*?)<\/svg>",
        "",
        html,
        flags=re.IGNORECASE,
    )


def fix_links(source: str, html: str) -> str:
    """
    Converts relative links in an HTML string to absolute links based on the source URL.

    :param source: The base URL of the HTML source.
    :param html: A string containing the HTML content with relative links.
    :return: The HTML string with relative links converted to absolute links.
    :raises ParserException: If the source URL cannot be parsed.
    """
    match = re.match(r"^(https?:\/\/[^/]+)", source)
    if match is None:
        raise ParserException(f"Source URL can not be parsed: {source}")
    base_url = match.group(1)

    return re.sub(
        r'href="\/(.*?)"',
        lambda match: f'href="{base_url}/{match.group(1)}"',
        html,
    )


def to_markdown(html: str) -> str:
    """
    Converts an HTML string to Markdown format.

    :param html: A string containing the HTML content.
    :return: A string containing the converted Markdown content.
    """
    return markdownify(html)
