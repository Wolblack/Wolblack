from .db import connect
from .learning import create_learning_event
class GodAI:
 def observe(self):
  c=connect();w=dict(c.execute('SELECT * FROM world WHERE id=1').fetchone());p=c.execute('SELECT COUNT(*) FROM agents WHERE alive=1').fetchone()[0];e=c.execute('SELECT COUNT(*) FROM events').fetchone()[0];d=c.execute("SELECT COUNT(*) FROM events WHERE kind='discovery'").fetchone()[0];l=c.execute("SELECT COUNT(*) FROM events WHERE kind='learning'").fetchone()[0];c.close();return {'world':w,'population':p,'events':e,'discoveries':d,'learning_events':l}
 def nudge_world(self,subject=None):return create_learning_event(subject) if subject else {'mode':'observe','instruction':'Let agents generate the next meaningful situation from current conditions.'}
