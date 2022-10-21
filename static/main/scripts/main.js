

async function setTime() {
    url = 'http://bots.sumjest.ru/api/getbots'
    // Default options are marked with *
    console.log(url)
    const response = await fetch(url, {
      method: 'GET', // *GET, POST, PUT, DELETE, etc.
      mode: 'cors', // no-cors, *cors, same-origin
    });
    await response.json().then((data) => {
       if (data.ok){
            for (let i = 0; i < data.result.length; i += 1)
            {
              document.getElementById("name" + i).textContent = data.result[i].name;
              document.getElementById("status" + i).textContent = data.result[i].status;
              document.getElementById("last_update" + i).textContent = (new Date(data.result[i].last_update* 1000)).toLocaleString();
            }
       }else{
          document.getElementById("error").textContent = data.reason
       }
    });
  }
  
async function onstop(data)
{
  bot_name = document.getElementById("name" + data).textContent
  url = 'http://bots.sumjest.ru/api/createtask?bot_name=' +  bot_name
  // Default options are marked with *
  console.log(JSON.stringify({task: 'stop'}));
  const response = await fetch(url, {
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
          alert("Запрос отправлен")
     }else{
        document.getElementById("error").textContent = data.reason
     }
  });
}

async function onstart(data)
{
  bot_name = document.getElementById("name" + data).textContent
  url = 'http://bots.sumjest.ru/api/createtask?bot_name=' +  bot_name
  // Default options are marked with *
  console.log(JSON.stringify({task: 'start'}));
  const response = await fetch(url, {
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
          alert("Запрос отправлен")
     }else{
        document.getElementById("error").textContent = data.reason
     }
  });
}

async function ondebug(data)
{
  bot_name = document.getElementById("name" + data).textContent
  url = 'http://bots.sumjest.ru/api/createtask?bot_name=' +  bot_name
  // Default options are marked with *
  console.log(JSON.stringify({task: 'debug_on'}));
  const response = await fetch(url, {
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
          alert("Запрос отправлен")
     }else{
        document.getElementById("error").textContent = data.reason
     }
  });
}

async function offdebug(data)
{
  bot_name = document.getElementById("name" + data).textContent
  url = 'http://bots.sumjest.ru/api/createtask?bot_name=' +  bot_name
  // Default options are marked with *
  console.log(JSON.stringify({task: 'debug_off'}));
  const response = await fetch(url, {
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
          alert("Запрос отправлен")
     }else{
        document.getElementById("error").textContent = data.reason
     }
  });
}

var t = setInterval(setTime, 1000);
