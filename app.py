from flask import Flask, jsonify
import requests, datetime
app=Flask(__name__)
@app.route('/')
def home():
 return requests.get('https://raw.githubusercontent.com/shaam-xyz/football/main/index.html').text
@app.route('/api/league30/<lg>')
def api(lg):
 up=[];live=[]
 for i in range(1,91):
  d=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime('%Y%m%d')
  try:
   r=requests.get(f'https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={d}',timeout=4)
   for ev in r.json().get('events',[]):
    comp=ev['competitions'][0];c0=comp['competitors'][0];c1=comp['competitors'][1]
    is_live=comp['status']['type']['state']=='in'
    base={'home':c0['team']['displayName'],'away':c1['team']['displayName'],'league':lg,'date':d,'isLive':is_live}
    (live if is_live else up).append(base)
   if len(up)>=8: break
  except: continue
 return jsonify({'live':live,'up':up[:8],'msg': str(len(up)) if up else 'موسم منتهي'})
@app.route('/api/standing/<lg>')
def st(lg):
 try:
  r=requests.get(f'https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/standings',timeout=5)
  e=r.json()['children'][0]['standings']['entries']
  return jsonify({'standing':[{'pos':i+1,'team':x['team']['displayName'],'points':int({s['name']:s['value'] for s in x['stats']}.get('points',0))} for i,x in enumerate(e[:15])]})
 except: return jsonify({'standing':[]})
if __name__=='__main__':app.run(host='0.0.0.0',port=10000)
