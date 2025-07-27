import pandas as pd
from googleapiclient import discovery
import time
import io
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('PERSPECTIVE_API_KEY')

client = discovery.build(
    "commentanalyzer",
    "v1alpha1",
    developerKey=API_KEY,
    discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
    static_discovery=False,
)

attributes = {
    'TOXICITY': {},
    'INSULT': {},
    'THREAT': {},
    'SEVERE_TOXICITY': {},
    'IDENTITY_ATTACK': {}
}

def analyze_single_text(text: str) -> dict:
    try:
        analyze_request = {
            'comment': {'text': text},
            'requestedAttributes': attributes
        }
        response = client.comments().analyze(body=analyze_request).execute()
        scores = {
            attr: round(response['attributeScores'][attr]['summaryScore']['value'], 4)
            for attr in attributes
        }
        return scores
    except Exception as e:
        return {attr: None for attr in attributes}

def analyze_texts(df: pd.DataFrame) -> pd.DataFrame:
    scores_list = []
    for text in df['text']:
        scores = analyze_single_text(str(text))
        scores_list.append(scores)
        time.sleep(1)  # to respect quota
    scores_df = pd.DataFrame(scores_list)
    return pd.concat([df, scores_df], axis=1)
