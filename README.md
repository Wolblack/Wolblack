# Living Pixel World

A persistent artificial civilization designed as a learning environment.

## v0.3 — AI minds
- persistent FastAPI + SQLite world
- autonomous agent decision cycle: observe → remember → decide → act → learn
- provider-agnostic AI minds with local stub, Ollama, and OpenAI-compatible modes
- long-term agent memory
- agent goals, personalities, relationships and knowledge
- evolving world language version
- world-level God AI that creates conditions and learning events rather than micromanaging citizens
- learning API for mathematics, physics, computer science, biology, engineering, history and English
- curated learning-source layer
- browser pixel-world interface

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Open `http://127.0.0.1:8000`.

## Enable actual AI minds locally

Install Ollama, pull a model, then start the server with:

```bash
AI_PROVIDER=ollama AI_MODEL=llama3.2 uvicorn backend.main:app --reload
```

Or configure an OpenAI-compatible endpoint using `.env.example`.

The default `stub` mode keeps the world fully runnable without an AI API.

## Learning world

The project does not pretend that NotebookLM/Gemini Notebook is a generic consumer API. Google renamed NotebookLM to Gemini Notebook in July 2026; it remains the research workspace. This repository therefore keeps an explicit source manifest and a learning-event layer that can be fed from curated material.

MIT OpenCourseWare is an especially strong foundation because it provides free/open materials across thousands of MIT courses, including structured syllabi and learning activities.
