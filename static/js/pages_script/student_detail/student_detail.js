import { getRequest, PostRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"

const student_id = document.getElementById('student_id').innerText;
const class_id = document.getElementById('class_id').innerText;


// Functions To Show The Attendence.
var attendence_data = [];
async function GetAttendence() {
    let attendence_input = document.getElementById('attendence_date')
    let attendence_date = attendence_input.value;

    let url = Complete_url('DataApi', '/get_attendence')
    url = url + "?request_for=SingleStudent&student_id=" + student_id


    if (attendence_date == "") {
        alert(`Please Select Any Month To See Attendence`)
    }
    else {

        url = url + "&attendence_date=" + attendence_date + "-01"
        attendence_data = await getRequest(url);
        ShowAttendence()

    }
}
function ShowAttendence() {
    const table_body = document.getElementById('attendence_table_body');
    table_body.innerHTML = "";
    for (let i = 0; i < attendence_data.length; i++) {
        let tr = document.createElement('tr');
        let tr_html = `<td>${i + 1}</td>
        <td>${attendence_data[i].attendence_date}</td>
        <td>${attendence_data[i].attendence_day}</td>`

        if (attendence_data[i].present_status == 'Present') {
            tr_html += `<td class='text-center'><div class='btn btn-info  btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
        }
        if (attendence_data[i].present_status == 'Absent') {
            tr_html += `<td class='text-center'><div class='btn btn-danger btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
        }
        if (attendence_data[i].present_status == 'Leave') {
            tr_html += `<td class='text-center'><div class='btn btn-warning text-grey btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
        }

        tr.innerHTML = tr_html;
        table_body.appendChild(tr);
    }
}
const AttendenceButton = document.getElementById('attendence_button')
AttendenceButton.addEventListener('click', async function () {
    await GetAttendence();
})



// Functions to get the documents.
var document_list = []
async function getAllDocuments() {
    let url = Complete_url('DataApi', '/get_students_documents')
    url = url + "?student_id=" + student_id

    document_list = await getRequest(url);
    const document_tbody = document.getElementById('document_tbody');
    for (let i = 0; i < document_list.length; i++) {
        let tr = document.createElement('tr');
        let tr_html = `<td>${i + 1}</td>
        <td>${document_list[i].document_name}</td>
        <td>${document_list[i].uploaded_date}</td>
        <td class='text-center'><a href="${document_list[i].download_url}" target="_blank"><i class="fa fa-eye success mr-2" tooltip="View"></i>View</a></td>
        <td class='text-center'><a href="${document_list[i].delete_url}"><i class="fa fa-trash success mr-2 text-danger" tooltip="Delete"></i>Delete</a></td>`
        tr.innerHTML = tr_html;
        document_tbody.appendChild(tr);
    }

}
const documentTabButton = document.getElementById('document-tab');
documentTabButton.addEventListener('click', async function () {
    if (document_list.length == 0) {
        await getAllDocuments()
    }

})

var subject_list = [];

// function to get the subject list in the class
async function getSubjectList() {
    let url = Complete_url('DataApi', '/get_subject_in_class');
    url = url + "?class_id=" + class_id;

    subject_list = await getRequest(url);
    const subject_tbody = document.getElementById('subject_tbody');


    for (let i = 0; i < subject_list.length; i++) {
        let tr = document.createElement('tr');
        let tr_html = `<td>${i + 1}</td>
        <td>${subject_list[i].subject_name}</td>
        <td>
        `
        let teachers = subject_list[i].teachers;

        for (let n = 0; n < teachers.length; n++) {
            tr_html += teachers[n];
            tr_html += ","
        }
        tr_html += "</td>"

        tr.innerHTML = tr_html;
        subject_tbody.appendChild(tr);
    }

}
const SubjectTabButton = document.getElementById('subjects-tab');
SubjectTabButton.addEventListener('click', async function () {
    if (subject_list.length == 0) {
        await getSubjectList();
    }
})

// Function To Show The Time Table
var time_table = {}
async function GetTimeTable() {

    let time_table_area = document.getElementById('time-table');

    if (time_table_area.innerText.length == 0) {

        let url = Complete_url('DataApi', '/get_student_time_table');
        url = `${url}?student_id=${student_id}`;
        time_table = await getRequest(url);

        var sortedDict = {};
        Object.keys(time_table).sort(function (a, b) {
            return ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].indexOf(a) - ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].indexOf(b);
        }).forEach(function (key) {
            sortedDict[key] = time_table[key];
        });

        time_table = sortedDict;

        let div = document.createElement('div');
        div.setAttribute('class', 'table-responsive');
        let table = document.createElement('table');

        table.setAttribute('class', 'table table-bordered')
        let time_table_thead = document.createElement('thead');
        let th = document.createElement('th');
        time_table_thead.appendChild(th);

        for (let i in time_table) {
            let periods = time_table[i]
            for (let n = 0; n < periods.length; n++) {
                th = document.createElement('th');
                th.innerHTML = `<h6 class="text-center">${periods[n].period_name}</h6><p class="small text-center">(${periods[n].start_time} - ${periods[n].end_time})</p>`;
                time_table_thead.appendChild(th);
            }
            break
        }
        let time_table_tbody = document.createElement('tbody');

        for (let i in time_table) {
            let tr = document.createElement('tr');
            th = document.createElement('th');
            th.style.width = "10vw";
            th.textContent = i;
            tr.appendChild(th);

            let period = time_table[i];
            for (let n = 0; n < period.length; n++) {
                let td = document.createElement('td');
                td.innerHTML = `<h6 class="text-center">${period[n].teacher_name}</h6><p class="small text-center">(${period[n].subject})</p>`
                tr.appendChild(td);
            }
            time_table_tbody.appendChild(tr)
        }
        table.appendChild(time_table_thead);
        table.appendChild(time_table_tbody);
        div.appendChild(table);
        time_table_area.appendChild(div)
    }

}
const TimeTableTab = document.getElementById('time-table-tab');
TimeTableTab.addEventListener('click', function () {
    GetTimeTable()
})


// functions to set the values of the input in the Edit form
function SetInputValue() {
    try {
        let blood_group_input = document.getElementById('blood_group');
        blood_group_input.value = document.getElementById('blood_group_value').innerText;
    }
    catch (error) {
        console.log(error.message);
    }
    try {
        let social_catogary_input = document.getElementById('social_catogary');
        social_catogary_input.value = document.getElementById('social_catogary_value').innerText
    }
    catch (error) {
        console.log(error.message);
    }
}

SetInputValue();

const result_tab_button = document.getElementById('result-tab')
var student_all_classes = {}
result_tab_button.addEventListener('click', async function () {

    if (Object.keys(student_all_classes).length == 0) {

        let url = Complete_url('DataApi', `/get_student_all_classes?student_id=${student_id}`)
        student_all_classes = await getRequest(url);

        let class_id_input = document.getElementById('class_name');
        class_id_input.innerHTML = "";
        let option = document.createElement('option')
        option.value = "";
        option.innerText = "Chose Class";
        class_id_input.appendChild(option);

        for (let i = 0; i < student_all_classes.length; i++) {
            option = document.createElement('option');
            option.value = student_all_classes[i].class_id;
            option.innerText = student_all_classes[i].class_name;
            class_id_input.appendChild(option);

        }

    }

})

const clas_in_input = document.getElementById('class_name');
clas_in_input.addEventListener('change', async function (event) {
    if (event.target.value == "") {
        ""
    }
    else {
        let url = Complete_url('DataApi', '/get_all_subjects_for_class?running_class_id=' + String(event.target.value))
        let subjects = await getRequest(url);

        let subject = document.getElementById('subject');
        subject.innerHTML = "";
        let option = document.createElement('option');
        option.value = "";
        option.innerText = "Chose Subject";
        subject.appendChild(option);

        for (let i = 0; i < subjects.length; i++) {
            option = document.createElement('option');
            option.value = subjects[i].subject_name;
            option.innerText = subjects[i].subject_name;
            subject.appendChild(option)
        }

    }
})



async function GetResult() {
    let subject_name = document.getElementById('subject').value;
    let from_date = document.getElementById('from_date').value;
    let to_date = document.getElementById('to_date').value;
    let url = Complete_url('DataApi', '/get_student_result');
    let class_name = document.getElementById('class_name').value;

    url = `${url}?student_id=${student_id}&class_id=${class_name}&subject_name=${subject_name}&from_date=${from_date}&to_date=${to_date}`;

    let result_tbody = document.getElementById('result_tbody');
    let result_data = await getRequest(url);

    result_tbody.innerHTML = "";

    for (let i = 0; i < result_data.length; i++) {

        let tr = document.createElement('tr');
        let td = document.createElement('td');
        td.innerText = result_data[i].exam_date
        tr.appendChild(td);
        td = document.createElement('td');
        td.innerText = result_data[i].exam_name;
        tr.appendChild(td);

        td = document.createElement('td');
        td.innerText = result_data[i].subject
        tr.appendChild(td);

        td = document.createElement('td');
        td.innerText = result_data[i].marks_obtained;
        tr.appendChild(td);

        td = document.createElement('td');
        td.innerText = result_data[i].max_marks;
        tr.appendChild(td)

        result_tbody.appendChild(tr);

    }

}

const result_button = document.getElementById('result_button')
result_button.addEventListener('click', async function () {
    await GetResult();

})

const current_class = document.getElementById('current_class');
var sections;


function SetSections(sections) {
    var section_element = document.getElementById('current_section')
    section_element.innerHTML = ""

    for (let n in sections) {
        const option = document.createElement('option')
        option.value = sections[n].id;
        option.innerText = sections[n].section_name;
        section_element.appendChild(option)
    }
}


current_class.addEventListener('change', async (event) => {
    const selectedOption = event.target.value;
    sections = await getRequest('/data/get_section?class_id=' + selectedOption);
    SetSections(sections)
});

var all_classes = []
const editButton = document.getElementById('editButton');
editButton.addEventListener('click', async function () {
    if (all_classes.length == 0) {

        let url = Complete_url('DataApi', '/get_all_clases')
        all_classes = await getRequest(url);
        for (let i = 0; i < all_classes.length; i++) {
            console.log(current_class.value)
            if (all_classes[i].value == "" || all_classes[i].value == "teachers" || all_classes[i].value == current_class.value || all_classes[i].class_name == 'Choose Class') {
                console.log("");
            }
            else {
                let option = document.createElement('option');
                option.value = all_classes[i].id;
                option.innerText = all_classes[i].class_name;
                current_class.appendChild(option);

            }

        }
    }
})
