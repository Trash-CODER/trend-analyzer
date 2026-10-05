from app.models.trend import NetworkGraph, GraphNode, GraphLink, TrendDetail, SentimentBreakdown, VolumeTimePoint
from datetime import datetime, timedelta

def get_landing_network() -> NetworkGraph:
    nodes = [
        # Categories
        {"id": "cat_ai", "label": "Artificial Intelligence", "group": "category", "val": 35},
        {"id": "cat_econ", "label": "Global Economy", "group": "category", "val": 30},
        {"id": "cat_pol", "label": "Politics & Policy", "group": "category", "val": 25},
        {"id": "cat_tech", "label": "Tech & Innovation", "group": "category", "val": 28},
        
        # Topics under AI
        {"id": "topic_llms", "label": "LLM Agents", "group": "topic", "val": 20},
        {"id": "topic_robotics", "label": "Humanoid Robotics", "group": "topic", "val": 16},
        {"id": "topic_chip", "label": "Semiconductor Race", "group": "topic", "val": 18},
        
        # Topics under Economy
        {"id": "topic_inflation", "label": "Interest Rates", "group": "topic", "val": 15},
        {"id": "topic_crypto", "label": "Digital Assets", "group": "topic", "val": 14},
        
        # Topics under Politics
        {"id": "topic_election", "label": "Global Elections", "group": "topic", "val": 18},
        {"id": "topic_climate", "label": "Climate Accords", "group": "topic", "val": 15},
        
        # Topics under Tech
        {"id": "topic_quantum", "label": "Quantum Computing", "group": "topic", "val": 12},
        {"id": "topic_space", "label": "Commercial Space", "group": "topic", "val": 13},
    ]
    
    links = [
        # Category to Topic connections
        {"source": "cat_ai", "target": "topic_llms", "strength": 0.9},
        {"source": "cat_ai", "target": "topic_robotics", "strength": 0.8},
        {"source": "cat_ai", "target": "topic_chip", "strength": 0.85},
        
        {"source": "cat_econ", "target": "topic_inflation", "strength": 0.8},
        {"source": "cat_econ", "target": "topic_crypto", "strength": 0.75},
        
        {"source": "cat_pol", "target": "topic_election", "strength": 0.85},
        {"source": "cat_pol", "target": "topic_climate", "strength": 0.7},
        
        {"source": "cat_tech", "target": "topic_quantum", "strength": 0.75},
        {"source": "cat_tech", "target": "topic_space", "strength": 0.8},
        
        # Cross connections / Intersections
        {"source": "topic_llms", "target": "topic_chip", "strength": 0.9},
        {"source": "topic_inflation", "target": "topic_election", "strength": 0.6},
        {"source": "topic_robotics", "target": "topic_quantum", "strength": 0.5},
    ]
    
    return NetworkGraph(
        nodes=[GraphNode(**n) for n in nodes],
        links=[GraphLink(**l) for l in links]
    )

def get_trend_detail(topic: str) -> TrendDetail:
    clean_topic = topic.replace("-", " ").title()
    
    base_date = datetime.now() - timedelta(days=7)
    timeline = []
    base_vol = 1200
    for i in range(7):
        day_str = (base_date + timedelta(days=i)).strftime("%Y-%m-%d")
        vol = base_vol + (i * 350) + (100 * (i % 3))
        timeline.append(VolumeTimePoint(timestamp=day_str, volume=vol))
        
    kw_nodes = [
        {"id": f"kw_1", "label": f"{clean_topic} Core", "group": "keyword", "val": 25},
        {"id": f"kw_2", "label": "Adoption Rate", "group": "keyword", "val": 18},
        {"id": f"kw_3", "label": "Market Impact", "group": "keyword", "val": 15},
        {"id": f"kw_4", "label": "Regulatory Risk", "group": "keyword", "val": 12},
        {"id": f"kw_5", "label": "Community Sentiment", "group": "keyword", "val": 14},
    ]
    kw_links = [
        {"source": "kw_1", "target": "kw_2", "strength": 0.9},
        {"source": "kw_1", "target": "kw_3", "strength": 0.85},
        {"source": "kw_1", "target": "kw_4", "strength": 0.65},
        {"source": "kw_1", "target": "kw_5", "strength": 0.75},
        {"source": "kw_2", "target": "kw_3", "strength": 0.7},
    ]
    
    keyword_graph = NetworkGraph(
        nodes=[GraphNode(**n) for n in kw_nodes],
        links=[GraphLink(**l) for l in kw_links]
    )
    
    sources = [
        "Reddit r/technology discussion threads (4.2k upvotes)",
        "X (Twitter) trending developer sentiment & thought-leader posts",
        "LinkedIn professional industry analysis updates",
        "Global tech news portals & research briefs"
    ]
    
    return TrendDetail(
        topic=clean_topic,
        category="Artificial Intelligence & Tech" if any(k in clean_topic.lower() for k in ["ai", "llm", "robot", "quantum", "chip"]) else "Global Markets & Innovation",
        sentiment=SentimentBreakdown(positive=58.0, neutral=25.0, negative=17.0),
        timeline=timeline,
        keyword_graph=keyword_graph,
        sources_summary=sources
    )
