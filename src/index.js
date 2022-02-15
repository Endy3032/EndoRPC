const DiscordRPC = require("discord-rpc")
const { app, BrowserWindow } = require("electron")

let mainWindow

function createWindow() {
  mainWindow = new BrowserWindow({
    webPreferences: { nodeIntegration: true },
    title: "EndyRPC",
    transparent: true,
    fullscreenable: false,
    autoHideMenuBar: true,
    vibrancy: "fullscreen-ui",
    titleBarStyle: "hiddenInset",
  })

  mainWindow.loadFile("src/index.html")

  mainWindow.on("closed", () => {
    mainWindow = null
  })
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

/**
 * Set the Client's activity
 * @param {RPCClient} Client The RPC Client
 * @typedef Activity
 * @type {Object}
 * @property {String|null} state - The user's current party status
 * @property {String|null} details - What the player is currently doing
 * @property {Number|null} startTimestamp - Epoch seconds for game start - including will show time as "elapsed"
 * @property {Number|null} endTimestamp - Epoch seconds for game end - including will show time as "remaining"
 * @property {String|null} largeImageKey - Name of the uploaded image for the large profile artwork
 * @property {String|null} largeImageText - Tooltip for the largeImageKey
 * @property {String|null} smallImageKey - Name of the uploaded image for the small profile artwork
 * @property {String|null} smallImageText - Tooltip for the smallImageKey
 * @property {String|null} partyId - ID of the player's party, lobby, or group
 * @property {Number|null} partySize - Current size of the player's party, lobby, or group
 * @property {Number|null} partyMax - Maximum size of the player's party, lobby, or group
 * @property {Array.<Object>{label: String, url: String}=} buttons - An array of buttons to show on the Rich Presence
 * 
 */
function setPresence(Client, Activity) {
  const { state, details, startTimestamp, endTimestamp, largeImageKey, largeImageText, smallImageKey, smallImageText, partyId, partySize, partyMax, buttons } = Activity
  if (buttons?.length > 2) return console.error("Too many buttons")

  data = {}

  if (state) data.state = state
  if (details) data.details = details
  if (startTimestamp) data.startTimestamp = startTimestamp
  if (endTimestamp) data.endTimestamp = endTimestamp
  if (largeImageKey) data.largeImageKey = largeImageKey
  if (largeImageText) data.largeImageText = largeImageText
  if (smallImageKey) data.smallImageKey = smallImageKey
  if (smallImageText) data.smallImageText = smallImageText
  if (partyId) data.partyId = partyId
  if (partySize) data.partySize = partySize
  if (partyMax) data.partyMax = partyMax
  if (buttons) data.buttons = buttons

  Client.setActivity(data)
}

const clientId = "799634564875681792"
DiscordRPC.register(clientId)
const rpc = new DiscordRPC.Client({ transport: "ipc" })

rpc.on("ready", () => {
  console.log("Ready")
  // setPresence(rpc, { details: "wwwwwoooooooooo" })
})

try {
  require("electron-reloader")(module, {
    debug: true,
    watchRenderer: true
  })
} catch (_) { console.log("Error") }    

// rpc.login({ clientId }).catch(console.error)