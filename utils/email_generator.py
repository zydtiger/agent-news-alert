from pathlib import Path
from zoneinfo import ZoneInfo
from utils.news_parser import NewsArticle


def generate_email_body(news_articles: list[NewsArticle]) -> str:
    """
    Generates an HTML email body from a list of NewsArticle objects.

    :param news_articles: A list of NewsArticle objects containing news article data.
    :return: A string containing the HTML email body.
    """
    # Load the email template
    template_path = Path(__file__).resolve().parent.parent / "templates" / "email_template.html"
    with open(template_path, "r", encoding="utf-8") as f:
        email_template = f.read()

    news_items_html = ""
    for i, article in enumerate(news_articles):
        date = article.date.astimezone(ZoneInfo("America/New_York"))
        formatted_date = date.strftime('%b %d, %Y %H:%M')

        news_items_html += f"""
        <div class="news-item">
            <a href="{article.url}" class="news-title">{i+1}. {article.title}</a>
            <p class="news-summary">{article.summary}</p>
            <div class="news-meta">
                <span class="news-source">{article.source}</span>
                <span>{formatted_date}</span>
            </div>
        </div>
        """

    return email_template.replace("{{NEWS_ITEMS}}", news_items_html)
