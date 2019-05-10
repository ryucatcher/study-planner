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
    for(code in modelData){
        if(!modelData.hasOwnProperty(code)) continue;
        moduleSelector.options[moduleSelector.options.length] = new Option(modelData[code].name, code);
    }

    var firstCode = Object.keys(modelData)[0];
    var aSelector = document.getElementById('assessment');
    for(i in modelData[firstCode].assessments){
        aSelector.options[aSelector.options.length] = new Option(code + ":" + modelData[firstCode].assessments[i].assessmentType, i);
    }

    moduleSelector.onchange = function(e){
        removeOptions(aSelector);
        var code = moduleSelector.options[moduleSelector.selectedIndex].value;

        for(i in modelData[code].assessments){
            aSelector.options[aSelector.options.length] = new Option(code + ":" + modelData[code].assessments[i].assessmentType, i);
        }
    }

    var dSelector = document.getElementById('tasks');
    aSelector.onchange = function(e){
        removeOptions(dSelector);
        var code = aSelector.options[aSelector.selectedIndex].value;

        for(i in modelData[code].assessments){
            for(j in modelData[code].assessments[i].tasks){

            aSelector.options[aSelector.options.length] = new Option(code + ":" + modelData[code].assessments[i].tasks[j], i);
            }
        }
    }
}