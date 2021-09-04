from flask import Flask,request,redirect,Response
import requests, os, re

app = Flask('__main__')
UPTIME_SITE = os.environ.get('UPTIME_SITE', 'https://stats.uptimerobot.com/5WXLnI8WO')

@app.route('/api/<path:path>', methods=['POST','GET', 'OPTION'])
def api(path):
  forward_url = "https://stats.uptimerobot.com/api/%s" % path
  resp = requests.get(forward_url)
  resptext = resp.content.decode('utf-8')
  excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
  headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
  headers.append(['Access-Control-Allow-Origin', '*'])
  return Response(resptext, resp.status_code, headers)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['POST','GET', 'OPTION'])
def proxy(path):
  if request.method=='GET':
    resp = requests.get(f'{UPTIME_SITE}{path}')
  elif request.method=='POST':
    resp = requests.post(f'{UPTIME_SITE}{path}',data=request.data)
  else: #'OPTION'
    resp = requests.options(f'{UPTIME_SITE}{path}')
  excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
  headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
  headers.append(['Access-Control-Allow-Origin', '*'])
  resptext = resp.content.decode('utf-8')
  resptext = resptext.replace("https://stats.uptimerobot.com/api/","%s://%s/api/"% (request.scheme, request.host))
  response = Response(resptext, resp.status_code, headers)
  return response