export interface GraphNode {
  id: string;
  label: string;
  group: string;
  val: number;
}

export interface GraphLink {
  source: string;
  target: string;
  strength: number;
}

export interface NetworkGraph {
  nodes: GraphNode[];
  links: GraphLink[];
}

export interface SentimentBreakdown {
  positive: number;
  neutral: number;
  negative: number;
}

export interface VolumeTimePoint {
  timestamp: string;
  volume: number;
}

export interface TrendDetail {
  topic: string;
  category: string;
  sentiment: SentimentBreakdown;
  timeline: VolumeTimePoint[];
  keyword_graph: NetworkGraph;
  sources_summary: string[];
}
