function removeOptions(selectbox)
{
    var i;
    for(i = selectbox.options.length - 1 ; i >= 0 ; i--)
    {
        selectbox.remove(i);
    }
}

window.onload = function(){
    var moduleSelector = document.getElementById("module");
    var dSelector = document.getElementById('dependances');
    for(code in modelData){
        if(!modelData.hasOwnProperty(code)) continue;
        moduleSelector.options[moduleSelector.options.length] = new Option(modelData[code].name, code);
    }

    var firstCode = Object.keys(modelData)[0];
    var aSelector = document.getElementById('assessment');
    for(i in modelData[firstCode].assessments){
        var a = modelData[firstCode].assessments[i];
        aSelector.options[aSelector.options.length] = new Option(a.name, a.id);
    }
    modelData[firstCode].assessments[0].tasks.forEach((task)=>{
        dSelector.options[dSelector.options.length] = new Option(task.name, task.id);
    });

    moduleSelector.onchange = function(e){
        removeOptions(aSelector);
        removeOptions(dSelector);
        dSelector.options[0] = new Option("Choose...", null);
        var code = moduleSelector.options[moduleSelector.selectedIndex].value;

        for(i in modelData[code].assessments){
            var a = modelData[code].assessments[i];
            aSelector.options[aSelector.options.length] = new Option(a.name, a.id);
        }

        modelData[code].assessments[0].tasks.forEach((task)=>{
            dSelector.options[dSelector.options.length] = new Option(task.name, task.id);
        });
    }

    aSelector.onchange = function(e){
        removeOptions(dSelector);
        dSelector.options[0] = new Option("Choose...", null);
        var aid = aSelector.options[aSelector.selectedIndex].value;

        var code = moduleSelector.options[moduleSelector.selectedIndex].value;
        var assessment = modelData[code].assessments.filter((as)=>as.id==aid)[0];

        assessment.tasks.forEach((task)=>{
            dSelector.options[dSelector.options.length] = new Option(task.name, task.id);
        });
    }
}