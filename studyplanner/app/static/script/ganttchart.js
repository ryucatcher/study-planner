window.onload = function(){

    gantt.config.scale_unit = "day";
    gantt.config.step = 1;
    gantt.config.date_scale = "%d";

    gantt.init('chart');
    gantt.parse({
        data: [
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
    });
}