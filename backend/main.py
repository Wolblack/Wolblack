from pathlib import Path
from fastapi import FastAPI,HTTPException
from fastapi.responses import FileResponse
from .db import init_db,connect
from .world import seed_agents,tick_world,snapshot
from .god_ai import GodAI
from .learning import create_learning_event,CONCEPTS
app=FastAPI(title='Living Pixel World',version='0.3.0');BASE=Path(__file__).resolve().parent.parent; god_ai=GodAI()
@app.on_event('startup')
def startup():init_db();seed_agents()
@app.get('/api/world')
def world():return snapshot()
@app.post('/api/tick')
def tick():tick_world();return snapshot()
@app.post('/api/tick/{count}')
def tick_many(count:int):
 if count<1 or count>100:raise HTTPException(400,'count must be between 1 and 100')
 for _ in range(count):tick_world()
 return snapshot()
@app.get('/api/god')
def god():return god_ai.observe()
@app.get('/api/lesson/{subject}')
def lesson(subject:str):return create_learning_event(subject)
@app.get('/api/subjects')
def subjects():return {'subjects':sorted(CONCEPTS),'concepts':CONCEPTS}
@app.get('/api/agent/{agent_id}')
def agent(agent_id:str):
 c=connect();r=c.execute('SELECT * FROM agents WHERE id=?',(agent_id,)).fetchone();c.close()
 if not r:raise HTTPException(404,'agent not found')
 import json
 return {**dict(r),'knowledge':json.loads(r['knowledge_json']),'memory':json.loads(r['memory_json'])}
@app.get('/')
def index():return FileResponse(BASE/'frontend'/'index.html')
