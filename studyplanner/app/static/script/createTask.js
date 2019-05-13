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
        var a = modelData[firstCode].assessments[i];
        aSelector.options[aSelector.options.length] = new Option(a.name, a.id);
    }

    moduleSelector.onchange = function(e){
        removeOptions(aSelector);
        var code = moduleSelector.options[moduleSelector.selectedIndex].value;

        for(i in modelData[code].assessments){
            var a = modelData[code].assessments[i];
            aSelector.options[aSelector.options.length] = new Option(a.name, a.id);
        }
    }

    if(predefinedData.assessmentid !='none'){
        for(i = moduleSelector.options.length - 1 ; i >= 0 ; i--)
        {
            if(moduleSelector.options[i].value == predefinedData.modulecode){
                moduleSelector.options[i].setAttribute("selected", "selected");
            }
        }
        moduleSelector.disabled = true;
        removeOptions(aSelector);
        var code = moduleSelector.options[moduleSelector.selectedIndex].value;

        for(i in modelData[code].assessments){
            var a = modelData[code].assessments[i];
            aSelector.options[aSelector.options.length] = new Option(a.name, a.id);
        }
        for(i = aSelector.options.length - 1 ; i >= 0 ; i--)
        {
            if(aSelector.options[i].value == predefinedData.assessmentid){
                aSelector.options[i].setAttribute("selected", "selected");
            }
        }
        aSelector.disabled = true;
    }
}

jQuery(function ($) {        
    $('form').bind('submit', function () {
      $(this).find(':input').prop('disabled', false);
    });
  });