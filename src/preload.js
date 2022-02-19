const { contextBridge, ipcRenderer } = require("electron")

contextBridge.exposeInMainWorld("EndyRPC", {
  setPresence: (Activity) => {
    const { state, details, startTimestamp, largeImageKey, largeImageText, smallImageKey, smallImageText, partySize, partyMax, buttons } = Activity
    // if (buttons?.length > 2) return console.error("Too many buttons")
    data = {}
  
    if (state) data.state = state
    if (details) data.details = details
    if (startTimestamp) data.startTimestamp = startTimestamp
    // if (endTimestamp) data.endTimestamp = endTimestamp
    if (largeImageKey) data.largeImageKey = largeImageKey
    if (largeImageText) data.largeImageText = largeImageText
    if (smallImageKey) data.smallImageKey = smallImageKey
    if (smallImageText) data.smallImageText = smallImageText
    // if (partyId) data.partyId = partyId
    if (partySize) data.partySize = partySize
    if (partyMax) data.partyMax = partyMax
    if (buttons) data.buttons = buttons

    ipcRenderer.send("updateRPC", data)
  },

  setAppID: (appID) => {
    ipcRenderer.send("updateAppID", appID)
  }
})
