import json, os, sys, webbrowser, ctypes
from threading import Thread
from urllib.request import build_opener, install_opener
current_dir = os.path.abspath(os.path.dirname(__file__))

# Messagebox Function
def msg(title, message):
  if sys.platform == 'darwin':
    os.system(f"osascript -e 'Tell application \"System Events\" to display dialog \"{message}\" with title \"{title}\"'")
  elif sys.platform == 'win32':
    ctypes.windll.user32.MessageBoxW(0, message, title, 0)

try:
  import requests
  from PyQt6 import QtWidgets
  if sys.platform == 'darwin':
    from UIM import Ui_MainWindow
  elif sys.platform == 'win32':
    from UIW import UI_MainWindow

  from pypresence import Presence
  from flask import Flask, request, redirect
except:
  os.system(f'pip3.9 install -r {os.path.join(current_dir, "Resources", "requirements.txt")}')
  msg("EndyPresence", "Dependencies installed. Reopen the program to continue!")
  exit(0)

# Setup
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

# Preventing HTTP 403 Forbidden
# Reason: Discord servers will reject requests from Python agent therefore
# using Mozilla user agent would trick Discord servers into giving us info
opener = build_opener()
opener.addheaders = [("User-agent", "Mozilla/5.0")]
install_opener(opener)


# Discord Authentication API
class Oauth(object):
  scope = "identify"
  client_id = "799634564875681792"
  client_secret = "NLNhwnpsbkUjPgSAWheugxlNP0WA-FYb"
  redirect_uri = "http://127.0.0.1:3032/login"
  discord_api_url = f"https://discord.com/api/"
  discord_token_url = f"https://discord.com/api/oauth2/token"
  discord_login_url = f"https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}"

  @staticmethod
  def get_access_token(code):
    data = {
      "client_id": Oauth.client_id,
      "client_secret": Oauth.client_secret,
      "grant_type": "authorization_code",
      "code": code,
      "redirect_uri": Oauth.redirect_uri,
      "scope": Oauth.scope
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    access_token = requests.post(url=Oauth.discord_token_url, data=data, headers=headers)
    return access_token.json().get("access_token")

  @staticmethod
  def get_user_json(access_token):
    url = Oauth.discord_api_url + "/users/@me"
    headers = {"Authorization": f"Bearer {access_token}"}
    return requests.get(url=url, headers=headers).json()

  @staticmethod
  def refresh_token(refresh_token):
    url = Oauth.discord_api_url + "/oauth2/token"
    data = {
      "client_id": Oauth.client_id,
      "client_secret": Oauth.client_secret,
      "grant_type": "refresh_token",
      "refresh_token": refresh_token,
      "redirect_uri": Oauth.redirect_uri,
      "scope": "identify"
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    return requests.post(url=url, data=data, headers=headers).json()


# FlaskServer
webserver = Flask("Discord OAuthenticator")


def run():
  webserver.run(host = "127.0.0.1", port = 3032)


FlaskApp = Thread(target=run)
FlaskApp.setDaemon(True)


@webserver.route("/", methods=["get"])
def index(): return redirect(Oauth.discord_login_url)


@webserver.route("/login", methods=["get"])
def login():
  user_json = Oauth.get_user_json(Oauth.get_access_token(request.args.get("code")))
  global username, user_tag, pfp_hash, user_id
  username = user_json["username"]
  user_tag = user_json["discriminator"]
  pfp_hash = user_json["avatar"]
  user_id = user_json["id"]
  ui.update(username, user_tag, pfp_hash, user_id)
  with open(os.path.join(current_dir, "Database.json"), "r+") as db:
    data = json.load(db)
    firstrun = data[0]
    other = data[1:3]
    userdata = data[3]
    appid = data[4]

    firstrun["FR"] = 0
    userdata["UD"][0]["name"] = username
    userdata["UD"][0]["tag"] = user_tag
    userdata["UD"][0]["pfp_hash"] = pfp_hash
    userdata["UD"][0]["user_id"] = user_id
    db.seek(0)
    ls = [firstrun, other[0], other[1], userdata, appid]
    db.write(json.dumps(ls))
    db.truncate()

  return "<script>alert('Authorization complete! You can now close the tab and return to the app');</script>"


@webserver.route("/refresh", methods=["get"])
def refresh():
  return "<script>alert('Authorization complete! You can now return to the app');</script>", redirect(Oauth.discord_login_url)


FlaskApp.start()

def update_rpc(limg, simg, ltxt, stxt, details, state, b1t, b1u, b2t, b2u):
  buttons = []
  if len(b1t) != 0 and len(b1u) != 0: buttons.append({"label": f"{b1t}", "url": f"{b1u}"})
  if len(b2t) != 0 and len(b2u) != 0: buttons.append({"label": f"{b2t}", "url": f"{b2u}"})
  RPC.update(
    large_image = limg if len(limg) > 0 else None,
    small_image = simg if len(simg) > 0 else None,
    details = details if len(details) >= 2 else None,
    state = state if len(state) >= 2 else None,
    buttons = buttons or None,
    large_text = ltxt if len(ltxt) >= 2 else None,
    small_text = stxt if len(stxt) >= 2 else None
  )
  ui.update_preview()
  ui.save_presence()

ui.rpcb.clicked.connect(lambda: update_rpc(str(ui.limge.currentText()), str(ui.simge.currentText()), ui.ltxte.toPlainText(), ui.stxte.toPlainText(), ui.detailse.toPlainText(), ui.statee.toPlainText(), ui.b1txte.toPlainText(), ui.b1urle.toPlainText(), ui.b2txte.toPlainText(), ui.b2urle.toPlainText()))

def refresh_asset():
  with open(os.path.join(current_dir, 'Database.json'), 'r+') as db:
    data = json.load(db)
    firstrun = data[0]
    rpcasset = data[1]
    presence = data[2]
    userdata = data[3]
    AppID = data[4]
    rpcasset["AD"] = json.loads(requests.get(f'https://discordapp.com/api/oauth2/applications/{AppID["AppID"]}/assets').text)
    ls = [firstrun, rpcasset, presence, userdata, AppID]
    db.seek(0)
    db.write(json.dumps(ls))
    db.truncate()


# Test for first run and setup data
with open(os.path.join(current_dir, "Database.json"), "r+") as db:
  refresh_asset()
  data = json.load(db)
  firstrun = data[0]
  rpcasset = data[1]
  presence = data[2]
  userdata = data[3]
  AppID = data[4]["AppID"]
  username = userdata["UD"][0]["name"]
  user_tag = userdata["UD"][0]["tag"]
  ui.update_appid_label(AppID)
  if firstrun["FR"] == 1:
    msg("EndyPresence - Authorization", "Check your browser to authorize")
    webbrowser.open("http://127.0.0.1:3032")
  else:
    ui.update(userdata["UD"][0]["name"], userdata["UD"][0]["tag"], userdata["UD"][0]["pfp_hash"], userdata["UD"][0]["user_id"])
  ui.load_presence()


# Initialize Discord RPC
RPC = Presence(AppID)
try:
  RPC.connect()
  update_rpc(str(ui.limge.currentText()), str(ui.simge.currentText()), ui.ltxte.toPlainText(), ui.stxte.toPlainText(),
             ui.detailse.toPlainText(), ui.statee.toPlainText(), ui.b1txte.toPlainText(), ui.b1urle.toPlainText(),
             ui.b2txte.toPlainText(), ui.b2urle.toPlainText())
except:
  msg("EndyPresence - Connection Error", "Can't connect to Discord RPC. Check if Discord is currently running.")


MainWindow.show()
sys.exit(app.exec())
