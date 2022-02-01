function userAction(button,action) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", `/${action}`, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(`{"macro":"${button}"}`);
    xhttp.onreadystatechange = function() { 
        if (xhttp.readyState == 4){
          if (xhttp.status == 204){
            console.log(action, button, document.getElementById(button).style.backgroundColor);
            if  (action=="hold"){
              document.getElementById(button).style.backgroundColor="red"; 
            }
            if (action=="release") {
              document.getElementById(button).style.backgroundColor="green";
            } 
            if (action=="click" || action=="releaseAll"){ 
              document.getElementById(button).style.backgroundColor="red";
              setTimeout(function(){document.getElementById(button).style.backgroundColor="green";},50);
            }
          }
        };
      };
}

function loadColors() {
  console.log("Loading colors")
  for (let item of document.getElementsByClassName("grid-item")){
    item.style.backgroundColor="green";
  }
}
