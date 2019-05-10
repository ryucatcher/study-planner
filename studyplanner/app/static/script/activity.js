$(document).ready(function(){
    $('#edit-name-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/activity/' + uid + '/editname/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                name:$("#new-act-name").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(){
                var titleDisplay = document.getElementsByClassName("assessment-title")[0];
                var titleEdit = document.getElementById("edit-name");
                titleDisplay.innerHTML = $("#new-act-name").val();
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
    $('#edit-completed-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/activity/' + uid + '/editcompleted/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                completed:$("#new-completed").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(data){
                var compDisplay = document.getElementById("completed");
                var compEdit = document.getElementById("edit-completed");
                compDisplay.innerHTML = $("#new-completed").val();
                compDisplay.style.display = "block";
                compEdit.style.display = "none";

                document.getElementById("progress").setAttribute("style", "width:" + data.act_progress + "%;");
                document.getElementById("progress-txt").innerHTML = data.act_progress + "%";
                console.log("Success!");
            },
            error: function(request, status, error) { 
                console.log("Fail!");
                alert("Error: " + request.responseText);
            }
        });
    });
    $('#edit-target-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/activity/' + uid + '/edittarget/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                target:$("#new-target").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(data){
                var tarDisplay = document.getElementById("target");
                var tarUnits = document.getElementById("units");
                var tarEdit = document.getElementById("edit-target");
                tarDisplay.innerHTML = $("#new-target").val();
                var compDisplay = document.getElementById("completed");
                compDisplay.innerHTML = data.completed;
                
                tarDisplay.style.display = "block";
                tarUnits.style.display = "block";
                tarEdit.style.display = "none";

                document.getElementById("progress").setAttribute("style", "width:" + data.act_progress + "%;");
                document.getElementById("progress-txt").innerHTML = data.act_progress + "%";
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
        var url_ = '/activity/' + uid + '/addtask/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                task_id:$("#new-task").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(){
                var newtask = document.createElement("div");
                newtask.setAttribute("class", "ib-text mibt-item");
                newtask.setAttribute("id", $("#new-task").val());
                var newtask_a = document.createElement("a");
                newtask_a.setAttribute("href", "/task/" + $("#new-task").val());
                var newtask_span = document.createElement("span");
                newtask_span.setAttribute("class", "ul-hover");
                newtask_span.innerHTML = $("#new-task :selected").text();
                newtask_a.appendChild(newtask_span);
                var newtask_img = document.createElement("img");
                newtask_img.setAttribute("src", "/static/img/icon_delete.png");
                newtask_img.setAttribute("alt", "icon");
                newtask_img.setAttribute("class", "delete-icon");
                newtask_img.setAttribute("onclick", "deleteTask('" + $("#new-task").val() + "')");
                newtask.appendChild(newtask_a);
                newtask.appendChild(newtask_img);
                var list = document.getElementById("task-list");
                var addLink = document.getElementById("add-task-link");
                list.insertBefore(newtask,addLink);

                var taskOption = document.getElementById("option-" + $("#new-task").val());
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
    $('#add-note-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/activity/' + uid + '/addnote/';
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
    document.getElementById("new-act-name").value = titleDisplay.innerHTML;
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

function editCompleted() {
    var compDisplay = document.getElementById("completed");
    var compEdit = document.getElementById("edit-completed");
    document.getElementById("new-completed").value = compDisplay.innerHTML;
    compDisplay.style.display = "none";
    compEdit.style.display = "block";
}

function cancelCompleted(){
    var compDisplay = document.getElementById("completed");
    var compEdit = document.getElementById("edit-completed");
    compDisplay.style.display = "block";
    compEdit.style.display = "none";
    console.log("cancelled!")
}

function editTarget() {
    var tarDisplay = document.getElementById("target");
    var tarUnits = document.getElementById("units");
    var tarEdit = document.getElementById("edit-target");
    document.getElementById("new-target").value = tarDisplay.innerHTML;
    tarDisplay.style.display = "none";
    tarUnits.style.display = "none";
    tarEdit.style.display = "block";
}

function cancelTarget(){
    var tarDisplay = document.getElementById("target");
    var tarUnits = document.getElementById("units");
    var tarEdit = document.getElementById("edit-target");
    tarDisplay.style.display = "block";
    tarUnits.style.display = "block";
    tarEdit.style.display = "none";
    console.log("cancelled!")
}

function addTask() {
    var addLink = document.getElementById("add-task-link");
    var addForm = document.getElementById("add-task");
    addLink.style.display = "none";
    addForm.style.display = "block";
}

function cancelAddTask() {
    var addLink = document.getElementById("add-task-link");
    var addForm = document.getElementById("add-task");
    addLink.style.display = "block";
    addForm.style.display = "none";
}

function deleteTask(t_id){
    event.preventDefault();
    var uid = $("#uid").html();
    var url_ = '/activity/' + uid + '/deletetask/';
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
            document.getElementById("new-task").appendChild(newoption);
            console.log("Success!");
        },
        error: function(request, status, error) { 
            console.log("Fail!");
            alert("Error: " + request.responseText);
        }
    });
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
    var url_ = '/activity/' + uid + '/deletenote/';
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
function deleteActivity(){
    var uid = $("#uid").html();
    var url_ = '/activity/' + uid + '/delete/';
    proceed = confirm("Deleting an activity is irreversible."
    + " The activity will be deleted from all tasks it is associated with."
    + "\nAre you sure you want to delete the activity?");
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