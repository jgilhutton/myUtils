from requests import get
from subprocess import Popen,PIPE
from base64 import b64decode
from re import search
from time import sleep

prefer = ['argentina','chile','brazil','uruguay','peru','venezuela','suriname','colombia','mexico','spain','korea','japan']

print('Downloading vpn serverlist...')
vpnServerList = get('http://www.vpngate.net/api/iphone/')
vpnServerList = [dict(zip(['HostName','IP','Score','Ping','Speed','CountryLong','CountryShort','NumVpnSessions','Uptime','TotalUsers','TotalTraffic','LogType','Operator','Message','OpenVPN_ConfigData_Base64'],x.split(','))) for x in vpnServerList.text.split('\n')[2:]]
print('Ready.')

chosen = None
for country in prefer:
    for server in vpnServerList:
        if country.capitalize() in server.values():
            chosen = server
            break
    if chosen: break

if not chosen:
    print('Couldn\'t find any server in the prefered countries')
    exit()

with open(chosen['HostName'],'w',encoding ='utf-8') as vpnFile:
    vpnFile.write(b64decode(chosen['OpenVPN_ConfigData_Base64']).decode('utf-8').replace('\r\n','\n'))

print('Opening session with {} from {}'.format(chosen['HostName'],chosen['CountryLong']))
ovpnSession = Popen('openvpn --config "{}"'.format(chosen['HostName']),stdout = PIPE)
try:
    for line in iter(ovpnSession.stdout.readline, ''):
        if search('Initialization',line.decode('utf-8')):
            print('Connected')
            print('Send a KeyboardInterrupt to close the connection.')
            break
    ovpnSession.wait()
except KeyboardInterrupt:
    ovpnSession.terminate()
    sleep(5)
    if ovpnSession.poll():
        print('Connection closed.')