import { getRequest, PostRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"

const staff_id = document.getElementById('staff_id').innerText;


// functions for attendence
var attendence_data = [];
async function GetAttendence() {
    let attendence_input = document.getElementById('attendence_date')
    let attendence_date = attendence_input.value;

    let url = Complete_url('DataApi', '/get_attendence')
    url = url + "?request_for=SingleStaff&staff_id=" + staff_id

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
        else if (attendence_data[i].present_status == 'Absent') {
            tr_html += `<td class='text-center'><div class='btn btn-danger btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
        }
        else if (attendence_data[i].present_status == 'Leave') {
            tr_html += `<td class='text-center'><div class='btn btn-warning text-grey btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
        }
        else {
            tr_html += `<td class='text-center'><div class='btn btn-secondary text-grey btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
        }

        tr.innerHTML = tr_html;
        table_body.appendChild(tr);
    }
}
const AttendenceButton = document.getElementById('attendence_button');
AttendenceButton.addEventListener('click', async function () {
    await GetAttendence();
})
ShowAttendence()


// Function for The documents
var document_list = []
async function getAllDocuments() {
    let url = Complete_url('DataApi', '/get_staff_documents');
    url = url + "?staff_id=" + staff_id;

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


// Function for the Time Table
var period_list = {}
var time_table = {}
async function GetTimeTable() {

    let time_table_area = document.getElementById('time-table');

    if (time_table_area.innerText.length == 0) {

        let url = Complete_url('DataApi', '/get_teacher_time_table');
        url = `${url}?teacher_id=${staff_id}`;
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

        let time_table_tbody = document.createElement('tbody');
        let time_table_thead = document.createElement('thead');
        let th = document.createElement('th');
        time_table_thead.appendChild(th);

        for (let i in time_table) {
            let last_period_name = "Period 0"
            let tr = document.createElement('tr');
            th = document.createElement('th');
            th.style.width = "10vw";
            th.textContent = i;
            tr.appendChild(th);

            let period = time_table[i];

            for (let n = 0; n < period.length; n++) {

                if (!(Object.keys(period_list).includes(period[n].period_name))) {
                    period_list[period[n].period_name] = { "start_time": period[n].start_time, "end_time": period[n].end_time }
                }

                let current_period_name = period[n].period_name

                if (last_period_name == current_period_name) {
                    td.innerHTML += ` <hr><h6 class="text-center">${period[n].class_name}</h6><p class="small text-center">(${period[n].subject})</p>`
                }
                else {
                    var td = document.createElement('td');
                    td.innerHTML = `<h6 class="text-center">${period[n].class_name}</h6><p class="small text-center">(${period[n].subject})</p>`
                    tr.appendChild(td);
                }
                last_period_name = current_period_name;

            }

            time_table_tbody.appendChild(tr)
        }

        for (let i in period_list) {
            th = document.createElement('th');
            th.innerHTML = `<h6 class="text-center">${i}</h6><p class="small text-center">(${period_list[i].start_time} - ${period_list[i].end_time})</p>`;
            time_table_thead.appendChild(th);
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