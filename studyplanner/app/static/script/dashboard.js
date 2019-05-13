$(document).ready(function(){
    $('#change-semester-form').on('submit', function(event){
        event.preventDefault();
        var url_ = '/api/changesemester';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                semester:$("#semester").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(data){
                console.log("Success!");
                url = '/deadlines/'
                window.location = url;
            },
            error: function(request, status, error) { 
                console.log("Fail!");
                alert(request.responseText);
            }
        });
    });
    $(document).on('click', function(e) {
        if (e.target.id != 'settings-menu' && e.target.id != 'settings-button'
        && e.target.id != 'set-img' /*&& e.target.id != 'hubinput-button'
        && e.target.id != 'change-button'*/) {
            $('#settings-menu').hide();
            console.log("hideee " + e.target.id)
        }
    });
});



window.onload = function(){
    $('#hubinput-button').tooltip({
        placement: 'top',
        title: 'Error! You must select a study profile file in JSON format.',
        trigger: 'manual'
    })
}

function uploadHubfile(){
    var fileinput = $('#hubfile-input');
    fileinput.change(e => {
        var file = e.target.files[0];
        if(file.type !== "application/json"){
            console.log('Wrong file format.');
            $('#hubinput-button').tooltip('show');
            setTimeout(()=>{$('#hubinput-button').tooltip('hide');}, 5000);
        }else{
            $('#hubinput-button').tooltip('hide');
            $('#upload-hubfile-form').submit();
        }
    });
    fileinput.click();
}

function changeSemester(){
    var CSdisplay = document.getElementById("change-semester");
    CSdisplay.style.display = "block";
}

function cancelChangeSemester(){
    var CSdisplay = document.getElementById("change-semester");
    CSdisplay.style.display = "none";
}

function openSettings(){
    var settingsMenu = document.getElementById("settings-menu");
    if(settingsMenu.style.display == "none")
        settingsMenu.style.display = "block";
    else settingsMenu.style.display = "none";
}