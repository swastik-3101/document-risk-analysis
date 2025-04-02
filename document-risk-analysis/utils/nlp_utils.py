import spacy
from textblob import TextBlob
from typing import List, Dict

# Load SpaCy model
nlp = spacy.load("en_core_web_sm")

# Define risk keywords
RISK_KEYWORDS = [
    "breach", "penalty", "fine", "risk", "litigation",
    "obligation", "liability", "compliance", "violation",
    "lawsuit", "sanction", "infraction", "duty", "responsibility"
]

def preprocess_text(text: str) -> List[str]:
    """
    Tokenizes and preprocesses text to handle lemmatization and normalization.
    Args:
        text (str): Input text.
    Returns:
        List[str]: Processed list of tokens.
    """
    doc = nlp(text)
    return [token.lemma_.lower() for token in doc if token.is_alpha]

def extract_risks(text: str) -> List[str]:
    """
    Extracts sentences containing risk-related keywords.
    Args:
        text (str): Input text to analyze.
    Returns:
        List[str]: Sentences containing risk keywords.
    """
    doc = nlp(text)
    risks = [sent.text for sent in doc.sents if any(keyword in preprocess_text(sent.text) for keyword in RISK_KEYWORDS)]
    return risks

def analyze_sentiment(text: str) -> Dict[str, float]:
    """
    Analyzes sentiment of a given text using TextBlob.
    Args:
        text (str): Text to analyze.
    Returns:
        Dict[str, float]: Sentiment polarity and subjectivity scores.
    """
    sentiment = TextBlob(text).sentiment
    return {"polarity": sentiment.polarity, "subjectivity": sentiment.subjectivity}

def categorize_risks(risks_with_sentiment: List[Dict]) -> Dict[str, List[Dict]]:
    """
    Categorizes risks into high, medium, and low risk based on polarity.
    Args:
        risks_with_sentiment (List[Dict]): List of risks with sentiment scores.
    Returns:
        Dict[str, List[Dict]]: Categorized risks.
    """
    categorized = {"high": [], "medium": [], "low": []}
    for risk in risks_with_sentiment:
        polarity = risk["polarity"]
        if polarity < -0.3:
            categorized["high"].append(risk)
        elif -0.3 <= polarity <= 0.3:
            categorized["medium"].append(risk)
        else:
            categorized["low"].append(risk)
    return categorized

def analyze_risk(text: str) -> Dict:
    """
    Identifies potential risks in text and provides sentiment analysis.
    Args:
        text (str): Input text.
    Returns:
        Dict: Risks with sentiment analysis and categorization.
    """
    # Extract risks from text
    risks = extract_risks(text)

    # Perform sentiment analysis on risks
    risks_with_sentiment = []
    for risk in risks:
        sentiment = analyze_sentiment(risk)
        risks_with_sentiment.append({
            "text": risk,
            "polarity": sentiment["polarity"],
            "subjectivity": sentiment["subjectivity"]
        })

    # Categorize risks by sentiment polarity
    categorized_risks = categorize_risks(risks_with_sentiment)

    return {
        "risks_with_sentiment": risks_with_sentiment,
        "categorized_risks": categorized_risks,
        "total_risks": len(risks)
    }
#TAX
#AGREEMENT