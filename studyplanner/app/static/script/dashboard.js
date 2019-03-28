

function uploadHubfile(){
    var fileinput = document.getElementById('hubfile-input');
    fileinput.onchange = e => {
        var file = e.target.files[0];
        if(file.type !== "application/json"){

        }
    };
    fileinput.click();
}