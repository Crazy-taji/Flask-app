var txt = document.getElementById("count");
var show = document.getElementById("showing");
var camTxt = document.getElementById("cam");

setInterval(() => {

    check(txt,"C-check", "/send_text", "Not Counting Right Now" )

//    if(fetch("/video").response == null){
//    document.getElementById("image").src = "https://tanahair.indonesia.go.id/pupm/static/no_video.jpg";
//    }


    }, 200);

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

