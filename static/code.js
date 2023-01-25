
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
//    check(txt,"C-check", "/send_text", "Not Counting Right Now" )
//    }, 100)
    function access(){
        camURL = document.getElementById("camURL").value;
        socket.emit("url", camURL)
    }
    function Turn(){
        socket.emit("cam", 1)

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

