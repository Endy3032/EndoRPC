/* eslint-disable no-unused-vars */
active = false

function toggleCheckmark() {
  if (active) {return}
  active = true

  checkmark = document.querySelector(".checkmark")
  checkmark.classList.toggle("on")
  thumb = document.querySelector(".checkmark .thumb")
  elapsed = document.querySelector(".elapsed")
  elapsed.classList.toggle("hide")
  
  if (!Object.values(checkmark.classList).includes("on")) {
    thumb.classList.toggle("Rleft")
    thumb.classList.toggle("Rright")
    setTimeout(function() {thumb.classList.toggle("Lleft"); thumb.classList.toggle("Rleft"); active = false}, 150)
  } else {
    thumb.classList.toggle("Lright")
    thumb.classList.toggle("Lleft")
    setTimeout(function() {thumb.classList.toggle("Rright"); thumb.classList.toggle("Lright"); active = false}, 150)
  }
}

function updateRPC() {
  startTimestamp = document.querySelector(".on") ? new Date().getTime() : null
  buttons = []
  b1txt = document.querySelector("#b1txt").value
  b1url = document.querySelector("#b1url").value
  b2txt = document.querySelector("#b2txt").value
  b2url = document.querySelector("#b2url").value
  if (b1txt.length > 0 && b1url.length > 0) {
    b1url = b1url.startsWith("https://") || b1url.startsWith("http://") ? b1url : "https://" + b1url
    buttons.push({ label: b1txt, url: b1url })
  }
  
  if (b2txt.length > 0 && b2url.length > 0) {
    b2url = b2url.startsWith("https://") || b2url.startsWith("http://") ? b2url : "https://" + b2url
    buttons.push({ label: b2txt, url: b2url })
  }

  try {partySize = parseInt(document.querySelector("#size").value)} catch(e) {alert("Party Size must be an integer"); partySize = null}
  try {partyMax = parseInt(document.querySelector("#max").value)} catch(e) {alert("Party Max must be an integer"); partyMax = null}

  limg = document.querySelector("#limg")
  simg = document.querySelector("#simg")

  const rpcData = {
    details: document.querySelector("#details").value || null,
    state: document.querySelector("#state").value || null,
    startTimestamp: startTimestamp || null,
    largeImageKey: limg.options[limg.selectedIndex].text || null,
    largeImageText: document.querySelector("#ltxt").value || null,
    smallImageKey: simg.options[simg.selectedIndex].text || null,
    smallImageText: document.querySelector("#stxt").value || null,
    partySize: partySize,
    partyMax: partyMax,
    buttons: buttons.length > 0 ? buttons : null
  }

  window.EndyRPC.setPresence(rpcData)
}

function updateAppID() {
  window.EndyRPC.setAppID(document.querySelector("#appid").value)
}

function updateAssets(appid) {
  const request = new Request(`https://discordapp.com/api/oauth2/applications/${appid}/assets`, { method: "GET" })

  fetch(request)
    .then(response => response.json())
    .then(res => {
      images = []
      ids = []
      res.forEach(element => {
        images.push(element.name)
        ids.push(element.id)
      })
  
      limg = document.querySelector("#limg")
      simg = document.querySelector("#simg")
      limg.options.length = 0
      simg.options.length = 0
  
      for (i = 0; i  < images.length; i++) {
        limg[i] = new Option(images[i], ids[i])
        simg[i] = new Option(images[i], ids[i])
      }
    })
}

setInterval(function() {
  document.querySelector(".details").innerText = document.querySelector("#details").value
  if (document.querySelector("#size").value && document.querySelector("#max").value) {
    document.querySelector(".state").innerText = `${document.querySelector("#state").value} (${document.querySelector("#size").value} of ${document.querySelector("#max").value})`
  } else {
    document.querySelector(".state").innerText = document.querySelector("#state").value
  }
  document.querySelector(".btn1").innerText = document.querySelector("#b1txt").value || "Button 1"
  document.querySelector(".btn2").innerText = document.querySelector("#b2txt").value || "Button 2"

  limg = document.querySelector("#limg")
  document.querySelector(".limg").style.background = `url("https://cdn.discordapp.com/app-assets/${document.querySelector("#appid").value}/${limg.value}.png") center/cover`
  simg = document.querySelector("#simg")
  document.querySelector(".simg").style.background = `url("https://cdn.discordapp.com/app-assets/${document.querySelector("#appid").value}/${simg.value}.png"), #18191C`
  document.querySelector(".simg").style.backgroundSize = "cover"

  limglabel = document.querySelector(".limg p")
  simglabel = document.querySelector(".simg p")
  limglabel.innerText = document.querySelector("#ltxt").value
  simglabel.innerText = document.querySelector("#stxt").value

  if ((limglabel.innerText.length > 0 && Object.values(limglabel.classList).includes("hide")) || (limglabel.innerText.length == 0 && !Object.values(limglabel.classList).includes("hide"))) {
    limglabel.classList.toggle("hide")
  }

  if ((simglabel.innerText.length > 0 && Object.values(simglabel.classList).includes("hide")) || (simglabel.innerText.length == 0 && !Object.values(simglabel.classList).includes("hide"))) {
    simglabel.classList.toggle("hide")
  }
}, 1000)