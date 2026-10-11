from pathlib import Path
import json,collections
from PIL import Image,ImageOps,ImageDraw
r=Path('evidence/coder390/main-judgements');d=Path('runs/coder390-audit')
s=json.loads((r/'negative-sample.json').read_text());required=collections.defaultdict(set)
for key,ids in {**s['samples'],**s['per_family']}.items():
 model,condition,*_=key.split(':');required[model].update(ids)
for p in (r/'items').glob('*/*/text-labels.json'):
 labels=json.loads(p.read_text())
 if any(x.get('claims') or x.get('uncertain') for x in labels.values()):required[p.parent.parent.name].add(p.parent.name)
for p in (r/'items').glob('*/*/image-labels.json'):
 l=json.loads(p.read_text())
 if l.get('claims') or l.get('uncertain'):required[p.parent.parent.name].add(p.parent.name)
queue=[]
for model,ids in sorted(required.items()):
 for identity in sorted(ids):
  p=r/'items'/model/identity
  if identity.startswith('portrait') and (p/'portrait.png').exists():queue.append((model,identity,p/'portrait.png'))
for batch in range(0,len(queue),12):
 sheet=Image.new('RGB',(1152,4*420),'#eeeeee');draw=ImageDraw.Draw(sheet)
 for n,(m,i,p) in enumerate(queue[batch:batch+12]):
  im=Image.open(p).convert('RGBA');bg=Image.new('RGBA',im.size,'white');bg.alpha_composite(im);im=ImageOps.contain(bg.convert('RGB'),(380,380))
  x=(n%3)*384;y=(n//3)*420;sheet.paste(im,(x+(384-im.width)//2,y+28));draw.text((x+6,y+7),m+'/'+i,fill='black')
 sheet.save(d/('sheet-%02d.png'%(batch//12)))
(d/'queue.json').write_text(json.dumps({'required':{k:sorted(v) for k,v in required.items()},'sheets':[[m,i] for m,i,p in queue]},indent=2)+'\n')
print('required counts',{k:len(v) for k,v in required.items()},'portrait images',len(queue),'sheets',(len(queue)+11)//12)
neg=[]
for model in ['base-matched','coder390']:
 ids=set()
 for key,values in {**s['samples'],**s['per_family']}.items():
  if key.startswith(model+':portrait'):ids.update(values)
 for identity in sorted(ids):
  source=json.loads((r/'items'/model/identity/'source.json').read_text())['source']
  neg.append(model+'/'+identity+'\n'+(Path(source)/'reasoning.txt').read_text())
(d/'negative-reasoning.txt').write_text('\n\n'.join(neg))
print('negative text chars',len((d/'negative-reasoning.txt').read_text()))
