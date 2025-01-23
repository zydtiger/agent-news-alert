from zoneinfo import ZoneInfo
from utils.news_parser import NewsArticle


def generate_email_body(news_articles: list[NewsArticle]) -> str:
    """
    Generates an HTML email body from a list of NewsArticle objects.

    :param news_articles: A list of NewsArticle objects containing news article data.
    :return: A string containing the HTML email body.
    """
    email_body = """
    <html>
    <head>
      <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        .news-item { margin-bottom: 20px; padding: 10px; border-bottom: 1px solid #ddd; }
        .news-title { font-size: 18px; font-weight: bold; color: #333; }
        .news-summary { margin: 10px 0; color: #555; }
        .news-meta { font-size: 12px; color: #888; }
        .news-source { color: #007bff; text-decoration: none; }
      </style>
    </head>
    <body>
      <h1>Latest News</h1>
    """

    for i, article in enumerate(news_articles):
        date = article.date.astimezone(ZoneInfo("America/New_York"))

        email_body += f"""
        <div class="news-item">
            <a href="{article.url}" class="news-title">{i+1}. {article.title}</a>
            <p class="news-summary">{article.summary}</p>
            <p class="news-meta">
                <span>Source: <a href="{article.url}" class="news-source">{article.source}</a></span><br/>
                <span>Date: {date.strftime('%b %d, %Y %H:%M')}</span>
            </p>
        </div>
        """

    email_body += """
    </body>
    </html>
    """
    return email_body
