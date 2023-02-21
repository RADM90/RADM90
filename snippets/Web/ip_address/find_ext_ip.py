import requests

EXTERNAL_IP = requests.get('https://api.ipify.org').content.decode('utf8')