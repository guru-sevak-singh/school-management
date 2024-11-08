import { getRequest, PostRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"

export var TimeTable = {}

export var all_classes = [];


let url = Complete_url('DataApi', '/get_all_subjects_classes');
all_classes = await getRequest(url);

export var all_teachers = [];
url = Complete_url('DataApi', '/get_teachers');
all_teachers = await getRequest(url);

const button_box = document.getElementById('button_box');

const teacher_input = document.getElementById('teacher_id');
teacher_input.innerHTML = '<option value=""> Add Teacher </option>';

for (let i = 0; i < all_teachers.length; i++) {
    teacher_input.innerHTML += `<option value="${all_teachers[i].id}">${all_teachers[i].name} (${all_teachers[i].designation})</option>`
}

const subject_input = document.getElementById('subject_id');

const main_content = document.getElementById('main_content');

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

function GetThisClassSubjects(clas_id) {
    let return_data = {}

    for (let i = 0; i < all_classes.length; i++) {

        if (all_classes[i].class_id == clas_id) {
            return_data = all_classes[i]
            break;
        }
        else {
            continue;
        }
    }


    subject_input.innerHTML = "";
    document.getElementById('teacher_id').value = "";
    let new_html = `
    <option value=""> Add Subject </option>
    `
    for (let i = 0; i < return_data.subjects.length; i++) {
        new_html += `<option value="${return_data.subjects[i].subject_id}">${return_data.subjects[i].subject_name}</option>`
    }

    subject_input.innerHTML = new_html;

}


function GetSchoolHours(starting_time, end_time) {
    // This Function return the Running Hours of the School in minutes 

    const time1 = new Date("2000-01-01 " + starting_time);
    const time2 = new Date("2000-01-01 " + end_time);

    // get Difference in Mili Second
    const school_hours = Math.abs(time1 - time2);

    // 1s = 1000ms, 1 min = 60 sec
    const MinuteGap = Math.floor(school_hours / (1000 * 60));

    return MinuteGap;
}

function getPeriodDuration(school_hours, recess_duration, no_of_period) {
    let period_duration = (school_hours - recess_duration) / no_of_period;
    return period_duration
}

function getNextPeriodTime(period_starting_time, period_duration) {
    // Extract hours and minutes from the time string
    const [hours, minutes] = period_starting_time.split(':').map(Number);

    // Calculate the total minutes
    let totalMinutes = hours * 60 + minutes;

    // Add The Period Duration To The Time
    totalMinutes += period_duration;

    // Calculate new hours and minutes
    const newHours = Math.floor(totalMinutes / 60);
    const newMinutes = totalMinutes % 60;

    // Format the new time string
    const formattedTime = `${String(newHours).padStart(2, '0')}:${String(newMinutes).padStart(2, '0')}`;

    return formattedTime;
}

export function GenerateTimeTableHeading(starting_time, end_time, periods, recess_duration) {

    // school running hours
    const school_hours = GetSchoolHours(starting_time, end_time);

    // single period duration in minus
    const period_duration = getPeriodDuration(school_hours, recess_duration, periods);
    alert(period_duration);

    // var recess_after_period = parseInt(periods / 2)

    let thead = document.getElementById('thead');
    thead.innerHTML = "";

    let tr = document.createElement('tr');
    let tr_html = `<th scope="col" style="text-align: center;" class="bg-grey"></th>`

    for (let i = 0; i < periods; i++) {

        var period_end_time = getNextPeriodTime(starting_time, period_duration)
        period_end_time = period_end_time.split(".")[0]
        if (i + 1 == periods) {

            TimeTable[`Period ${i + 1}`] = { "starting_time": starting_time, "end_time": end_time, "period_detail": [] }
            tr_html += `<th scope="col" style="text-align: center;" class="btn-primary">
            <h6>Period ${i + 1}</h6>
            <small class="float-center small text-center mt-2 notice_minutes">(${starting_time}-${end_time})</small>
            </th>`
        }
        else {

            TimeTable[`Period ${i + 1}`] = { "starting_time": starting_time, "end_time": period_end_time, "period_detail": [] }

            tr_html += `<th scope="col" style="text-align: center;" class="btn-primary">
            <h6>Period ${i + 1}</h6>
            <small class="float-center small text-center mt-2 notice_minutes">(${starting_time}-${period_end_time})</small>
            </th>`

            if (i == Number(document.getElementById("recess_after_period").value) - 1) {

                starting_time = period_end_time;
                period_end_time = getNextPeriodTime(starting_time, Number(recess_duration));
                console.log(recess_duration, typeof (recess_duration), period_end_time);
                TimeTable["Recess"] = { "starting_time": starting_time, "end_time": period_end_time, "period_detail": [] }
                tr_html += `<th scope="col" style="text-align: center;" class="bg-grey">
                        <h6>Recess</h6>
                        <small class="float-center small text-center mt-2 notice_minutes">(${starting_time}-${period_end_time})</small>
                    </th>`
            }
        }

        starting_time = period_end_time;
    }

    tr.innerHTML = tr_html;

    thead.appendChild(tr);

}

export function GeneratetimeTableBody(all_classes, periods) {

    let tbody = document.getElementById('tbody');
    tbody.innerHTML = "";

    for (let n = 0; n < all_classes.length; n++) {
        let class_name = all_classes[n].class_name;
        let class_id = all_classes[n].class_id

        let tr = document.createElement('tr');
        tr.setAttribute('id', class_id);

        let th = document.createElement('th');
        th.setAttribute('class', 'btn-secondary');
        th.setAttribute('scope', 'col');
        th.style.width = "100%";
        th.style.textAlign = 'center';
        th.innerText = class_name.replaceAll(" ", "");

        tr.appendChild(th);
        tbody.appendChild(tr);


        for (let i = 0; i < periods; i++) {

            let append_data = { "class_id": class_id, "teacher_id": "", "subject_id": "" };
            let period_name = `Period ${i + 1}`
            console.log(period_name)
            TimeTable[period_name]['period_detail'].push(append_data);

            let td = document.createElement('td');
            td.setAttribute('class', 'time_table_active btn-white text-center');
            td.style.cursor = 'pointer';
            td.innerHTML = `<h6>Add Subject</h6>
            <small class="float-center small text-center mt-2 notice_minutes">(Add Teacher)</small>
            <input type="number" class="teacher_id hidden_element">
            <input type="number" class="subject_id hidden_element">
            <input type="text" class="period_name hidden_element" value="Period ${i + 1}">
            `

            td.addEventListener('click', function () {
                ShowForm(this, TimeTable);
            })
            tr.appendChild(td);


            if (i == Number(document.getElementById("recess_after_period").value) - 1) {
                let append_data = { "class_id": class_id, "teacher_id": "", "subject_id": "" };
                TimeTable['Recess']['period_detail'].push(append_data)
                td = document.createElement('td');
                td.setAttribute('class', 'bg-grey recess_td');
                tr.appendChild(td);

            }

            tbody.appendChild(tr)

        }


    }
}


export function ShowForm(td, TimeTable) {

    console.log(TimeTable);
    let clas_id = td.parentElement.id;
    GetThisClassSubjects(clas_id)
    let period_name = td.getElementsByClassName('period_name')[0].value
    const add_schedule_button = document.getElementById('add_schedule_button');
    add_schedule_button.remove();

    document.getElementById('teacher_id').value = td.getElementsByClassName('teacher_id')[0].value;
    document.getElementById('subject_id').value = td.getElementsByClassName('subject_id')[0].value
    console.log(clas_id, period_name);

    let button = document.createElement('button');
    button.setAttribute('type', 'button');
    button.setAttribute('class', 'btn btn-success');
    button.setAttribute('id', 'add_schedule_button');
    button.innerText = 'Add Schedule';

    button.addEventListener('click', function () {
        console.log('i got clicked');
        try {
            console.log(TimeTable[period_name])

            let period_detail = TimeTable[period_name]['period_detail'];

            let teacher_name = document.getElementById('teacher_id');
            let subject_name = document.getElementById('subject_id');
            let continue_status = true;

            if (teacher_name.value != "") {
                for (let i = 0; i < period_detail.length; i++) {

                    if (period_detail[i].teacher_id == teacher_name.value) {
                        continue_status = confirm('This Teacher Already in Another Class \nDo You Want To Add Same Teacher in Two Classes');
                        break;
                    }
                    else {
                        continue;
                    }
                }
            }

            if (continue_status == true) {

                for (let i = 0; i < period_detail.length; i++) {
                    if (period_detail[i]['class_id'] == clas_id) {
                        period_detail[i]['teacher_id'] = teacher_name.value;
                        period_detail[i]['subject_id'] = subject_name.value;
                        break;
                    }
                    else {
                        continue;
                    }
                }

                td.getElementsByClassName('teacher_id')[0].value = teacher_name.value;
                td.getElementsByClassName('subject_id')[0].value = subject_name.value;

                if (teacher_name.value != "" && subject_name.value != "") {
                    td.classList = [];

                    td.classList.add('bg-primary');
                    td.classList.add('time_table_active');
                    td.classList.add('text-center');
                    td.classList.add('text-white');
                }
                else if (teacher_name.value == "" && subject_name.value != "") {
                    td.classList = [];

                    td.classList.add('bg-danger');
                    td.classList.add('time_table_active');
                    td.classList.add('text-center');
                    td.classList.add('text-white');
                }
                else if (teacher_name.value != "" && subject_name.value == "") {
                    td.classList = [];

                    td.classList.add('bg-warning');
                    td.classList.add('time_table_active');
                    td.classList.add('text-center')
                    td.classList.add('text-dark');
                }
                else {
                    td.classList = [];

                    td.classList.add('bg-grey');
                    td.classList.add('time_table_active');
                    td.classList.add('text-center')
                    td.classList.add('text-dark');
                }


                let selectedIndex = teacher_name.selectedIndex;
                let selectedOption = teacher_name.options[selectedIndex];
                let selectedOptionText = selectedOption.textContent;
                teacher_name = selectedOptionText;

                selectedIndex = subject_name.selectedIndex;
                selectedOption = subject_name.options[selectedIndex];
                selectedOptionText = selectedOption.textContent;
                subject_name = selectedOptionText;
                td.getElementsByTagName('h6')[0].innerText = subject_name;
                td.getElementsByClassName('small')[0].innerText = `(${teacher_name})`;

            }

        }
        catch (error) {
            console.log(error);
        }

        $("#schedule-information-form").modal('hide');

    })

    button_box.appendChild(button);

    $("#schedule-information-form").modal('show');
}


