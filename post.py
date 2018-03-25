import requests
url='http://101.132.194.57:5000/username'
r=requests.post(url,data={'action':'getinfo','username':'6339231763','getid':'5441290280'})
print(r.text)