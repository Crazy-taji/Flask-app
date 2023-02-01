
    var socket = io();
    var stats = document.getElementById("stats");


    function inform(text){
        console.log(text)
        stats.innerHTML = text
    }
    socket.on("connect", ()=>{
        console.log("connected");
        stats.innerHTML = "Connected To Server"
    })
    socket.on("response", (url) =>{
        inform(url);
    })

    //{{ url_for('video') }}
    var txt = document.getElementById("count");
    var camURL = document.getElementById("camURL");
    setInterval(function() {
    check(txt,"C-check", "/send_text", "Not Counting Right Now" )
    console.log(1)
    }, 100);




    function access(){
        camURL = document.getElementById("camURL").value;
        socket.emit("url", camURL)
    }

    function Turn(value){
        socket.emit("cam", 1);
        let turnText = document.getElementById("camTurn")
        if(value == 1){turnText.value = 0; turnText.innerHTML = ("Turn On Camera"); inform("Camera Turn Off Request Was Sent")}
        if(value == 0){turnText.value = 1; turnText.innerHTML = ("Turn Off Camera"); inform("Camera Turn On Request Was Sent")}


    }
    function Process(num){
        socket.emit("model", num)
        console.log(num)
    }


    function check (OutputID,InputID, link, elseVal ){

        if(document.getElementById(InputID).checked == true){
            fetch(link)
            .then(response => {
                response.text().then(t => OutputID.innerHTML = t)
            });
        }
        else{
            OutputID.innerHTML = elseVal;
        }
    }

