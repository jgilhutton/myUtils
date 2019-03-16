import threading
import subprocess
from sys import argv,stdout
import requests
from time import sleep

IPS = []
ts = []
NUM_THREADS = 10
Q = 0

with open(argv[1], 'r') as ips:
  IPS = [x.strip() for x in ips.readlines()]
  

HEADERS = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
	    'Accept': 'text/html,application/xml;*/*;q=0.8',
	    'Accept-Language': 'en-US;q=0.5',
	    'Accept-Encoding': 'gzip, deflate',
	    'DNT': '1',
	    'Connection': 'close',
	    }

def ping(ip):
  global Q
  proc = subprocess.Popen('ping -n 1 -w 3000 %s' %ip, shell = True, stdout =  subprocess.PIPE).communicate()[0]
  #myprint(Q,len(IPS))
  if "Respuesta desde" in proc:
    getindex(ip)
  Q += 1
  #myprint(Q,len(IPS))
    
def getindex(ip):
  L_HEADERS = HEADERS # Local
  L_HEADERS['Host'] = ip
  try:
    r = requests.get('http://%s/' %ip,headers=L_HEADERS).text
    if r.strip() != '':
      print '\r{} Ok'.format(ip)
      #myprint(Q,len(IPS))
      log(r, ip)
  except Exception as e:
    pass
    #myprint(Q,len(IPS))
  print '{}/{}\r'.format(Q,len(IPS)),
    
def log(index, ip):
  with open(ip+'.html', 'w') as dump:
    dump.write(index.strip())

class Th(threading.Thread):
  def __init__(self,ip):
    threading.Thread.__init__(self)
    self.ip = ip
    
  def run(self):
    ts.append(self)
    ping(ip)

c = 0
while True:
  for ip in IPS[c:c + NUM_THREADS]:
    Th(ip).start()
    sleep(0.05)
  for t in ts:
    t.join(8)
  ts = []
  if (len(IPS)-c) < NUM_THREADS:
    for ip in IPS[c:]:
      Th(ip).start()
      sleep(0.05)
    for t in ts:
      t.join(8)
    break
  c += NUM_THREADS
