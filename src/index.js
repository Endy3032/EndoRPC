const DiscordRPC = require("discord-rpc")
const { app, BrowserWindow, ipcMain, shell } = require("electron")
const path = require("path")

let mainWindow

function createWindow() {
  mainWindow = new BrowserWindow({
    webPreferences: { nodeIntegration: true, preload: path.join(__dirname, "preload.js") },
    title: "EndyRPC",
    transparent: true,
    fullscreenable: false,
    autoHideMenuBar: true,
    vibrancy: "fullscreen-ui",
    titleBarStyle: "hiddenInset",
    width: 1120,
    height: 930,
    minWidth: 1120,
    minHeight: 930
  })

  mainWindow.loadFile("src/index.html")

  mainWindow.on("closed", () => {
    mainWindow = null
  })

  mainWindow.webContents.setWindowOpenHandler((link) => {
    shell.openExternal(link.url)
    return { action: "deny" }
  })
}

app.whenReady().then(createWindow)

app.on("activate", () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit()
  }
})

const appId = "799634564875681792"
DiscordRPC.register(appId)
const rpc = new DiscordRPC.Client({ transport: "ipc" })

rpc.on("ready", () => {
  console.log("Ready")
})

ipcMain.on("updateRPC", (event, arg) => {
  rpc.setActivity(arg)
  event.returnValue = "success"
})

ipcMain.on("updateAppID", (event, arg) => {
  DiscordRPC.register(arg)
  event.returnValue = "success"
})

rpc.login({ clientId: appId }).catch(console.error)