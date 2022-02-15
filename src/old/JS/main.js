const { app, BrowserWindow } = require("electron")
const path = require("path")

const env = process.env.NODE_ENV || "development"

function createWindow () {
  const win = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: path.join(__dirname, "preload.js")
    },
    vibrancy: "dark"
  })

  win.loadFile("index.html")
}

app.whenReady().then(() => {
  createWindow()

  app.on("activate", () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow()
    }
  })
})

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    app.quit()
  }
})

if (env === "development") {
  try {
    require("electron-reloader")(module, {
      debug: true,
      watchRenderer: true
    })
  } catch (_) { console.log("Error") }    
}