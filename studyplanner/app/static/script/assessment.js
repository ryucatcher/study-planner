$(document).ready(function(){
    $('#edit-name-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/assessment/' + uid + '/editname/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                name:$("#new-assessment-name").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(){
                var titleDisplay = document.getElementsByClassName("assessment-title")[0];
                var titleEdit = document.getElementById("edit-name");
                titleDisplay.innerHTML = $("#new-assessment-name").val();
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
        var url_ = '/assessment/' + uid + '/editdescription/';
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
    $('#edit-startdate-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/assessment/' + uid + '/editstartdate/';
        $.ajax({
            type:'POST',
            url: url_,
            data:{
                startdate:$("#new-startdate").val(),
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success:function(){
                var dateDisplay = document.getElementById("startdate");
                var dateEdit = document.getElementById("edit-startdate");
                var newdate = formatDate(new Date($("#new-startdate").val()));
                dateDisplay.innerHTML = newdate;
                dateDisplay.style.display = "block";
                dateEdit.style.display = "none";
                console.log("Success!");
            },
            error: function(request, status, error) { 
                console.log("Fail!");
                alert("Error: " + request.responseText);
            }
        });
    });
    $('#edit-deadline-form').on('submit', function(event){
        event.preventDefault();
        var uid = $("#uid").html();
        var url_ = '/assessment/' + uid + '/editdeadline/';
        var date = new Date($("#new-deadline").val());
        var today = new Date();
        var proceed = true;
        if(date < today){
            proceed = confirm("You set the deadline to a past date. Are you sure you want to continue?");
        }
        if(proceed){
            $.ajax({
                type:'POST',
                url: url_,
                data:{
                    deadline:$("#new-deadline").val(),
                    csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
                },
                success:function(){
                    var dateDisplay = document.getElementById("deadline");
                    var dateEdit = document.getElementById("edit-deadline");
                    var newdate = formatDate(new Date($("#new-deadline").val()));
                    dateDisplay.innerHTML = newdate;
                    dateDisplay.style.display = "block";
                    dateEdit.style.display = "none";
                    console.log("Success!");
                },
                error: function(request, status, error) { 
                    console.log("Fail!");
                    alert("Error: " + request.responseText);
                }
            });
        }
    });
});

function editName() {
    var titleDisplay = document.getElementsByClassName("assessment-title")[0];
    var titleEdit = document.getElementById("edit-name");
    document.getElementById("new-assessment-name").value = titleDisplay.innerHTML;
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

function editStartDate() {
    var dateDisplay = document.getElementById("startdate");
    var dateEdit = document.getElementById("edit-startdate");
    var datestring = dateDisplay.innerHTML;
    var d = new Date(Date.parse(datestring)).toISOString().substr(0, 10);
    document.getElementById("new-startdate").value = d;
    dateDisplay.style.display = "none";
    dateEdit.style.display = "block";
}

function cancelStartDate(){
    var dateDisplay = document.getElementById("startdate");
    var dateEdit = document.getElementById("edit-startdate");
    dateDisplay.style.display = "block";
    dateEdit.style.display = "none";
    console.log("cancelled!")
}

function editDealine() {
    var dateDisplay = document.getElementById("deadline");
    var dateEdit = document.getElementById("edit-deadline");
    var datestring = dateDisplay.innerHTML;
    var d = new Date(Date.parse(datestring)).toISOString().substr(0, 10);
    document.getElementById("new-deadline").value = d;
    dateDisplay.style.display = "none";
    dateEdit.style.display = "block";
}

function cancelDeadline(){
    var dateDisplay = document.getElementById("deadline");
    var dateEdit = document.getElementById("edit-deadline");
    dateDisplay.style.display = "block";
    dateEdit.style.display = "none";
    console.log("cancelled!")
}

function formatDate(date) {
    var monthNames = [
      "January", "February", "March",
      "April", "May", "June", "July",
      "August", "September", "October",
      "November", "December"
    ];
  
    var day = date.getDate();
    var monthIndex = date.getMonth();
    var year = date.getFullYear();
  
    return monthNames[monthIndex] + ' ' + day + ', ' + year;
  }

