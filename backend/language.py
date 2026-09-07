import random
from .db import connect
SEEDS={'ka':'self','ru':'food','mi':'place','to':'other','ve':'learn','na':'danger','el':'water','or':'build'}
def maybe_evolve_language(tick):
 c=connect(); v=c.execute('SELECT language_version FROM world WHERE id=1').fetchone()[0]
 if tick%25==0:
  v+=1; token=random.choice(['sha','ven','aru','kei','lom','ira']); meaning=random.choice(['energy','number','sky','metal','motion','memory']); c.execute('INSERT INTO events(tick,kind,description) VALUES (?,?,?)',(tick,'language',f'The language changed: {token} now refers to {meaning}.')); c.execute('UPDATE world SET language_version=? WHERE id=1',(v,))
 c.commit();c.close();return v
def language_dictionary():return dict(SEEDS)
