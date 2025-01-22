import requests
import re
from markdownify import markdownify

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"
}


def get(url: str) -> str:
    response = requests.get(url, headers=REQUEST_HEADERS)
    return response.text


def extract_body(html: str) -> str | None:
    match = re.search(r"<body[^>]*>([\s\S]*?)<\/body>", html, flags=re.IGNORECASE)
    return match.group(1) if match is not None else None


def exclude_unwanted(html: str) -> str:
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


def fix_links(source: str, html: str) -> str | None:
    match = re.match(r"^(https?:\/\/[^/]+)", source)
    if match is None:
        return None
    base_url = match.group(1)

    return re.sub(
        r'href="\/(.*?)"',
        lambda match: f'href="{base_url}/{match.group(1)}"',
        html,
    )


def to_markdown(html: str) -> str:
    return markdownify(html)
