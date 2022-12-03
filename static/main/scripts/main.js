const Badges = {ON: "success", OFF: "secondary", DEBUG_ON: "warning", DEBUG_OFF: "warning", NOT_AVAILABLE: "danger", RUNNING: "primary", STOPPING: "primary"}
var alert_iterator = 0;

async function fetchWithTimeout(resource, options = {}) {
  const { timeout = 5000 } = options;
  
  const controller = new AbortController();
  const id = setTimeout(() => controller.abort(), timeout);
  const response = await fetch(resource, {
    ...options,
    signal: controller.signal  
  });
  clearTimeout(id);
  return response;
}

function createAlert(text, color = "success")
{
  var alert = document.createElement("div")
  alert.innerHTML = text +`
  <button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>`
  alert.className = "alert alert-"+ color +" alert-dismissible fade show";
  alert.role = "alert";
  alert.id = "alert" + alert_iterator;
  var alert_block = document.getElementById("alert_block")
  alert_block.appendChild(alert)
  alert_iterator++;
  setTimeout((alertId) => $("#" + alertId).alert("close"), 5000, alert.id)
}

async function setTime() {
    url = 'http://bots.sumjest.ru/api/getbots'
    // Default options are marked with *
    console.log(url)
    const response = await fetchWithTimeout(url, {
      method: 'GET', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
      cache: 'no-store',
    });
    await response.json().then((data) => {
       if (data.ok){
            for (let i = 0; i < data.result.length; i += 1)
            {
              document.getElementById("bot_name" + i).textContent = data.result[i].name;
              var status = data.result[i].status.toString().replace('_',' ');
              var debug = data.result[i].debug;
              if (debug && document.getElementById('bot_debug_status' + i).hasAttribute('hidden'))
              {
                document.getElementById('bot_debug_status' + i).removeAttribute('hidden')
              }else if (!debug && !document.getElementById('bot_debug_status' + i).hasAttribute('hidden')){
                document.getElementById('bot_debug_status' + i).setAttribute('hidden', '');
              }
              document.getElementById("bot_status_label" + i).textContent = status;
              document.getElementById("bot_status_label" + i).className = "badge badge-" + Badges[data.result[i].status];
              document.getElementById("bot_last_update" + i).textContent = (new Date(data.result[i].last_update* 1000)).toLocaleString();
            }
       }else{
          document.getElementById("error").textContent = data.reason
       }
    });
  }
  
async function onstop(data)
{
  bot_name = document.getElementById("bot_name" + data).textContent
  url = 'http://bots.sumjest.ru/api/createtask?bot_name=' +  bot_name
  // Default options are marked with *
  console.log(JSON.stringify({task: 'stop'}));
  const response = await fetchWithTimeout(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify({task: 'stop'}) 
  });
  
  await response.json().then((data) => {
     if (data.ok){
          createAlert("Запрос отправлен!")
     }else{
        document.getElementById("error").textContent = data.reason
     }
  });
}

async function onstart(data)
{
  bot_name = document.getElementById("bot_name" + data).textContent
  url = 'http://bots.sumjest.ru/api/createtask?bot_name=' +  bot_name
  // Default options are marked with *
  console.log(JSON.stringify({task: 'start'}));
  const response = await fetchWithTimeout(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify({task: 'start'}) 
  });
  
  await response.json().then((data) => {
     if (data.ok){
          createAlert("Запрос отправлен!")
     }else{
        document.getElementById("error").textContent = data.reason
     }
  });
}

async function ondebug(data)
{
  bot_name = document.getElementById("bot_name" + data).textContent
  url = 'http://bots.sumjest.ru/api/createtask?bot_name=' +  bot_name
  // Default options are marked with *
  console.log(JSON.stringify({task: 'debug_on'}));
  const response = await fetchWithTimeout(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify({task: 'debug_on'}) 
  });
  
  await response.json().then((data) => {
     if (data.ok){
          createAlert("Запрос отправлен!")
     }else{
        document.getElementById("error").textContent = data.reason
     }
  });
}

async function offdebug(data)
{
  bot_name = document.getElementById("bot_name" + data).textContent
  url = 'http://bots.sumjest.ru/api/createtask?bot_name=' +  bot_name
  // Default options are marked with *
  console.log(JSON.stringify({task: 'debug_off'}));
  const response = await fetchWithTimeout(url, {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    mode: 'cors', // no-cors, *cors, same-origin
    headers: {
      'Content-Type': 'application/json'
      // 'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: JSON.stringify({task: 'debug_off'}) 
  });
  
  await response.json().then((data) => {
     if (data.ok){
          createAlert("Запрос отправлен!")
     }else{
        document.getElementById("error").textContent = data.reason
     }
  });
}

var t = setInterval(setTime, 1000);
