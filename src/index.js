const DiscordRPC = require("discord-rpc")
const { app, BrowserWindow, shell } = require("electron")
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
    width: 1080,
    height: 970,
    minWidth: 1080,
    minHeight: 970
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

app.whenReady().then(() => {
  createWindow()
})

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

const clientId = "799634564875681792"
DiscordRPC.register(clientId)
const rpc = new DiscordRPC.Client({ transport: "ipc" })

rpc.on("ready", () => {
  console.log("Ready")
  // setPresence(rpc, { details: "wwwwwoooooooooo" })
})

// try {
//   require("electron-reloader")(module, {
//     debug: true,
//     watchRenderer: true,
//     ignore: ["out", "node_modules", "src/Resources"],
//   })
// } catch (_) { console.log("Error") }    

// rpc.login({ clientId }).catch(console.error)