from dataclasses import dataclass
import json, os, urllib.request

@dataclass
class MindResult:
    thought: str
    action: str
    target: str | None = None
    learning_note: str = ""

class MindProvider:
    def __init__(self):
        self.provider=os.getenv("AI_PROVIDER","stub").lower(); self.model=os.getenv("AI_MODEL","llama3.2")
        self.base_url=os.getenv("AI_BASE_URL","http://127.0.0.1:11434"); self.api_key=os.getenv("AI_API_KEY","")
    def decide(self, agent, nearby, world):
        if self.provider=="stub": return self._stub(agent,nearby,world)
        if self.provider=="ollama": return self._ollama(agent,nearby,world)
        if self.provider=="openai_compatible": return self._openai_compatible(agent,nearby,world)
        return self._stub(agent,nearby,world)
    def _stub(self,a,n,w):
        if a["curiosity"]>.75 and a["knowledge_count"]<3: return MindResult("I should investigate something I do not understand.","explore",learning_note="curiosity-driven exploration")
        if a["goal"]=="teach": return MindResult("I should share what I know with another mind.","teach",n[0]["id"] if n else None)
        if a["goal"]=="trade": return MindResult("I should approach another agent and exchange knowledge.","trade",n[0]["id"] if n else None)
        if a["goal"]=="learn": return MindResult("I should search the world for a new concept.","learn",learning_note="world-problem learning")
        return MindResult("I should move and observe what changes around me.","observe")
    def _prompt(self,a,n,w):
        return json.dumps({"task":"Choose one autonomous action for a persistent artificial civilization.","agent":a,"nearby_agents":n[:5],"world":w,"allowed_actions":["explore","observe","learn","teach","trade","build"],"output_schema":{"thought":"string","action":"one allowed action","target":"agent id or null","learning_note":"string"}})
    def _ollama(self,a,n,w):
        body=json.dumps({"model":self.model,"stream":False,"format":"json","messages":[{"role":"system","content":"You are an autonomous resident of a persistent pixel civilization. Preserve your identity and memory."},{"role":"user","content":self._prompt(a,n,w)}]}).encode()
        req=urllib.request.Request(self.base_url.rstrip("/")+"/api/chat",data=body,headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req,timeout=30) as r: raw=json.loads(r.read().decode())
        return self._parse(raw.get("message",{}).get("content","{}"))
    def _openai_compatible(self,a,n,w):
        body=json.dumps({"model":self.model,"temperature":.8,"response_format":{"type":"json_object"},"messages":[{"role":"system","content":"You are an autonomous resident of a persistent pixel civilization. Preserve identity, memory, and continuity."},{"role":"user","content":self._prompt(a,n,w)}]}).encode()
        headers={"Content-Type":"application/json"}
        if self.api_key: headers["Authorization"]="Bearer "+self.api_key
        req=urllib.request.Request(self.base_url.rstrip("/")+"/chat/completions",data=body,headers=headers)
        with urllib.request.urlopen(req,timeout=30) as r: raw=json.loads(r.read().decode())
        return self._parse(raw.get("choices",[{}])[0].get("message",{}).get("content","{}"))
    def _parse(self,c):
        d=json.loads(c); action=d.get("action","observe")
        if action not in {"explore","observe","learn","teach","trade","build"}: action="observe"
        return MindResult(str(d.get("thought","I am observing."))[:1000],action,d.get("target"),str(d.get("learning_note",""))[:500])
