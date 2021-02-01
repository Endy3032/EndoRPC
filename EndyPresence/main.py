import json, os, webbrowser
from tkinter import *
from threading import Thread
from tkinter import messagebox as msgbox
from urllib.request import urlopen, Request, urlretrieve, build_opener, install_opener
try:
  import requests
  from pypresence import Presence
  from flask import Flask, request, redirect
  from PIL import Image, ImageTk, ImageDraw, ImageFilter
except:
  os.system('pip install -r requirements.txt')
  msgbox.showinfo('EndyPresence', 'Succesfully installed dependencies! Please re-run the program.')
  exit(0)

class Oauth(object):
  client_id = '799634564875681792'
  client_secret = 'NLNhwnpsbkUjPgSAWheugxlNP0WA-FYb'
  scope = 'identify'
  redirect_uri = 'http://127.0.0.1:5000/login'
  discord_login_url = f'https://discord.com/api/oauth2/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&scope={scope}'
  discord_token_url = f'https://discord.com/api/oauth2/token'
  discord_api_url = f'https://discord.com/api/'

  @staticmethod
  def get_access_token(code):
    data = {
      'client_id': Oauth.client_id,
      'client_secret': Oauth.client_secret,
      'grant_type': 'authorization_code',
      'code': code,
      'redirect_uri': Oauth.redirect_uri,
      'scope': Oauth.scope
    }

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    access_token = requests.post(url = Oauth.discord_token_url, data = data, headers = headers)
    json = access_token.json()
    return json.get('access_token')

  @staticmethod
  def get_user_json(access_token):
    url = Oauth.discord_api_url + '/users/@me'

    headers = {
      "Authorization": f"Bearer {access_token}"
    }

    user_object = requests.get(url = url, headers = headers)
    user_json = user_object.json()
    return user_json
  
  @staticmethod
  def refresh_token(refresh_token):
    url = Oauth.discord_api_url + '/oauth2/token'

    data = {
      'client_id': Oauth.client_id,
      'client_secret': Oauth.client_secret,
      'grant_type': 'refresh_token',
      'refresh_token': refresh_token,
      'redirect_uri': Oauth.redirect_uri,
      'scope': 'identify'
    }

    headers = {
      'Content-Type': 'application/x-www-form-urlencoded'
    }

    refresh = requests.post(url = url, data = data, headers = headers)
    json = refresh.json()
    return json

with open('Config.json', 'r') as firstruntest:
  firstruntest = json.load(firstruntest)
  if firstruntest['FirstRun'] == '1':
    with open('AssetFile.json', 'w') as file: pass
    with open('UserData.json', 'w') as file: pass

opener = build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
install_opener(opener)

blurple = '#7289DA'
greyple = '#99AAB5'
dark_bl = '#2C2F33'
quitebl = '#23272A'
white = '#FFFFFF'
winbg = dark_bl #3B4252

# Tkinter App
# Window
win = Tk()
win.title("Endy's Discord Presence")
win.minsize(830, 550)
win.resizable(False, False)
win.config(bg = winbg)
win.iconphoto(False, PhotoImage(file = os.path.join('Assets', 'Images', 'Endy.png')))

# Frames & Canvases
RightPane = PanedWindow(orient = VERTICAL, borderwidth = 0, bg = winbg)
TitleFrame = Frame(win, bg = winbg)
Widgets = Frame(win, bg = winbg)
FooterFrame = Frame(win, bg = winbg)

Preview = Label(
  RightPane,
  text = 'Presence Preview',
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

# Variables
large_img_def = 'endy'
large_txt_def = 'EndyPresence v0.95'
small_img_def = 'idle'
small_img_def = 'Idle'
username = 'User'
user_tag = 'XXXX'
avt_hash = ''
state = 'Idling'

# Command
def gen_upd():
  webbrowser.open('http://127.0.0.1:5000')

def rpc_upd():
  l_img = limg.get()
  s_img = simg.get()
  state = state_E.get()
  details = details_E.get()
  buttons = []
  if len(btn1_txt_E.get()) != 0:
    btn1txt = btn1_txt_E.get()
    btn1url = btn1_url_E.get()
    buttons.append({"label": f"{btn1txt}", "url": f"{btn1url}"})
  if len(btn1_txt_E.get()) > 0:
    btn2txt = btn2_txt_E.get()
    btn2url = btn2_url_E.get()
    buttons.append({"label": f"{btn2txt}", "url": f"{btn2url}"}) if len(btn2txt) != 0 and len(btn2url) != 0 else None
  print(buttons)
  RPC.update(
    large_image = l_img,
    large_text = 'EndyPresence',
    small_image = s_img,
    small_text = 'v1.0',
    state = state,
    buttons = buttons if len(buttons) != 0 else None,
    details = details
  )

def end():
  try: RPC.close()
  finally: exit(0)

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

def mask_circle(pil_img, background_color, blur_radius, offset=0):
  background = Image.new(pil_img.mode, pil_img.size, background_color)

  offset = blur_radius * 2 + offset
  mask = Image.new("L", pil_img.size, 0)
  draw = ImageDraw.Draw(mask)
  draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
  mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

  result = pil_img.copy()
  result.putalpha(mask)
  composited = Image.composite(pil_img, background, mask)
  return composited.resize((125, 125))

def refresh():
  with open('AssetFile.json', 'w') as DiscordAssets:
    try:
      response = requests.get(f'https://discordapp.com/api/oauth2/applications/{AppID}/assets')
      DiscordAssets.write(response.text)
    except: msgbox.showerror('Error', 'Unable to retrieve assets data. Using currently saved assets data!')

roundPolygon(Canv, [10, 385, 385, 10], [0, 0, 250, 250], 7, width = 0, fill = blurple)
Canv.create_rectangle(10, 225, 385, 270, fill = '#6c82cf', width = 0)
roundPolygon(Canv, [10, 385, 385, 10], [225, 225, 390, 390], 5, width = 0, fill = '#6c82cf')

# Initialize
AppID = "799634564875681792"
RPC = Presence(AppID)
try: RPC.connect()
except: msgbox.showerror("Discord Connection Error", "Can't connect to Discord RPC service. Maybe check if Discord is running?")
RPC.update(
  state = "Initializing...", 
  large_image = 'initialize',
  large_text = 'EndyPresence v1.0')

RPC.update(
  state = 'Idling',
  details = 'Wow!',
  large_image = 'endy',
  large_text = 'EndyPresence v1.0',
  small_image = 'idle',
  small_text = 'Idle')

default_pfp = Image.open(os.path.join('Assets', 'Images', 'basepfp.png'))
pic = ImageTk.PhotoImage(mask_circle(default_pfp, blurple, 0))

# Assets list
refresh()
with open('AssetFile.json', 'r') as DiscordAssets:
  asset_id = []
  asset_name = []
  try:
    asset_json = json.load(DiscordAssets)
    for i in asset_json:
      asset_id.append(i['id'])
      asset_name.append(i['name'])
  except:
    msgbox.showerror('Error', 'No assets data found. Connect to the internet and hit "Refresh" to retrieve assets data')
    if len(asset_name) == 0:
      asset_name.append('None')

limg = StringVar(win)
try: endyimgindex = asset_name.index('endy')
except: endyimgindex = 0
limg.set(asset_name[endyimgindex])

simg = StringVar(win)
try: idleimgindex = asset_name.index('idle')
except: idleimgindex = 0
simg.set(asset_name[idleimgindex])

# GUI
title = Label(
  TitleFrame,
  text = "EndyPresence",
  font = ('Uni Sans', 30),
  fg = blurple,
  bg = winbg)
version = Label(
  FooterFrame,
  text = 'v1.0',
  font = ('Uni Sans', 18),
  fg = blurple,
  bg = winbg)
app_id_L = Label(
  Widgets,
  font = ('Uni Sans', 20),
  text = 'App ID',
  bg = winbg,
  fg = greyple)
app_id_E = Entry(
  Widgets,
  font = ('Varela Round', 20),
  bg = winbg,
  fg = greyple,
  justify = 'center',
  disabledbackground= winbg,
  highlightbackground = winbg)
usr_id_L = Label(
  Widgets,
  font = ('Uni Sans', 20),
  text = 'User ID',
  bg = winbg,
  fg = greyple)
usr_id_E = Entry(
  Widgets,
  font = ('Varela Round', 20),
  bg = winbg,
  fg = greyple,
  justify = 'center',
  highlightbackground = winbg)
upd_btn = Button(
  Widgets,
  text = 'Update',
  font = ('Uni Sans', 20),
  fg = blurple,
  bg = dark_bl,
  justify = 'center',
  command = gen_upd)
rpc_btn = Button(
  Widgets,
  text = 'Update Presence',
  font = ('Uni Sans', 20),
  fg = blurple,
  bg = dark_bl,
  justify = 'center',
  command = rpc_upd)
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
l_img_L = Label(
  Widgets,
  font = ('Uni Sans', 20),
  text = 'LImage',
  bg = winbg,
  fg = greyple)
l_img_OM = OptionMenu(
  Widgets,
  limg,
  *asset_name)
s_img_L = Label(
  Widgets,
  font = ('Uni Sans', 20),
  text = 'SImage',
  bg = winbg,
  fg = greyple)
s_img_OM = OptionMenu(
  Widgets,
  simg,
  *asset_name)
details_L = Label(
  Widgets,
  font = ('Uni Sans', 20),
  text = 'Details',
  bg = winbg,
  fg = greyple)
details_E = Entry(
  Widgets,
  font = ('Varela Round', 20),
  bg = winbg,
  fg = greyple,
  justify = 'center',
  highlightbackground = winbg)
state_L = Label(
  Widgets,
  font = ('Uni Sans', 20),
  text = 'State',
  bg = winbg,
  fg = greyple)
state_E = Entry(
  Widgets,
  font = ('Varela Round', 20),
  bg = winbg,
  fg = greyple,
  justify = 'center',
  highlightbackground = winbg)
btn1_txt_L = Label(
  Widgets,
  font = ('Whitney Semibold', 20),
  text = 'Button 1 Text',
  bg = winbg,
  fg = greyple)
btn1_txt_E = Entry(
  Widgets,
  font = ('Varela Round', 20),
  bg = winbg,
  fg = greyple,
  justify = 'center',
  highlightbackground = winbg)
btn1_url_L = Label(
  Widgets,
  font = ('Whitney Semibold', 20),
  text = 'Button 1 URL',
  bg = winbg,
  fg = greyple)
btn1_url_E = Entry(
  Widgets,
  font = ('Varela Round', 20),
  bg = winbg,
  fg = greyple,
  justify = 'center',
  highlightbackground = winbg)
btn2_txt_L = Label(
  Widgets,
  font = ('Whitney Semibold', 20),
  text = 'Button 2 Text',
  bg = winbg,
  fg = greyple)
btn2_txt_E = Entry(
  Widgets,
  font = ('Varela Round', 20),
  bg = winbg,
  fg = greyple,
  justify = 'center',
  highlightbackground = winbg)
btn2_url_L = Label(
  Widgets,
  justify = 'center',
  highlightbackground = winbg,
  font = ('Whitney Semibold', 20),
  text = 'Button 2 URL',
  bg = winbg,
  fg = greyple)
btn2_url_E = Entry(
  Widgets,
  font = ('Varela Round', 20),
  bg = winbg,
  fg = greyple,
  justify = 'center',
  highlightbackground = winbg)


title.pack(pady = 5)
version.pack(pady = 5, side = LEFT, anchor = SW)
usr_id_L.grid(column = 0, row = 1, pady = 5, padx = 10)
usr_id_E.grid(column = 1, columnspan = 2, row = 1, pady = 5, padx = 10)
app_id_L.grid(column = 0, row = 0, pady = 5, padx = 10)
app_id_E.grid(column = 1, columnspan = 2, row = 0, pady = 5, padx = 10)
app_id_E.insert(0, '799634564875681792')
app_id_E.config(state = DISABLED)
l_img_L.grid(column = 0, row = 2, pady = 5, padx = 10)
l_img_OM.config(width = 20, bg = winbg, font = ('Varela Round', 18), fg = blurple)
l_img_OM['menu'].config(bg = white)
l_img_OM.grid(column = 1, columnspan = 2, row = 2, pady = 5, padx = 10)
s_img_L.grid(column = 0, row = 3, pady = 5, padx = 10)
s_img_OM.config(width = 20, bg = winbg, font = ('Varela Round', 18), fg = blurple)
s_img_OM['menu'].config(bg = white)
s_img_OM.grid(column = 1, columnspan = 2, row = 3, pady = 5, padx = 10)
details_L.grid(column = 0, row = 4, pady = 5, padx = 10)
details_E.grid(column = 1, columnspan = 2, row = 4, pady = 5, padx = 10)
state_L.grid(column = 0, row = 5, pady = 5, padx = 10)
state_E.grid(column = 1, columnspan = 2, row = 5, pady = 5, padx = 10)
btn1_txt_L.grid(column = 0, row = 6, pady = 5, padx = 10)
btn1_txt_E.grid(column = 1, columnspan = 2, row = 6, pady = 5, padx = 10)
btn1_url_L.grid(column = 0, row = 7, pady = 5, padx = 10)
btn1_url_E.grid(column = 1, columnspan = 2, row = 7, pady = 5, padx = 10)
btn2_txt_L.grid(column = 0, row = 8, pady = 5, padx = 10)
btn2_txt_E.grid(column = 1, columnspan = 2, row = 8, pady = 5, padx = 10)
btn2_url_L.grid(column = 0, row = 9, pady = 5, padx = 10)
btn2_url_E.grid(column = 1, columnspan = 2, row = 9, pady = 5, padx = 10)
upd_btn.grid(column = 0, row = 10, pady = 5, padx = 10)
rpc_btn.grid(column = 2, row = 10, pady = 5, padx = 10)
pfp.pack(pady = 20)
name.pack()

def update(uname, utag, ahash, uid):
  usr_id_E.delete(0, END)
  usr_id_E.insert(0, uid)
  pfp_url = f'https://cdn.discordapp.com/avatars/{uid}/{ahash}.png?size=512'
  path = os.path.join('Assets', 'Images', 'dlpfp.png')
  urlretrieve(pfp_url, path)
  pimg = Image.open(path)
  timg = ImageTk.PhotoImage(mask_circle(pimg, blurple, 0))
  pfp.configure(image = timg)
  pfp.image = timg
  name['text'] = f'{uname}#{utag}'

# FlaskServer
# Initialize
app = Flask('Discord OAuthenticator')
def run(): app.run()
FlaskApp = Thread(target = run)
FlaskApp.setDaemon(True)

# Data
Data = {
  "username": "",
  "user_tag": "",
  "avt_hash": "",
  "id": ""}

# Website
@app.route('/', methods=['get'])
def index():
  return redirect(Oauth.discord_login_url)

@app.route('/login', methods=['get'])
def login():
  code = request.args.get('code')
  access_token = Oauth.get_access_token(code)
  user_json = Oauth.get_user_json(access_token)
  global username, user_tag, avt_hash, user_id
  username = Data['username'] = user_json['username']
  user_tag = Data['user_tag'] = user_json['discriminator']
  avt_hash = Data['avt_hash'] = user_json['avatar']
  user_id = Data['id'] = user_json['id']
  update(username, user_tag, avt_hash, user_id)
  try:
    return 'You can close this tab now!'
  finally:
    myJSON = json.dumps(Data)
    with open("UserData.json", "w") as jsfile: jsfile.write(myJSON)

FlaskApp.start()
with open('Config.json', 'r') as first:
  first = json.load(first)
  if first['FirstRun'] == '1':
    msgbox.showinfo('EndyPresence', 'Check your default browser for a new tab!')
    webbrowser.open('http://127.0.0.1:5000')
    output = json.dumps({"FirstRun": "0"})
    with open('Config.json', 'w') as first_w: first_w.write(output)
  else:
    with open('UserData.json', 'r') as file:
      user_data = json.load(file)
      username = user_data['username']
      user_tag = user_data['user_tag']
      avt_hash = user_data['avt_hash']
      user_id = user_data['id']
      update(username, user_tag, avt_hash, user_id)

refresh()
win.protocol('WM_DELETE_WINDOW', end)
win.mainloop()
