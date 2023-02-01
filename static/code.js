
    var socket = io();


    socket.on("connect", ()=>{
        console.log("connected");
    })
    socket.on("response", (url) =>{
    console.log(url);
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

    function Turn(){
        socket.emit("cam", 1)

    }
    function Process(num){
        socket.emit("model", num)
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

