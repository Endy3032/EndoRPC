# import psutil as ps
from tkinter import *
from threading import Thread
from pypresence import Presence
from OAuthAuthenticator import Oauth
from tkinter import messagebox as msgbox
from flask import Flask, request, redirect
import io, json, os, requests, time, webbrowser
from PIL import Image, ImageTk, ImageDraw, ImageFilter
from urllib.request import urlopen, Request, urlretrieve, build_opener, install_opener

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
win.minsize(800, 475)
win.resizable(False, False)
win.config(bg = winbg)
win.iconphoto(False, PhotoImage(file = os.path.join('Assets', 'Endy.png')))

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
large_txt_def = 'EndyPresence v1.0'
small_img_def = 'idle'
small_img_def = 'Idle'
username = 'User'
user_tag = 'XXXX'
avt_hash = ''
state = 'Idling'

# Command
def gen_upd():
  webbrowser.open('http://127.0.0.1:5000')

def rpc_upd(l_img, s_img, state, l_txt = None, s_txt = None, buttons = None, details = None):
  RPC.update(
    large_image = l_img,
    large_text = l_txt,
    small_image = s_img,
    small_text = s_txt,
    state = state,
    buttons = buttons,
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

default_pfp = Image.open(os.path.join('Assets', 'basepfp.png'))
pic = ImageTk.PhotoImage(mask_circle(default_pfp, blurple, 0))

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

title.pack(pady = 5)
version.pack(pady = 5, side = LEFT, anchor = SW)
usr_id_L.grid(column = 0, row = 1, pady = 5, padx = 10)
usr_id_E.grid(column = 1, columnspan = 2, row = 1, pady = 5, padx = 10)
app_id_L.grid(column = 0, row = 0, pady = 5, padx = 10)
app_id_E.grid(column = 1, columnspan = 2, row = 0, pady = 5, padx = 10)
app_id_E.insert(0, '799634564875681792')
upd_btn.grid(column = 1, row = 2, pady = 5, padx = 10)
pfp.pack(pady = 20)
name.pack()

def update(uname, utag, ahash, uid):
  usr_id_E.delete(0, END)
  usr_id_E.insert(0, uid)
  pfp_url = f'https://cdn.discordapp.com/avatars/{uid}/{ahash}.png?size=512'
  path = os.path.join('Assets', 'dlpfp.png')
  urlretrieve(pfp_url, path)
  pimg = Image.open(os.path.join('Assets', 'dlpfp.png'))
  timg = ImageTk.PhotoImage(mask_circle(pimg, blurple, 0))
  pfp.configure(image = timg)
  pfp.image = timg
  name['text'] = f'{uname}#{utag}'

# Assets list
assets = ['asset one', 'asset two', 'asset three', 'asset four']
values = StringVar(win)
values.set(assets[0])

large_img_CB = OptionMenu(
  Widgets,
  values,
  *assets)
large_img_CB.config(width = 10, bg = dark_bl, font = ('Uni Sans', 15), fg = blurple)
large_img_CB['menu'].config(bg = winbg)
# large_img_CB.grid(row = 1)

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

win.protocol('WM_DELETE_WINDOW', end)
win.mainloop()