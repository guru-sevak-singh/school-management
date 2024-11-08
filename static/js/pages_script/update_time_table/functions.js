import { getRequest, PostRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"
import { ShowForm, all_classes } from "/static/js/pages_script/time_table/time_table_functions.js";

function minuteGap(time1, time2) {
    // Parse the times into Date objects
    const date1 = new Date(`2000-01-01T${time1}`);
    const date2 = new Date(`2000-01-01T${time2}`);

    // Calculate the difference in milliseconds
    const differenceMs = Math.abs(date2 - date1);

    // Convert milliseconds to minutes
    const minutes = Math.floor(differenceMs / (1000 * 60));

    return minutes;

}

async function AddNewTimeTable() {
    let url = Complete_url('DataApi', '/add_new_time_table');
    let schedule_day = document.getElementById('day').value;
    url = url + "?day=" + schedule_day;
    console.log(TimeTable);

    let data = JSON.stringify(TimeTable);
    let time_table_status = await PostRequest(url, data);

    if (time_table_status.status == 'done') {
        alert(`The Time Table of ${schedule_day} is Added Successfully, Do You Want To Add Some More Time Table...`)
    }
}

export function AddSubmitTimeTableButton() {

    if (document.getElementById('update_new_time_table') == null) {
        let button = document.createElement('button');
        button.setAttribute('id', 'update_new_time_table');
        button.setAttribute('class', 'btn btn-success');
        button.textContent = 'Create New Time Table';
        button.addEventListener('click', async function () {
            await AddNewTimeTable()
        })
        main_content.appendChild(button);

    }

}



var all_teachers = [];
let teacher_url = Complete_url('DataApi', '/get_teachers');
all_teachers = await getRequest(teacher_url);


var all_teacher_data = {}
for (let i = 0; i < all_teachers.length; i++) {
    all_teacher_data[String(all_teachers[i].id)] = all_teachers[i];
}

let subject_url = Complete_url('DataApi', '/get_all_subjects_classes')
var all_subject_classes = [];
all_subject_classes = await getRequest(subject_url);

let subject_list = {}
for (let i = 0; i < all_subject_classes.length; i++) {
    let subjects = all_subject_classes[i].subjects;
    for (let n = 0; n < subjects.length; n++) {
        subject_list[subjects[n].subject_id] = subjects[n].subject_name;
    }

}

export async function get_day_data(day) {
    let url = Complete_url('DataApi', '/get_all_time_table')
    url = `${url}?day=${day}`
    let return_data = await getRequest(url);


    return return_data
}

var TimeTable = {};

function SaveNewPeriodData() {
    TimeTable = {};
    let thead = document.getElementById('thead');
    let trs = thead.getElementsByTagName('th');
    for (let i = 1; i < trs.length; i++) {

        let period_name = trs[i].getElementsByTagName('h6')[0].innerText;
        let timing = trs[i].getElementsByTagName('small')[0].innerText;
        timing = timing.replace("(", '');
        timing = timing.replace(')', '');
        timing = timing.replaceAll(" ", "");

        let starting_time = timing.split("-")[0];
        let end_time = timing.split("-")[1];

        TimeTable[period_name] = { "starting_time": starting_time, "end_time": end_time, "period_detail": [] }

    }

    let tbody = document.getElementById('tbody');
    trs = tbody.getElementsByTagName('tr');
    for (let i = 0; i < trs.length; i++) {

        let class_id = trs[i].id;

        let tds = trs[i].getElementsByTagName('td');

        for (let n = 0; n < tds.length; n++) {

            let subject_id = tds[n].getElementsByClassName('subject_id')[0].value;
            let teacher_id = tds[n].getElementsByClassName('teacher_id')[0].value;
            let push_data = { "class_id": class_id, "teacher_id": teacher_id, "subject_id": subject_id }
            let period_name = tds[n].getElementsByClassName('period_name')[0].value;

            TimeTable[period_name]['period_detail'].push(push_data);

        }

    }

}



export function CreateHeading(time_table_data) {

    let thead = document.getElementById('thead');
    thead.innerHTML = "";

    let tbody = document.getElementById('tbody');
    tbody.innerHTML = "";
    let tr = document.createElement('tr');
    let th = document.createElement('th');
    tr.appendChild(th);
    thead.appendChild(tr);


    for (let clas in time_table_data) {
        var period_data = time_table_data[clas];
        let tr = document.createElement('tr');
        th = document.createElement('th');
        th.innerText = clas
        tr.appendChild(th)
        tr.setAttribute('id', time_table_data[clas][0]['class_id']);

        tbody.appendChild(tr);
        let td;

        for (let i = 0; i < period_data.length; i++) {
            let teacher_name = "Add Teacher"

            if (period_data[i].teacher_id != "") {
                teacher_name = `${all_teacher_data[String(period_data[i].teacher_id)].name} (${all_teacher_data[String(period_data[i].teacher_id)].designation})`;

            }

            let subject_name = "Add Subject";

            if (period_data[i].subject_id != "") {
                subject_name = subject_list[period_data[i].subject_id];
            }

            td = document.createElement('td');
            td.setAttribute('class', 'time_table_active text-center');

            if (period_data[i].period_name == 'Recess') {

                td.innerHTML = `<h6></h6><small class='small'></small>
                <input type="number" class="teacher_id hidden_element" value=${period_data[i].teacher_id}>
                <input type="number" class="subject_id hidden_element" value=${period_data[i].subject_id}>
                <input type='text' readonly class="period_name hidden_element" value="${period_data[i].period_name}">
                `
            }
            else {

                td.innerHTML = `<h6>${subject_name}</h6><small class='small'>(${teacher_name})</small>
            <input type="number" class="teacher_id hidden_element" value=${period_data[i].teacher_id}>
            <input type="number" class="subject_id hidden_element" value=${period_data[i].subject_id}>
            <input type='text' readonly class="period_name hidden_element" value="${period_data[i].period_name}">
            `
            }
            if (teacher_name == 'Add Teacher' && subject_name == 'Add Subject') {
                td.classList.add('bg-white');
                td.classList.add('text-dark');
            }
            else if (teacher_name != 'Add Teacher' && subject_name != 'Add Subject') {
                td.classList.add('bg-primary');
                td.classList.add('text-white')

            }
            else if (teacher_name != 'Add Teacher' && subject_name == 'Add Subject') {
                td.classList.add('bg-warning');
                td.classList.add('text-dark');
            }
            else {
                td.classList.add('bg-danger');
                td.classList.add('text-white');
            }

            td.addEventListener('click', function () {

                ShowForm(this, TimeTable);
            });

            tr.appendChild(td);
            tbody.appendChild(tr);
        }

    }

    for (let i = 0; i < period_data.length; i++) {
        th = document.createElement('th');
        th.setAttribute('class', 'text-center table-heading');
        th.innerHTML = `<h6>${period_data[i].period_name}</h6><small class='small'>(${period_data[i].period_starting_time} - ${period_data[i].period_end_time})</small>`;
        tr.appendChild(th);
        if (i == 0) {
            document.getElementById('from_time').value = period_data[i].period_starting_time;
        }

        if ( i == period_data.length  -1){
            document.getElementById('to_time').value = period_data[i].period_end_time;
        }

        if (period_data[i].period_name == 'Recess') {
            
            let reces_gap = minuteGap(period_data[i].period_starting_time, period_data[i].period_end_time);

            document.getElementById('break_time').value = reces_gap;

            document.getElementById('recess_after_period').value = i;


        }
    }


    SaveNewPeriodData(time_table_data);
    console.log(TimeTable);
    AddSubmitTimeTableButton();

    document.getElementById('period_counts').value = period_data.length - 1;

}