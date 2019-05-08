$(document).ready(function(){
    $('#edit-name-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/task/' + uid + '/editname/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                name:$("#new-task-name").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(){
                var titleDisplay = document.getElementsByClassName("assessment-title")[0];
                var titleEdit = document.getElementById("edit-name");
                titleDisplay.innerHTML = $("#new-task-name").val();
                titleDisplay.style.display = "block";
                titleEdit.style.display = "none";
                console.log("Success!");
            },
            error: function(request, status, error) { 
                console.log("Fail!");
                alert("Error: " + request.responseText);
            }
        });
    });
    $('#edit-description-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/task/' + uid + '/editdescription/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                description:$("#new-description").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(){
                var descDisplay = document.getElementById("description");
                var descEdit = document.getElementById("edit-description");
                descDisplay.innerHTML = $("#new-description").val();
                descDisplay.style.display = "block";
                descEdit.style.display = "none";
                console.log("Success!");
            },
            error: function(request, status, error) { 
                console.log("Fail!");
                alert("Error: " + request.responseText);
            }
        });
    });
    $('#edit-duration-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/task/' + uid + '/editduration/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                duration:$("#new-duration").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(){
                var durDisplay = document.getElementById("duration");
                var durEdit = document.getElementById("edit-duration");
                durDisplay.innerHTML = $("#new-duration").val() + " days";
                durDisplay.style.display = "block";
                durEdit.style.display = "none";
                console.log("Success!");
            },
            error: function(request, status, error) { 
                console.log("Fail!");
                alert("Error: " + request.responseText);
            }
        });
    });
    $('#add-task-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/task/' + uid + '/addreqtask/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                task_id:$("#new-req-task").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(){
                var newtask = document.createElement("div");
                newtask.setAttribute("class", "ib-text mibt-item");
                newtask.setAttribute("id", $("#new-req-task").val());
                var newtask_a = document.createElement("a");
                newtask_a.setAttribute("href", "/task/" + $("#new-req-task").val());
                var newtask_span = document.createElement("span");
                newtask_span.setAttribute("class", "ul-hover");
                newtask_span.innerHTML = $("#new-req-task :selected").text();
                newtask_a.appendChild(newtask_span);
                var newtask_img = document.createElement("img");
                newtask_img.setAttribute("src", "/static/img/icon_delete.png");
                newtask_img.setAttribute("alt", "icon");
                newtask_img.setAttribute("class", "delete-icon");
                newtask_img.setAttribute("onclick", "deleteReqTask('" + $("#new-req-task").val() + "')");
                newtask.appendChild(newtask_a);
                newtask.appendChild(newtask_img);
                var list = document.getElementById("reqtask-list");
                var addLink = document.getElementById("add-task-link");
                list.insertBefore(newtask,addLink);

                var taskOption = document.getElementById("option-" + $("#new-req-task").val());
                taskOption.parentNode.removeChild(taskOption);
                var addForm = document.getElementById("add-task");
                addLink.style.display = "block";
                addForm.style.display = "none";
                console.log("Success!");
            },
            error: function(request, status, error) { 
                console.log("Fail!");
                alert("Error: " + request.responseText);
            }
        });
    });
    $('#add-activity-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/task/' + uid + '/addactivity/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                name:$("#new-activity-name").val(),
                type:$("#act-type").val(),
                target:$("#new-activity-target").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(data){
                var id = data.id;
                var newact_a = document.createElement("a");
                newact_a.setAttribute("href", "/activity/" + id);
                var newact_div = document.createElement("div");
                newact_div.setAttribute("class", "assessment-table-entry");
                newact_div.innerHTML = data.name;
                var type_div = document.createElement("div");
                type_div.setAttribute("class", "assessment-type");
                type_div.setAttribute("style", "margin-left: 5px;");
                type_div.innerHTML = data.type;
                var space_div = document.createElement("div");
                space_div.setAttribute("style", "flex: 1 1 auto;");
                var bar_div = document.createElement("div");
                bar_div.setAttribute("class", "progress-bar pb-infobox");
                var barfill_div = document.createElement("div");
                barfill_div.setAttribute("class", "progress-bar-fill");
                bar_div.appendChild(barfill_div);
                newact_div.appendChild(type_div);
                newact_div.appendChild(space_div);
                newact_div.appendChild(bar_div);
                newact_a.appendChild(newact_div);
                document.getElementById("activities-list").appendChild(newact_a);
                document.getElementById("progress").setAttribute("style", "width:" + data.task_progress + "%;");
                document.getElementById("progress-txt").innerHTML = data.task_progress + "%";

                cancelAddActivity();
                console.log("Success!");
            },
            error: function(request, status, error) { 
                console.log("Fail!");
                alert(request.responseText);
            }
        });
    });
    $('#add-note-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/task/' + uid + '/addnote/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                note:$("#new-note-text").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(data){
                var id = data.id;
                var newnote_div = document.createElement("div");
                newnote_div.setAttribute("class", "note-entry");
                newnote_div.setAttribute("id", id);
                var newnote_header = document.createElement("div");
                newnote_header.setAttribute("class", "note-header");
                var newnote_date = document.createElement("div");
                newnote_date.innerHTML = data.date;
                var newnote_img = document.createElement("img");
                newnote_img.setAttribute("src", "/static/img/icon_delete.png");
                newnote_img.setAttribute("alt", "icon");
                newnote_img.setAttribute("class", "delete-icon");
                newnote_img.setAttribute("onclick", "deleteNote('" + id + "')");
                var newnote_text = document.createElement("div");
                newnote_text.innerHTML = data.note;
                
                newnote_header.appendChild(newnote_date);
                newnote_header.appendChild(newnote_img);
                newnote_div.appendChild(newnote_header);
                newnote_div.appendChild(newnote_text);
                document.getElementById("notes-list").appendChild(newnote_div);
                cancelAddNote();
                console.log("Success!");
            },
            error: function(request, status, error) { 
                console.log("Fail!");
                alert(request.responseText);
            }
        });
    });
});

function editName() {
    var titleDisplay = document.getElementsByClassName("assessment-title")[0];
    var titleEdit = document.getElementById("edit-name");
    document.getElementById("new-task-name").value = titleDisplay.innerHTML;
    titleDisplay.style.display = "none";
    titleEdit.style.display = "block";
}

function cancelName(){
    var titleDisplay = document.getElementsByClassName("assessment-title")[0];
    var titleEdit = document.getElementById("edit-name");
    titleDisplay.style.display = "block";
    titleEdit.style.display = "none";
    console.log("cancelled!")
}

function editDescription() {
    var descDisplay = document.getElementById("description");
    var descEdit = document.getElementById("edit-description");
    document.getElementById("new-description").value = descDisplay.innerHTML;
    descDisplay.style.display = "none";
    descEdit.style.display = "block";
}

function cancelDescription(){
    var descDisplay = document.getElementById("description");
    var descEdit = document.getElementById("edit-description");
    descDisplay.style.display = "block";
    descEdit.style.display = "none";
    console.log("cancelled!")
}

function editDuration() {
    var durDisplay = document.getElementById("duration");
    var durEdit = document.getElementById("edit-duration");
    document.getElementById("new-duration").value = durDisplay.innerHTML.replace(' days','');;
    durDisplay.style.display = "none";
    durEdit.style.display = "block";
}

function cancelDuration(){
    var durDisplay = document.getElementById("duration");
    var durEdit = document.getElementById("edit-duration");
    durDisplay.style.display = "block";
    durEdit.style.display = "none";
    console.log("cancelled!")
}

function addReqTask() {
    var addLink = document.getElementById("add-task-link");
    var addForm = document.getElementById("add-task");
    //document.getElementById("new-duration").value = durDisplay.innerHTML.replace(' days','');;
    addLink.style.display = "none";
    addForm.style.display = "block";
}

function cancelAddTask() {
    var addLink = document.getElementById("add-task-link");
    var addForm = document.getElementById("add-task");
    addLink.style.display = "block";
    addForm.style.display = "none";
}

function deleteReqTask(t_id){
    event.preventDefault();
    var uid = $("#uid").html();
    var url_ = '/task/' + uid + '/deletereqtask/';
    $.ajax({
        type:'POST',
        url: url_,
        data:{
            task_id: t_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success:function(){
            var taskDisplay = document.getElementById(t_id);
            var taskTag = taskDisplay.querySelectorAll('span')[0];
            var taskName = taskTag.innerHTML;
            taskDisplay.parentNode.removeChild(taskDisplay);

            var newoption = document.createElement("option");
            newoption.setAttribute("id","option-" + t_id);
            newoption.value = t_id;
            newoption.innerHTML = taskName;
            document.getElementById("new-req-task").appendChild(newoption);
            console.log("Success!");
        },
        error: function(request, status, error) { 
            console.log("Fail!");
            alert("Error: " + request.responseText);
        }
    });
}

function setUnits(){
    var tag = document.getElementById("act-type").value;
    var type_units = [{tag: 'RE', units: 'pages'},
                 {tag: 'WR', units: 'words'},
                 {tag: 'ST', units: 'hours'},
                 {tag: 'PR', units: 'requirements'}];
    var l = type_units.length;
    for (var i = 0; i < l; i++) {
        if(tag==type_units[i].tag){
            document.getElementById("units").innerHTML = type_units[i].units;
        }
    }
}

function addActivity(){
    var addAct = document.getElementById("new-activity");
    addAct.style.display = "block";
}

function cancelAddActivity(){
    var addAct = document.getElementById("new-activity");
    document.getElementById("new-activity-name").value="";
    document.getElementById("new-activity-target").value="";
    addAct.style.display = "none";
}

function addNote(){
    var addNote = document.getElementById("new-note");
    addNote.style.display = "block";
}

function cancelAddNote(){
    var addNote = document.getElementById("new-note");
    document.getElementById("new-note-text").value="";
    addNote.style.display = "none";
}

function deleteNote(n_id){
    event.preventDefault();
    var uid = $("#uid").html();
    var url_ = '/task/' + uid + '/deletenote/';
    proceed = confirm("Are you sure you want to delete the note?");
    if(!proceed) return;
    $.ajax({
        type:'POST',
        url: url_,
        data:{
            note_id: n_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success:function(){
            var noteDisplay = document.getElementById(n_id);
            noteDisplay.parentNode.removeChild(noteDisplay);
            console.log("Success!");
        },
        error: function(request, status, error) { 
            console.log("Fail!");
            alert("Error: " + request.responseText);
        }
    });
}
function deleteTask(){
    var uid = $("#uid").html();
    var url_ = '/task/' + uid + '/delete/';
    proceed = confirm("Deleting a task is irreversible."
    + " All activities that are solely associated with this task will also be deleted."
    + "\nAre you sure you want to delete the task?");
    if(!proceed) return;
    $.ajax({
        type:'POST',
        url: url_,
        data:{
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success:function(data){
            window.location = data.url;
        },
        error: function(request, status, error) { 
            console.log("Fail!");
            alert("Error: " + request.responseText);
        }
    });
}