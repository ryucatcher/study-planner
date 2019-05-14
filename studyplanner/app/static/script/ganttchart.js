const _MS_PER_DAY = 1000 * 60 * 60 * 24;

var ganttdata;
var ganttlinks;

function daysBetween(a, b) {
  const utc1 = Date.UTC(a.getFullYear(), a.getMonth(), a.getDate());
  const utc2 = Date.UTC(b.getFullYear(), b.getMonth(), b.getDate());

  return Math.floor((utc2 - utc1) / _MS_PER_DAY);
}

window.onload = function(){

    gantt.config.scale_unit = "day";
    gantt.config.step = 1;
    gantt.config.date_scale = "%d";

    gantt.config.columns = [
        {name:"text",       label:"Task name",  width:"*", tree:true },
        {name:"start", label:"Start date", align:"center", width:100 },
        {name:"deadline",   label:"Deadline",   align:"center", width:100 }
    ];

    gantt.init('chart');

    ganttdata = [];
    ganttlinks = [];
    linkid = 0;
    linkdata = [];

    // Convert gantt model data
    var id = 0;
    for(c in chartdata){
        if(!chartdata.hasOwnProperty(c)) continue;
        m = chartdata[c];

        id++;
        var moduleID = id;
        ganttdata.push({
            id: moduleID, _data:m, text: m.name, start: '', duration: 0, deadline: '', progress: 0, open: true, readonly: true
        });

        m.assessments.forEach((a) => {
            a.startDate = new Date(Date.parse(a.startDate));
            a.deadline = new Date(Date.parse(a.deadline));
            a.duration = daysBetween(a.startDate, a.deadline);
            a.assessmentType = a.assessmentType.substr(a.assessmentType.indexOf('.')+1);

            id++;
            var assessmentID = id;
            var startDate = a.startDate.toLocaleDateString('en-GB');
            var deadline = a.deadline.toLocaleDateString('en-GB');
            ganttdata.push({
                id: assessmentID, _data: a, text: a.name + ": " + a.assessmentType, start_date: startDate, start: startDate, deadline: deadline, duration: a.duration, parent: moduleID, progress: 0, open: true, readonly: true
            });

            var dateOffset = 0;

            var sorted = a.tasks.sort((a, b)=>{
                if(a.dependencies.includes(b.id)){
                    return -1;
                }else if(b.dependencies.includes(a.id)){
                    return 1;
                }else{
                    return 0;
                }
            });

            sorted = sorted.reverse()

            sorted.forEach((t)=>{
                id++;
                var taskID = id;
                var start = new Date(a.startDate);
                start.setDate(start.getDate() + dateOffset);
                var deadline = new Date(start)
                deadline.setDate(deadline.getDate() + t.duration);
                t.dependencies.forEach((d)=>{
                    linkdata.push({
                        source: taskID,
                        targetUID: d
                    });
                });
                ganttdata.push({
                    id: taskID, _data:t, text: t.name, start_date: start, start: start.toLocaleDateString('en-GB'), deadline: deadline.toLocaleDateString('en-GB'), duration: t.duration, parent: assessmentID, progress: 0, open: true, readonly: true
                });
                dateOffset += t.duration;
            });
        });

    }

    linkdata.forEach((data)=>{
        linkid++;
        var targetid = ganttdata.filter((entry)=> entry._data.id == data.targetUID)[0].id;
        ganttlinks.push({
            id: linkid,
            source: targetid,
            target: data.source,
            type: "0"
        });
    });

    gantt.parse({
        data: ganttdata,
        links: ganttlinks
    });

    // Add milestones
    setInterval(()=>{
        ganttdata.filter((entry) => Array.isArray(entry._data.milestones)).filter((entry)=>entry._data.milestones.length > 0).forEach((entry)=>{
            entry._data.milestones.forEach((milestone)=>{
                var taskid = milestone.tasks.sort((a,b) => {
                    var aid = ganttdata.filter((e)=>e._data.id == a)[0].id;
                    var bid = ganttdata.filter((e)=>e._data.id == b)[0].id;
                    return aid - bid;
                })[milestone.tasks.length-1];
                // Add element style for milestone
                var el = $('div[task_id="'+ ganttdata.filter(entry => entry._data.id == taskid)[0].id +'"');
                el.addClass('milestone-task');
                el.attr('data-content', milestone.name);
            });
        });
    }, 1000);

}