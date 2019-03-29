
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