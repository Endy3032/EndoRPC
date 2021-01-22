import webbrowser, time, sys, json
from threading import Thread
from flask import Flask, request, redirect
from OAuthAuthenticator import Oauth

def run():
  app.run()

app = Flask(__name__)
t = Thread(target = run)
t.setDaemon(True)

def begin():
  t.start()
  webbrowser.open('http://127.0.0.1:5000')

Data = {
  "username": "",
  "user_tag": "",
  "avt_hash": "",
  "id": ""
}

@app.route('/', methods=['get'])
def index():
  return redirect(Oauth.discord_login_url)

@app.route('/login', methods=['get'])
def login():
  code = request.args.get('code')
  access_token = Oauth.get_access_token(code)
  user_json = Oauth.get_user_json(access_token)
  username = user_json['username']
  user_tag = user_json['discriminator']
  avt_hash = user_json['avatar']
  user_id = user_json['id']
  global Data
  Data['username'] = username
  Data['user_tag'] = user_tag
  Data['avt_hash'] = avt_hash
  Data['id'] = user_id
  try:
    return 'You can close this tab now!'
  finally:
    myJSON = json.dumps(Data)
    with open("UserConfig.json", "w") as jsfile:
      jsfile.write(myJSON)
    exit

