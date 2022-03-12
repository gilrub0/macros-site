function userAction(button, action) {
    document.getElementById(button).classList.toggle("waiting_for_response")
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", `/${action}`, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(`{"macro":"${button}"}`);
    xhttp.onreadystatechange = function() {
        if (xhttp.readyState == 4) {
            if (xhttp.status == 204) {
                document.getElementById(button).classList.toggle("waiting_for_response")
                if (action == "hold") {
                    toggleActive(button);
                };
                if (action == "release") {
                    toggleActive(button);
                };
                if (action == "click") {
                    toggleActive(button);
                    setTimeout(function() { toggleActive(button); }, 50);
                };
                if (action == "releaseAll") {
                    var active_buttons = document.getElementsByClassName("active")
                    for (var i = 0; i < active_buttons.length; i++) {
                        active_buttons[i].classList.replace("active", "not_active");
                    };
                    document.getElementById(button).style.backgroundColor = "";
                };
                if (action == "lock") {
                    toggleActive(button);
                };
            };
        };
    };
}

function loadColors() {
    for (let item of document.getElementsByClassName("grid-item")) {
        item.classList.toggle("not_active")
    };
}

function toggleActive(btn) {

    document.getElementById(btn).classList.toggle("not_active");
    document.getElementById(btn).classList.toggle("active");

}

function remove_btn(button) {
    if (confirm('Are you sure?')) {
        console.log("remove " + button);
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", `/remove_btn`, true);
        xhttp.setRequestHeader("Content-type", "application/json");
        xhttp.send(`{"remove":"${button}"}`);
        xhttp.onreadystatechange = function() {
            if (xhttp.readyState == 4) {
                if (xhttp.status == 204) {
                    var row_to_remove=document.getElementById(`${button}`);
                    row_to_remove.remove();
                    // document.getElementById(`${button}`).parentNode.parentNode.removeChild(document.getElementById(`${button}`))
                };
            };
        };
    };
}

function add_btn(button, hold) {
    console.log(button, hold);
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", `/add_btn`, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(`{"${button}":{"name":"${button}","hold":${hold},"pressed": false}}`);
    setTimeout(function() { location.reload(); }, 50);
    
}