function login() {
  let username = document.querySelector("#username").value;
  let password = document.querySelector("#password").value;

    $.ajax({
        type: "POST",
        url: '/login',
        data: {
          login_info: JSON.stringify({username: username, password: password})
        },
        success: function(response){
            if(response=="False")
            {
                window.alert("Incorrect username or password")
                window.location.href = '/'
            }
            else{
                window.location.href = '/'
            }
        }
    })
}

function createUser()
{
  const username = document.querySelector("#username");
  const userInput = username.value;
  const password = document.querySelector("#password");
  const passInput = password.value;
    if(passInput=="" || userInput=="")
    {
        return "Failed";
    }
    $.ajax({
        type: "POST",
        url: '/createUser',
        data: {
          json_string: JSON.stringify({username: userInput, password: passInput})
        },
        success: function(response){

            if(response=="False")
            {
                window.alert("User ID already taken")
                window.location.href = '/'
                return "Failed"
            }
            else{
                window.location.href = '/profile'
            }
        }
    })
}

function createGroup()
{
  const username = document.querySelector("#username");
  const userInput = username.value;
  const password = document.querySelector("#password");
  const passInput = password.value;
    if(passInput=="" || userInput=="")
    {
        return "Failed";
    }
    $.ajax({
        type: "POST",
        url: '/createGroup',
        data: {
          json_string: JSON.stringify({username: userInput, password: passInput})
        },
        success: function(response){

            if(response=="False")
            {
                window.alert("Group ID already taken")
                window.location.href = '/'
                return "Failed"
            }
            else{
                window.location.href = '/group'
            }
        }
    })
}

function createNewEvent()
{
    const title = document.querySelector("#title").value;
    const timeFrom = document.querySelector("#from").value;
    const timeTo = document.querySelector("#to").value;
    const date = document.querySelector("#date").value;
    const address = document.querySelector("#address").value;
    $.ajax({
        type: "POST",
        url: '/createNewEvent',
        data: {
          json_string: JSON.stringify({title: title, timeFrom: timeFrom, timeTo: timeTo, date: date, address: address})
        },
        success: function(response){
            if(response=="False")
            {
                window.alert("Failed to create new event")
                window.location.href = '/'
                return "Failed"
            }
            else{
                window.location.href = '/'
            }
        }
    })
}

function subscribe() {
    const groupID = document.querySelector("#groupID").value;
    $.ajax({
        type: "POST",
        url: '/subscribe',
        data: {
          json_string: JSON.stringify({groupID: groupID})
        },
        success: function(response){
            if(response=="False")
            {
                window.alert("Failed to subscribe")
                window.location.href = '/'
                return "Failed"
            }
            else{
                window.location.href = '/'
            }
        }
    })
}

function setFreetime() {
    const freetime = document.querySelector("#freetime").value;
    $.ajax({
        type: "POST",
        url: '/setFreetime',
        data: {
          json_string: JSON.stringify({freetime: freetime})
        },
        success: function(response){
            if(response=="False")
            {
                window.alert("Failed to set free time")
                window.location.href = '/'
                return "Failed"
            }
            else{
                window.location.href = '/'
            }
        }
    })
}

function addTask() {
    const taskName = document.querySelector("#taskName").value;
    const taskDuration = document.querySelector("#taskDuration").value;
    $.ajax({
        type: "POST",
        url: '/addTask',
        data: {
          json_string: JSON.stringify({taskName: taskName, taskDuration: taskDuration})
        },
        success: function(response){
            if(response=="False")
            {
                window.alert("Failed to add task")
                window.location.href = '/'
                return "Failed"
            }
            else{
                window.location.href = '/'
            }
        }
    })
}

function fetchEvents() {
    $.ajax({
        type: "GET",
        url: '/fetchEvents',
        success: function (response) {
            newsfeed = document.querySelector("#newsfeed");
            var temp = document.getElementsByTagName("template")[0];
            for (let element of JSON.parse(response)) {
                var clone = temp.content.cloneNode(true);
                clone.querySelector(".group_name").innerHTML = "<b> " + element["groupID"] + "</b>";
                clone.querySelector(".event_info").innerHTML = element["info"];
                clone.querySelector(".going_btn").setAttribute('aria-pressed', element["going"]);
                clone.querySelector(".going_btn").setAttribute('id', element["eventID"]);
                newsfeed.appendChild(clone);
            }
        }
    });
}

window.onload = () => {
    if (window.location.pathname == '/profile') {
        fetchEvents();
    }
}
