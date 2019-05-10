$(document).ready(function(){
    $('#edit-name-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/milestone/' + uid + '/editname/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                name:$("#new-milestone-name").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(){
                var titleDisplay = document.getElementsByClassName("assessment-title")[0];
                var titleEdit = document.getElementById("edit-name");
                titleDisplay.innerHTML = $("#new-milestone-name").val();
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
    $('#add-task-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/milestone/' + uid + '/addreqtask/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                task_id:$("#new-req-task").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(data){
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

                changeStatus(data.status_img);
                console.log("Success!");
            },
            error: function(request, status, error) { 
                console.log("Fail!");
                alert("Error: " + request.responseText);
            }
        });
    });
});

function editName() {
    var titleDisplay = document.getElementsByClassName("assessment-title")[0];
    var titleEdit = document.getElementById("edit-name");
    document.getElementById("new-milestone-name").value = titleDisplay.innerHTML;
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
    var url_ = '/milestone/' + uid + '/deletereqtask/';
    $.ajax({
        type:'POST',
        url: url_,
        data:{
            task_id: t_id,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
        },
        success:function(data){
            var taskDisplay = document.getElementById(t_id);
            var taskTag = taskDisplay.querySelectorAll('span')[0];
            var taskName = taskTag.innerHTML;
            taskDisplay.parentNode.removeChild(taskDisplay);

            var newoption = document.createElement("option");
            newoption.setAttribute("id","option-" + t_id);
            newoption.value = t_id;
            newoption.innerHTML = taskName;
            document.getElementById("new-req-task").appendChild(newoption);
            
            changeStatus(data.status_img);
            console.log("Success!");
        },
        error: function(request, status, error) { 
            console.log("Fail!");
            alert("Error: " + request.responseText);
        }
    });
}

function changeStatus(img_url){
    var status_img = document.getElementById("status")
    status_img.setAttribute("src", "/static/" + img_url);
}

function deleteMilestone(){
    var uid = $("#uid").html();
    var url_ = '/milestone/' + uid + '/delete/';
    proceed = confirm("Are you sure you want to delete this milestone?");
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