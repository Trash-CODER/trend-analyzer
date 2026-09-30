# Trend Analyzer: Social Intelligence Graph & Multi-Agent Trend Reporter

## 1. System Overview & Core User Flows
An interactive web application providing visual graph-based exploration of trending topics across social communities (Reddit, X, LinkedIn style).

### User Journey
1. **Interactive Topic Network (Landing View)**:
   - Visual physics-simulated network graph of high-level topics (e.g., AI, Economy, Politics, Tech).
   - Clicking a node routes to the focused Trend Dashboard.
2. **Trend Dashboard (Drill-Down & Search)**:
   - **Topic Search Bar**: Look up any custom topic or keyword.
   - **Sentiment Pie Chart**: Distribution of public sentiment (Positive, Neutral, Negative).
   - **Timeline Volume Line Chart**: Historical & recent engagement/mention trajectory over time.
   - **Keyword Co-occurrence Graph**: Interactive sub-graph where nodes represent frequently co-occurring keywords/entities connected by edge strength.
3. **AI Explainer & Report Generator (Gemini Pro Agent)**:
   - Interactive Q&A with an explainer bot to uncover *why* the trend is emerging.
   - On-demand structured synthesis report generation (Markdown breakdown of drivers, sentiment, risks, and forecasts).
4. **Auth & Report Persistence (Relational + JSON)**:
   - Sign up / Log in via JWT auth.
   - Authenticated users can save generated trend reports and snapshots into a SQLite database.

## 2. Shared Data Contracts (Source of Truth)

All backend endpoints and frontend state must match these schemas.

### Python Backend Schemas (`backend/app/models/trend.py` & `report.py`)
```python
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

# --- AI Report & User Schemas ---
class ReportGenerateRequest(BaseModel):
    topic: str

class SavedReportResponse(BaseModel):
    id: int
    topic_name: str
    markdown_content: str
    trend_snapshot: Optional[Dict[str, Any]] = None
    created_at: datetime

# TypeScript Frontend Interfaces (frontend/src/types/trend.ts)
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

export interface SavedReport {
  id: number;
  topic_name: string;
  markdown_content: string;
  trend_snapshot?: Record<string, any>;
  created_at: string;
}

## 3. Database Schema (SQLite + JSON Hybrid)
Implemented via SQLAlchemy in backend/app/db/models.py:

User: id, email, hashed_password, created_at

SavedReport: id, user_id (ForeignKey), topic_name, markdown_content (Text), trend_snapshot (JSON), created_at

## 4. Tech Stack & Dependencies
Backend (backend/requirements.txt)
fastapi>=0.110.0

uvicorn[standard]>=0.28.0

pydantic>=2.6.0

sqlalchemy>=2.0.0

python-jose[cryptography]>=3.3.0 (JWT token handling)

passlib[bcrypt]>=1.7.4 (Password hashing)

google-genai>=0.1.0 (Gemini Pro client)

python-dotenv>=1.0.0

requests>=2.31.0

Frontend (frontend/package.json)
React 18+ (Vite + TypeScript)

Tailwind CSS

lucide-react (Icons)

react-force-graph-2d (Interactive Canvas/WebGL network graphs)

recharts (Pie and Line charts)

react-markdown (For rendering the AI report)

axios (HTTP client with auth interceptor)

5. Vibe Coding Rules & Operational Constraints
Strict Milestone Boundaries: Only build the currently assigned milestone. Do not scaffold unrequested features.

Environment Isolation: Never touch backend/.venv or frontend/node_modules.

Contract Adherence: Any schema change must be reflected in both backend Pydantic models and frontend TypeScript interfaces simultaneously.

Mock First: Build working UI and routes using mock datasets before calling external APIs or Gemini token consumption.

Git Checkpoints: Commit after each milestone is validated.

6. Development Roadmap & Step-by-Step Milestones
Phase 1: Foundations & Connectivity
[ ] M1.1 Backend Core: Initialize FastAPI (backend/app/main.py) with GET /api/health and CORS.

[ ] M1.2 Frontend Core: Initialize Vite React + TypeScript template, install Tailwind CSS, and verify health check call.

Phase 2: Contracts & Mock Trend Engine
[ ] M2.1 Schemas: Set up backend/app/models/trend.py and frontend/src/types/trend.ts matching Section 2.

[ ] M2.2 Mock Exploration Service: Build backend/app/services/mock_trends.py:

GET /api/topics/network: Returns landing page topic network (Nodes & Links).

GET /api/trends/{topic}: Returns TrendDetail (Sentiment, Timeline, Keyword Graph).

Phase 3: Visual Exploration Frontend
[ ] M3.1 Landing Graph View: Build interactive full-screen network graph using react-force-graph-2d. Clicking a node navigates to /dashboard/{topic}.

[ ] M3.2 Trend Dashboard View:

Search input to query new topics.

Sentiment Pie Chart & Timeline Line Chart using recharts.

Secondary Keyword Network Graph.

## Phase 4: Gemini AI Explainer & Report Writer
[ ] M4.1 Explainer Agent: Implement backend/app/agents/explainer.py using google-genai to answer queries about the active trend.

[ ] M4.2 Report Generator: Prompt Gemini Pro with current trend metrics (TrendDetail) to output a structured Markdown executive report.

[ ] M4.3 Frontend Report Drawer: Markdown viewer displaying generated insights with a "Save Report" action.

## Phase 5: Authentication & Report Persistence
[ ] M5.1 Auth API: Implement SQLite database with SQLAlchemy (User & SavedReport) and JWT endpoints (/api/auth/register, /api/auth/login).

[ ] M5.2 Report Endpoints: Protected routes (POST /api/reports, GET /api/reports) allowing logged-in users to save and view their library.

[ ] M5.3 Auth UI: Login/Register modal and Saved Reports drawer on the frontend.


## Rules
- Never edit files inside `.venv/` or `node_modules/`.
- Keep backend API routes and agent workflows modular.
- Any new backend packages must be recorded in `backend/requirements.txt`.