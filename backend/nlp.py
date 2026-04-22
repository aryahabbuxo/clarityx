from transformers import pipeline

sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

DURABILITY_KEYWORDS = [
    "lasted", "durable", "broke", "quality", "months", "years",
    "still working", "fell apart", "long lasting", "cheap", "sturdy"
]

def longevity_score(reviews):
    if not reviews:
        return {"score": 50, "label": "No reviews available"}
    
    durability_reviews = [
        r for r in reviews
        if any(k in r.lower() for k in DURABILITY_KEYWORDS)
    ]
    
    to_analyze = durability_reviews[:5] if durability_reviews else reviews[:5]
    
    try:
        results = sentiment_model(to_analyze)
        positive = sum(1 for r in results if r["label"] == "POSITIVE")
        score = round((positive / len(results)) * 100)
        
        if score >= 70:
            label = "Excellent"
        elif score >= 50:
            label = "Good"
        elif score >= 30:
            label = "Average"
        else:
            label = "Poor"
            
        return {"score": score, "label": label}
    except Exception as e:
        print(f"NLP error: {e}")
        return {"score": 50, "label": "Could not analyze"}