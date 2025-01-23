import json
import html
import re
import feedparser
from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field, HttpUrl, BeforeValidator
from typing import Any, Annotated

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
}


class ParserException(Exception):
    """
    Custom exception for errors encountered during parsing.
    """

    pass


class NewsFeed(BaseModel):
    """
    Represents a news feed source.
    """

    name: str = Field(description="The name of the news agency")
    url: HttpUrl = Field(description="The URL of the news feed")


def parse_struct_date(value: list[int]) -> datetime:
    """
    Parses a date represented as a list of integers.

    :param value: A list containing date and time components.
    :return: A datetime object with timezone information.
    """
    return datetime(*value[:6], tzinfo=timezone.utc)


class NewsArticle(BaseModel):
    """
    Represents a news article.
    """

    title: str = Field(description="The title of the news article")
    date: Annotated[datetime, BeforeValidator(parse_struct_date)] = Field(
        description="The date of the news article"
    )
    url: HttpUrl = Field(description="The URL of the news article")
    source: str = Field(
        description="The source of the news article (e.g., New York Times)"
    )
    summary: str = Field(description="The summary of the news article")
    priority: int = Field(
        description="The priority of the news article, between 0 and 2"
    )


def parse_feed(news_feed: NewsFeed) -> list[NewsArticle]:
    """
    Parses a single news feed and extracts articles.

    :param news_feed: The news feed to parse.
    :return: A list of parsed news articles.
    :raises ParserException: If an error occurs while parsing the feed.
    """
    feed = feedparser.parse(str(news_feed.url), request_headers=REQUEST_HEADERS)
    articles = []
    entries: list[dict[str, Any]] = feed.entries
    for article in entries:
        try:
            articles.append(
                NewsArticle(
                    title=article["title"],
                    date=article["published_parsed"],
                    url=article["link"],
                    source=news_feed.name,
                    # Strip HTML tags and unescape HTML entities from the summary
                    summary=re.sub(r"<[^>]*>", "", html.unescape(article["summary"])),
                    priority=0,
                )
            )
        except Exception as e:
            raise ParserException(f"Error parsing feed: {e}")
    return articles


def parse_feeds() -> list[NewsArticle]:
    """
    Parses all news feeds defined in the configuration file.

    :return: A list of all parsed news articles.
    :raises FileNotFoundError: If the configuration file is missing.
    :raises ParserException: If an error occurs while parsing any feed.
    """
    with open("./conf/sources.json", "r") as sources_conf:
        sources = json.load(sources_conf)

    sources = [NewsFeed(**source) for source in sources]
    articles = []
    for source in sources:
        articles.extend(parse_feed(source))
    return articles


def remove_old_news(articles: list[NewsArticle]) -> list[NewsArticle]:
    """
    Removes articles older than 24 hours.

    :param articles: The list of news articles to filter.
    :return: A list of news articles published in the last 24 hours.
    """
    now = datetime.now(timezone.utc)
    return [article for article in articles if article.date > now - timedelta(hours=24)]


def remove_empty_news(articles: list[NewsArticle]) -> list[NewsArticle]:
    """
    Removes articles that have empty summaries.

    :param articles: The list of news articles to filter.
    :return: A list of news articles with non-empty summaries.
    """
    return [article for article in articles if article.summary != ""]
