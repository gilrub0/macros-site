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
              // document.getElementById(button).style.backgroundColor="red"; 
              document.getElementById(button).classList.toggle("active");
            }
            if (action=="release") {
              // document.getElementById(button).style.backgroundColor="green";
              setTimeout(document.getElementById(button).classList.toggle("active"),15);
            } 
            if (action=="click"){ 
              document.getElementById(button).style.backgroundColor="red";
              setTimeout(function(){document.getElementById(button).style.backgroundColor="green";},50);
            }
            if (action=="releaseAll"){  
              document.getElementById(button).style.backgroundColor="";
            }
            if (action=="lock"){  
              document.getElementById(button).classList.toggle("active");
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

function chBackcolor(color) {
  document.body.style.background = color;
}