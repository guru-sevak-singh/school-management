import { GenerateTimeTableHeading, GeneratetimeTableBody, all_classes, TimeTable, AddSubmitTimeTableButton } from "/static/js/pages_script/time_table/time_table_functions.js";

const period_counts = document.getElementById('period_counts');
period_counts.addEventListener('change', function (event) {
    document.getElementById('recess_after_period').value = parseInt(event.target.value / 2) + 1
})



function GenerateTable() {
    let day = document.getElementById('day').value;
    let period_counts = document.getElementById('period_counts').value;
    let break_time = document.getElementById('break_time').value;
    let from_time = document.getElementById('from_time').value;
    let to_time = document.getElementById('to_time').value;

    console.log(from_time, to_time)

    if (day == "" || period_counts == "" || break_time == "" || from_time == "" || to_time == "") {
        alert('There is a Veckent Field');
    }

    else {
        try {
            GenerateTimeTableHeading(from_time, to_time, period_counts, break_time);
            GeneratetimeTableBody(all_classes, period_counts);
            AddSubmitTimeTableButton()
            console.log(TimeTable)
        }
        catch (error) {
            console.log(error.message);
        }
    }
}


const generate_table = document.getElementById('generate_table');
generate_table.addEventListener('click', function () {
    GenerateTable()
})

