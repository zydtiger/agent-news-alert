import json
from loguru import logger
from utils import news_parser, agent, email_generator, send_email
from utils.news_parser import NewsFeed, ParserException
from utils.agent import config
from conf.secrets import RECEIVER_EMAIL

# Get articles from RSS feeds
logger.info("Getting articles from RSS feeds")
with open("./conf/sources.json", "r") as sources_conf:
    sources = json.load(sources_conf)

sources = [NewsFeed(**source) for source in sources]
articles = []
for source in sources:
    try:
        articles.extend(news_parser.parse_feed(source))
        logger.info(f"Parsed RSS endpoint: {source.name}, {source.url}")
    except ParserException as e:
        logger.warning(f"Error parsing RSS endpoint: {source.name}, {source.url}")

articles = news_parser.remove_old_news(articles)
articles = news_parser.remove_empty_news(articles)

# Rate articles using agent
logger.info(
    f"Rating articles using agent based on model: {config['news_evaluator']['model']}"
)
articles_rated = [article for article in articles]
agent.evaluate(articles_rated)
articles_rated.sort(key=lambda x: x.priority, reverse=True)

# Send email
logger.info("Generating email for articles")
email_body = email_generator.generate_email_body(articles_rated[:10])
send_email.send_email(email_body)
logger.success(f"Email sent to: {RECEIVER_EMAIL}")
