function userAction(button,action) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", `/${action}`, true);
    xhttp.setRequestHeader("Content-type", "application/json");
    xhttp.send(`{"macro":"${button}"}`);
    xhttp.onreadystatechange = function() { 
        if (xhttp.readyState == 4){
          if (xhttp.status == 204){
            // console.log(action, button, document.getElementById(button).style.backgroundColor);
            if  (action=="hold"){
              document.getElementById(button).classList.toggle("active");
            };
            if (action=="release") {
              document.getElementById(button).classList.toggle("active");
            }; 
            if (action=="click"){ 
              document.getElementById(button).classList.toggle("active");
              setTimeout(function(){document.getElementById(button).classList.toggle("active");},50);
            };
            if (action=="releaseAll"){
              var active_buttons = document.getElementsByClassName("active")  
              for (var i=0; i<active_buttons.length; i++) {
                active_buttons[i].classList.remove("active");
              };
              document.getElementById(button).style.backgroundColor="";
            };
            if (action=="lock"){  
              document.getElementById(button).classList.toggle("active");
            };
          };
        };
      };
}

function loadColors() {
  console.log("Loading colors")
  for (let item of document.getElementsByClassName("grid-item")){
    item.style.backgroundColor="green";
  }
}
