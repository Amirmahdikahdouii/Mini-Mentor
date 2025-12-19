# Mini Mentor Agent

An AI-powered learning roadmap generator that creates personalized learning paths based on your goals. Built with Vue 3 (frontend) and FastAPI (backend), integrated with Claude AI.

![Mini Mentor](https://img.shields.io/badge/AI-Claude-blue) ![Vue.js](https://img.shields.io/badge/Vue.js-3.x-green) ![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal) ![Docker](https://img.shields.io/badge/Docker-Compose-blue)

## Features

- **AI-Powered Roadmaps**: Generate comprehensive learning paths using Claude AI
- **Visual Timeline**: Interactive timeline showing learning phases and milestones
- **Markdown Support**: Rich formatted content with syntax highlighting
- **History Tracking**: Save and revisit your generated roadmaps
- **Dark Theme**: Modern, developer-focused UI design
- **Dockerized**: Easy deployment with Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Claude API key from [Anthropic](https://console.anthropic.com/)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Mini-Mentor-Agent
   ```

2. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```bash
   CLAUDE_API_KEY=your_claude_api_key_here
   ```

3. **Start the application**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Project Structure

```
Mini-Mentor-Agent/
├── front-end/                 # Vue 3 frontend
│   ├── src/
│   │   ├── components/        # Vue components
│   │   ├── views/             # Page views
│   │   ├── services/          # API services
│   │   ├── router/            # Vue Router config
│   │   └── assets/            # Styles and assets
│   ├── Dockerfile
│   └── nginx.conf
├── backend/                   # FastAPI backend
│   ├── app/
│   │   ├── main.py           # FastAPI app
│   │   ├── models.py         # SQLAlchemy models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── database.py       # Database config
│   │   └── services/
│   │       └── claude_service.py  # Claude AI integration
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
└── README.md
```

## Development

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp env.example .env
# Edit .env and add your CLAUDE_API_KEY

# Run development server
uvicorn app.main:app --reload --port 8000
```

### Frontend Development

```bash
cd front-end

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend development server runs on port 3000 with API proxy to backend.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/api/roadmaps` | Create a new roadmap |
| GET | `/api/roadmaps` | List all roadmaps |
| GET | `/api/roadmaps/{id}` | Get a specific roadmap |
| DELETE | `/api/roadmaps/{id}` | Delete a roadmap |

### Create Roadmap Request

```json
POST /api/roadmaps
{
  "query": "I want to learn Go language"
}
```

### Response

```json
{
  "id": 1,
  "user_query": "I want to learn Go language",
  "title": "Go Programming Language Learning Roadmap",
  "content": "## Phase 1: Fundamentals...",
  "visual_data": {
    "phases": [...],
    "total_duration": "3-6 months"
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CLAUDE_API_KEY` | Your Anthropic Claude API key | Yes |
| `DATABASE_URL` | SQLite database URL | No (defaults to `sqlite:///./data/roadmaps.db`) |

## Tech Stack

### Frontend
- Vue 3 with Composition API
- Vue Router
- Axios
- Marked (Markdown rendering)
- Highlight.js (Syntax highlighting)

### Backend
- FastAPI
- SQLAlchemy (SQLite)
- Anthropic Claude SDK
- Pydantic
- Uvicorn

### Infrastructure
- Docker & Docker Compose
- Nginx (production frontend)

## License

MIT License

