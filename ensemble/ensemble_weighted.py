# ensemble/ensemble_weighted.py

from models.bert_model import get_bert_score
from utils.openai_moderation import get_openai_moderation_score

def ensemble_weighted_average(bert_score: float, openai_score: float, weights=(0.5, 0.5)) -> float:
    return(openai_score)

def get_final_score(text: str) -> float:
    bert_score = get_bert_score(text)
    openai_score = get_openai_moderation_score(text)
    return ensemble_weighted_average(bert_score, openai_score)
