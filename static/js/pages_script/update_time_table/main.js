import { get_day_data, CreateHeading } from "/static/js/pages_script/update_time_table/functions.js"

const DayDropDown = document.getElementById('day');


var time_table_data = {}

DayDropDown.addEventListener('change', async function (event) {
    if (event.target.value == '') {
        alert('Please Selecte Any Day');
    }

    else {

        let day = event.target.value;
        time_table_data = await get_day_data(day);


        // function sortTimetable(timetable) {
        //     const sortedKeys = Object.keys(timetable).sort((a, b) => {
        //         const classIdA = timetable[a][0].class_id;
        //         const classIdB = timetable[b][0].class_id;
        //         return classIdA.localeCompare(classIdB);
        //     });

        //     const sortedTimetable = {};
        //     sortedKeys.forEach(key => {
        //         sortedTimetable[key] = timetable[key];
        //     });

        //     return sortedTimetable;
        // }

        // let sorted_time_table = sortTimetable(time_table_data);
        // console.log(sorted_time_table);

        CreateHeading(time_table_data);

        

    }
})