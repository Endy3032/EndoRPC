import json, os, webbrowser
from tkinter import *
from threading import Thread
from tkinter import messagebox as msgbox
from urllib.request import urlretrieve, build_opener, install_opener

try:
  import requests
  from pypresence import Presence
  from flask import Flask, request, redirect
  from PIL import Image, ImageTk, ImageDraw, ImageFilter
except:
  os.system('pip install -r requirements.txt')
  msgbox.showinfo('EndyPresence', 'Succesfully installed dependencies! Please re-run the program.')
  exit(0)

with open('Config.json', 'r') as firstruntest:
  firstruntest = json.load(firstruntest)
  if firstruntest['FirstRun'] == '1':
    with open('AssetFile.json', 'w') as file: pass
    with open('UserData.json', 'w') as file: pass
    with open('PresenceConfig.json', 'w') as file:
      PData = {'limg': 'endy', 'simg': 'idle', 'ltxt': 'EndyPresence', 'stxt': 'Idle', 'details': 'EndyPresence', 'state': 'v0.97', 'b1txt': '', 'b1url': '', 'b2txt': '', 'b2url': ''}
      file.write(json.dumps(PData))

class Oauth(object):
  scope = 'identify'
  client_id = '799634564875681792'
  client_secret = 'NLNhwnpsbkUjPgSAWheugxlNP0WA-FYb'
  redirect_uri = 'http://127.0.0.1:5000/login'
  discord_api_url = f'https://discord.com/api/'
  discord_token_url = f'https://discord.com/api/oauth2/token'
  discord_login_url = f'https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}'
  
  @staticmethod
  def get_access_token(code):
    data = {'client_id': Oauth.client_id,
            'client_secret': Oauth.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': Oauth.redirect_uri,
            'scope': Oauth.scope}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    access_token = requests.post(url = Oauth.discord_token_url, data = data, headers = headers)
    return access_token.json().get('access_token')

  @staticmethod
  def get_user_json(access_token):
    url = Oauth.discord_api_url + '/users/@me'
    headers = {"Authorization": f"Bearer {access_token}"}
    return requests.get(url = url, headers = headers).json()

  @staticmethod
  def refresh_token(refresh_token):
    url = Oauth.discord_api_url + '/oauth2/token'
    data = {'client_id': Oauth.client_id,
            'client_secret': Oauth.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'redirect_uri': Oauth.redirect_uri,
            'scope': 'identify'}
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(url = url, data = data, headers = headers).json()

opener = build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
install_opener(opener)

blurple, greyple, dark_bl, quitebl, white = '#7289DA', '#99AAB5', '#2C2F33', '#23272A', '#FFFFFF'
winbg = dark_bl #3B4252

# Tkinter App
# Window
win = Tk()
win.title("Endy's Discord Presence")
win.minsize(815, 600)
win.resizable(False, False)
win.config(bg = winbg)
win.iconphoto(False, PhotoImage(file = os.path.join('Assets', 'Images', 'Endy.png')))

# Frames & Canvas
RightPane = PanedWindow(orient = VERTICAL, borderwidth = 0, bg = winbg)
# BottomRightPane = PanedWindow(orient = VERTICAL, borderwidth = 0, bg = winbg)
TitleFrame = Frame(win, bg = winbg)
Widgets = Frame(win, bg = winbg)
FooterFrame = Frame(win, bg = winbg)

Preview = Label(
  RightPane,
  text = 'Preview Presence',
  font = ('Uni Sans', 30),
  justify = 'center',
  fg = blurple,
  bg = winbg,
  highlightthickness = 0,
  borderwidth = 0)

Canv = Canvas(
  RightPane,
  bg = winbg,
  highlightthickness = 0,
  borderwidth = 0)

RightPane.pack(fill = BOTH, expand = True, side = RIGHT)
TitleFrame.pack(side = TOP)
Widgets.pack()
FooterFrame.pack(side = BOTTOM)
RightPane.add(Preview, pady = 10)
RightPane.add(Canv)
# RightPane.add(BottomRightPane)

# Variables
username = 'User'
user_tag = 'XXXX'
avt_hash = ''
Data = {"username": "",
        "user_tag": "",
        "avt_hash": "",
        "id": ""}
Entries = []
OMS = []
PData = {'limg': '', 'simg': '', 'ltxt': '', 'stxt': '', 'details': '', 'state': '', 'b1txt': '', 'b1url': '', 'b2txt': '', 'b2url': ''}

# Command
def gen_upd(): webbrowser.open('http://127.0.0.1:5000')

def rpc_upd():
  if len(Entries[6].get()) != 0: buttons.append({"label": f"{Entries[6].get()}", "url": f"{Entries[7].get()}"})
  if len(Entries[8].get()) != 0: buttons.append({"label": f"{Entries[8].get()}", "url": f"{Entries[9].get()}"})
  RPC.update(large_image = limg.get(),
             small_image = simg.get(),
             details = Entries[4].get(),
             state = Entries[5].get(),
             buttons = buttons if len(buttons) != 0 else None,
             large_text = Entries[2].get(),
             small_text = Entries[3].get())
  buttons.clear()
  PData['limg'] = limg.get()
  PData['simg'] = simg.get()
  PData['ltxt'] = Entries[2].get()
  PData['stxt'] = Entries[3].get()
  PData['details'] = Entries[4].get()
  PData['state'] = Entries[5].get()
  PData['b1txt'] = Entries[6].get()
  PData['b1url'] = Entries[7].get()
  PData['b2txt'] = Entries[8].get()
  PData['b2url'] = Entries[9].get()
  with open('PresenceConfig.json', 'w') as PConfig:
    PConfig.write(json.dumps(PData))

def roundPolygon(canvas, x, y, sharpness, **kwargs):
  if sharpness < 2: sharpness = 2
  ratioMultiplier, ratioDividend, points = sharpness - 1, sharpness, []
  for i in range(len(x)):
    points.append(x[i])
    points.append(y[i])
    if i != (len(x) - 1):
      points.append((ratioMultiplier*x[i] + x[i + 1])/ratioDividend)
      points.append((ratioMultiplier*y[i] + y[i + 1])/ratioDividend)
      points.append((ratioMultiplier*x[i + 1] + x[i])/ratioDividend)
      points.append((ratioMultiplier*y[i + 1] + y[i])/ratioDividend)
    else:
      points.append((ratioMultiplier*x[i] + x[0])/ratioDividend)
      points.append((ratioMultiplier*y[i] + y[0])/ratioDividend)
      points.append((ratioMultiplier*x[0] + x[i])/ratioDividend)
      points.append((ratioMultiplier*y[0] + y[i])/ratioDividend)
      points.append(x[0])
      points.append(y[0])
  return canvas.create_polygon(points, **kwargs, smooth=TRUE)

roundPolygon(Canv, [10, 385, 385, 10], [0, 0, 250, 250], 7, width = 0, fill = blurple)
Canv.create_rectangle(10, 225, 385, 270, fill = '#6c82cf', width = 0)
roundPolygon(Canv, [10, 385, 385, 10], [225, 225, 390, 390], 5, width = 0, fill = '#6c82cf')

def mask_circle(pil_img, background_color, blur_radius, offset=0):
  background = Image.new(pil_img.mode, pil_img.size, background_color)
  offset = blur_radius * 2 + offset
  mask = Image.new("L", pil_img.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
  mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))
  result = pil_img.copy()
  result.putalpha(mask)
  return Image.composite(pil_img, background, mask).resize((125, 125))

def refresh():
  with open('AssetFile.json', 'w') as DiscordAssets:
    try: DiscordAssets.write(requests.get(f'https://discordapp.com/api/oauth2/applications/{AppID}/assets').text)
    except: msgbox.showerror('Error', 'Unable to retrieve assets data. Using currently saved assets data!')

# Init
AppID = "799634564875681792"
RPC = Presence(AppID)
try: RPC.connect()
except: msgbox.showerror("Connection Error", "Can't connect to Discord RPC. Check if Discord is currently running.")

default_pfp = Image.open(os.path.join('Assets', 'Images', 'basepfp.png'))
pic = ImageTk.PhotoImage(mask_circle(default_pfp, blurple, 0))

# GUI
refresh()
with open('AssetFile.json', 'r') as DiscordAssets:
  asset_id, asset_name = [], []
  try:
    asset_json = json.load(DiscordAssets)
    for i in asset_json:
      asset_id.append(i['id'])
      asset_name.append(i['name'])
  except:
    msgbox.showerror('Error', 'No assets data found. Connect to the internet and hit "Refresh" to retrieve assets data')
    if len(asset_name) == 0:
      asset_name.append('None')

limg, simg = StringVar(win), StringVar(win)
try:
  with open('PresenceConfig.json', 'r') as Pres:
    Pres = json.load(Pres)
    limg.set(asset_name[asset_name.index(Pres['limg'])])
    simg.set(asset_name[asset_name.index(Pres['simg'])])
except:
  limg.set(asset_name[0])
  simg.set(asset_name[0])

Labels = ['App ID', 'User ID', 'LargeIMG', 'SmallIMG', 'LargeTXT', 'SmallTXT', 'Details', 'State', 'B1 Text', 'B1 URL', 'B2 Text', 'B2 URL']
OM = [limg, simg]
BtnTexts = ['Update UserData', 'Update Presence']

for i in range(len(Labels)):
  lbl = Label(
    Widgets,
    font = ('Uni Sans', 20),
    text = Labels[i],
    bg = winbg,
    fg = greyple
  )
  lbl.grid(column = 0, row = i, pady = 5, padx = 7)

for i in range(len(Labels) - 2):
  ent = Entry(
    Widgets,
    font = ('Varela Round', 20),
    bg = winbg,
    fg = greyple,
    justify = 'center',
    highlightbackground = winbg,
    disabledbackground = winbg)
  if i > 1: ent.grid(column = 1, columnspan = 2, row = i + 2, pady = 5, padx = 8)
  else: ent.grid(column = 1, columnspan = 2, row = i, pady = 5, padx = 8)
  Entries.append(ent)

for i in range(2):
  om = OptionMenu(
    Widgets,
    limg if i == 0 else simg,
    *asset_name)
  om.config(width = 20, bg = winbg, font = ('Varela Round', 18), fg = blurple)
  om['menu'].config(bg = white)
  om.grid(column = 1, columnspan = 2, row = i + 2, pady = 5, padx = 10)
  OMS.append(om)

Entries[0].insert(0, '799634564875681792')
Entries[0].config(state = DISABLED)

title = Label(
  TitleFrame,
  text = "EndyPresence",
  font = ('Uni Sans', 30),
  fg = blurple,
  bg = winbg)
title.pack(pady = 5)

pfp = Label(
  Canv,
  image = pic,
  bg = blurple)
name = Label(
  Canv,
  text = f'{username}#{user_tag}',
  font = ('Whitney Semibold', 23),
  justify = 'center',
  fg = white,
  bg = blurple)
version = Label(
  RightPane,
  text = 'v0.97',
  font = ('Uni Sans', 18),
  fg = blurple,
  bg = winbg)

pfp.pack(pady = 20)
name.pack()
version.pack(pady = 5, side = BOTTOM, anchor = S)
for i in range(2):
  btn = Button(
    RightPane,
    text = BtnTexts[i],
    font = ('Uni Sans', 20),
    fg = blurple,
    bg = dark_bl,
    justify = 'center',
    command = gen_upd if i == 0 else rpc_upd
  )
  btn.pack(pady = 7, padx = 10, side = BOTTOM)

def update(uname, utag, ahash, uid):
  Entries[1].delete(0, END)
  Entries[1].insert(0, uid)
  pfp_url = f'https://cdn.discordapp.com/avatars/{uid}/{ahash}.png?size=512'
  path = os.path.join('Assets', 'Images', 'dlpfp.png')
  urlretrieve(pfp_url, path)
  timg = ImageTk.PhotoImage(mask_circle(Image.open(path), blurple, 0))
  pfp.configure(image = timg)
  pfp.image = timg
  name['text'] = f'{uname}#{utag}'

with open('PresenceConfig.json', 'r') as Pres:
  Pres = json.load(Pres)
  Entries[2].insert(0, Pres['ltxt'])
  Entries[3].insert(0, Pres['stxt'])
  Entries[4].insert(0, Pres['details'])
  Entries[5].insert(0, Pres['state'])
  Entries[6].insert(0, Pres['b1txt'])
  Entries[7].insert(0, Pres['b1url'])
  Entries[8].insert(0, Pres['b2txt'])
  Entries[9].insert(0, Pres['b2url'])
global buttons
buttons = []
if len(PData['b1txt']) != 0: buttons.append({"label": f"{PData['b1txt']}", "url": f"{PData['b1url']}"})
if len(PData['b2txt']) != 0: buttons.append({"label": f"{PData['b2txt']}", "url": f"{PData['b2url']}"})
rpc_upd()
buttons.clear()

# FlaskServer
app = Flask('Discord OAuthenticator')
def run(): app.run()
FlaskApp = Thread(target = run)
FlaskApp.setDaemon(True)

@app.route('/', methods=['get'])
def index(): return redirect(Oauth.discord_login_url)

@app.route('/login', methods=['get'])
def login():
  user_json = Oauth.get_user_json(Oauth.get_access_token(request.args.get('code')))
  global username, user_tag, avt_hash, user_id
  username = Data['username'] = user_json['username']
  user_tag = Data['user_tag'] = user_json['discriminator']
  avt_hash = Data['avt_hash'] = user_json['avatar']
  user_id = Data['id'] = user_json['id']
  update(username, user_tag, avt_hash, user_id)
  try:
    with open('Config.json', 'w') as first_w: first_w.write(json.dumps({"FirstRun": "0"}))
    return 'You can close this tab now!'
  finally:
    with open("UserData.json", "w") as jsfile: jsfile.write(json.dumps(Data))

FlaskApp.start()

with open('Config.json', 'r') as first:
  first = json.load(first)
  if first['FirstRun'] == '1':
    msgbox.showinfo('EndyPresence', 'Check your default browser for a new tab!')
    webbrowser.open('http://127.0.0.1:5000')
  else:
    with open('UserData.json', 'r') as file:
      user_data = json.load(file)
      username = user_data['username']
      user_tag = user_data['user_tag']
      avt_hash = user_data['avt_hash']
      user_id = user_data['id']
      update(username, user_tag, avt_hash, user_id)

refresh()
win.mainloop()
