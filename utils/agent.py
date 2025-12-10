import yaml
from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from pydantic import BaseModel, Field, SecretStr

from utils.news_parser import NewsArticle
from conf.secrets import OPENAI_API_KEY, OPENAI_COMPATIBLE_ENDPOINT

with open("./conf/agents.yml", "r") as agents_conf:
    config = yaml.safe_load(agents_conf)


class PriorityRating(BaseModel):
    """
    Represents the priority rating for a news article.
    """

    priority: int = Field(description="The priority rating (0, 1, or 2)")


def evaluate(articles: list[NewsArticle]):
    """
    Evaluates a list of news articles and assigns a priority rating to each article.

    The function uses a LLM to evaluate the priority of each article based on its content.
    Priority ratings are assigned to the articles in-place.

    :param articles: A list of NewsArticle objects to evaluate.
    :return: None
    """
    model = ChatOpenAI(
        model=config["news_evaluator"]["model"],
        api_key=SecretStr(OPENAI_API_KEY),
        base_url=OPENAI_COMPATIBLE_ENDPOINT,
    ).with_structured_output(PriorityRating)
    system_message = SystemMessage(content=config["news_evaluator"]["task"])
    human_messages = [
        HumanMessage(content=article.model_dump_json()) for article in articles
    ]
    responses = model.batch([[system_message, msg] for msg in human_messages])
    ratings = [
        response.priority
        for response in responses
        if isinstance(response, PriorityRating)
    ]
    assert len(ratings) == len(articles)
    for article, rating in zip(articles, ratings):
        article.priority = rating
