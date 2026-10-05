from datetime import datetime
from typing import List, Literal, Dict, Any, Optional
from pydantic import BaseModel, Field

# --- Graph Entities ---
class GraphNode(BaseModel):
    id: str
    label: str
    group: str           # e.g., 'category', 'topic', 'keyword'
    val: float           # Size / Weight (e.g., mention frequency)

class GraphLink(BaseModel):
    source: str          # Source node id
    target: str          # Target node id
    strength: float      # Link weight

class NetworkGraph(BaseModel):
    nodes: List[GraphNode]
    links: List[GraphLink]

# --- Analytics Entities ---
class SentimentBreakdown(BaseModel):
    positive: float      # e.g., 55.4%
    neutral: float       # e.g., 28.2%
    negative: float      # e.g., 16.4%

class VolumeTimePoint(BaseModel):
    timestamp: str       # e.g., "2026-09-20"
    volume: int

class TrendDetail(BaseModel):
    topic: str
    category: str
    sentiment: SentimentBreakdown
    timeline: List[VolumeTimePoint]
    keyword_graph: NetworkGraph
    sources_summary: List[str]
