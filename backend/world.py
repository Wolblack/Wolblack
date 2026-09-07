import json, random, uuid
from .db import connect
from .agent_mind import MindProvider
from .language import maybe_evolve_language
MAP_W,MAP_H=64,40
PERSONALITIES=["curious","builder","scholar","wanderer","caregiver","skeptic","inventor"]
GOALS=["find_food","explore","learn","build","teach","trade"]
mind=MindProvider()
def seed_agents(n=24):
 c=connect()
 if c.execute("SELECT COUNT(*) FROM agents").fetchone()[0]: c.close(); return
 for i in range(n):
  c.execute("INSERT INTO agents VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",(str(uuid.uuid4())[:8],f"Aru-{i+1:02d}",random.randrange(MAP_W),random.randrange(MAP_H),random.randint(8,34),random.randint(60,100),random.random(),random.choice(PERSONALITIES),random.choice(GOALS),1,json.dumps({"counting":1 if i<8 else 0}),"[]",json.dumps({"ka":"self","ru":"food"})))
 c.execute("INSERT INTO events(tick,kind,description) VALUES (0,'world','The first generation wakes in an unfinished world.')"); c.commit(); c.close()
def _nearby(c,a):
 rows=c.execute("SELECT id,name,x,y,goal,personality FROM agents WHERE alive=1 AND id!=?",(a["id"],)).fetchall()
 return [dict(r) for r in rows if abs(r["x"]-a["x"])+abs(r["y"]-a["y"] )<=6][:5]
def tick_world():
 c=connect(); w=dict(c.execute("SELECT * FROM world WHERE id=1").fetchone()); tick=w["tick"]+1; day=w["day"]+1; year=w["year"]+(day>365); day=1 if day>365 else day
 for a in c.execute("SELECT * FROM agents WHERE alive=1").fetchall():
  k=json.loads(a["knowledge_json"] or '{}'); av=dict(a); av["knowledge_count"]=sum(1 for v in k.values() if v); av["memory_tail"]=json.loads(a["memory_json"] or '[]')[-8:]
  try:r=mind.decide(av,_nearby(c,a),w)
  except Exception as e:r=mind._stub(av,[],w); c.execute("INSERT INTO events(tick,kind,description) VALUES (?,?,?)",(tick,'mind',f"AI fallback: {type(e).__name__}"))
  x,y=a["x"],a["y"]
  if r.action in ("explore","observe","learn"): dx,dy=random.choice([(0,0),(1,0),(-1,0),(0,1),(0,-1)]); x=max(0,min(MAP_W-1,x+dx)); y=max(0,min(MAP_H-1,y+dy))
  energy=max(0,a["energy"]-random.randint(1,3)); age=a["age"]+(day==1); mem=json.loads(a["memory_json"] or '[]'); mem.append({"tick":tick,"thought":r.thought,"action":r.action,"target":r.target,"learning_note":r.learning_note}); mem=mem[-100:]
  if r.action=="learn" or random.random()<.02:
   concept=random.choice(["measurement","geometry","plants","motion","storytelling","logic","energy"]); k[concept]=k.get(concept,0)+1; c.execute("INSERT INTO events(tick,kind,description) VALUES (?,?,?)",(tick,'discovery',f"{a['name']} encountered a new concept: {concept}."))
  if r.action in ("teach","trade") and r.target:c.execute("INSERT INTO events(tick,kind,description) VALUES (?,?,?)",(tick,'social',f"{a['name']} interacted with {r.target} through {r.action}."))
  if energy==0 or age>90:c.execute("UPDATE agents SET alive=0 WHERE id=?",(a["id"],))
  else:c.execute("UPDATE agents SET x=?,y=?,energy=?,age=?,memory_json=?,knowledge_json=? WHERE id=?",(x,y,energy,age,json.dumps(mem),json.dumps(k),a["id"]))
 if tick%10==0:c.execute("INSERT INTO events(tick,kind,description) VALUES (?,?,?)",(tick,'world',f"The world reached tick {tick}; the civilization is adapting."))
 c.execute("UPDATE world SET tick=?,year=?,day=? WHERE id=1",(tick,year,day)); c.commit(); c.close(); maybe_evolve_language(tick)
def snapshot():
 c=connect();w=c.execute("SELECT * FROM world WHERE id=1").fetchone(); rows=c.execute("SELECT id,name,x,y,age,energy,curiosity,personality,goal,alive,knowledge_json,memory_json FROM agents WHERE alive=1").fetchall(); ev=c.execute("SELECT tick,kind,description FROM events ORDER BY id DESC LIMIT 30").fetchall();c.close()
 return {"tick":w["tick"],"year":w["year"],"day":w["day"],"language_version":w["language_version"],"agents":[{**{k:r[k] for k in ('id','name','x','y','age','energy','curiosity','personality','goal','alive')},"knowledge":json.loads(r["knowledge_json"]),"memory":json.loads(r["memory_json"])[-8:]} for r in rows],"events":[dict(e) for e in ev]}
