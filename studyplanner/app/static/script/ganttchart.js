const _MS_PER_DAY = 1000 * 60 * 60 * 24;

var ganttdata;

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

    // Convert gantt model data
    var id = 0;
    for(c in chartdata){
        if(!chartdata.hasOwnProperty(c)) continue;
        m = chartdata[c];

        id++;
        var moduleID = id;
        ganttdata.push({
            id: moduleID, text: m.name, start: '', duration: 0, deadline: '', progress: 0, open: true, readonly: true
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
                id: assessmentID, text: a.name + ": " + a.assessmentType, start_date: startDate, start: startDate, deadline: deadline, duration: a.duration, parent: moduleID, progress: 0, open: true, readonly: true
            });

            var dateOffset = 0;

            a.tasks.forEach((t)=>{
                id++;
                var taskID = id;
                var start = new Date(a.startDate);
                start.setDate(start.getDate() + dateOffset);
                var deadline = new Date(start)
                deadline.setDate(deadline.getDate() + t.duration);
                ganttdata.push({
                    id: taskID, text: t.name, start_date: start, start: start.toLocaleDateString('en-GB'), deadline: deadline.toLocaleDateString('en-GB'), duration: t.duration, parent: assessmentID, progress: 0, open: true, readonly: true
                });
                dateOffset += t.duration;
            });
        });

    }

    gantt.parse({
        data: ganttdata
    });

    var test = [
        {
            id: 1, text: 'Item 1', start_date: '03-05-2019', duration: 14, progress: 0.4, open: true, readonly: true,
        },
        {
            id: 2, text: 'Item 2', start_date: '03-04-2019', duration: 40, progress: 0.4, open: true, readonly: true,
        },
        {
            id: 3, text: 'Item 3', start_date: '23-05-2019', duration: 14, progress: 0.4, open: true, readonly: true,
        },
        {
            id: 4, text: 'Item 4', start_date: '03-05-2019', duration: 1, progress: 0.4, open: false, readonly: true,
        },
    ]
}