import { getRequest, PostRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"

const selected_class_value = document.getElementById('selected_class_value').innerText

const ClassInput = document.getElementById('attendence_class');
ClassInput.value = selected_class_value;

const section_id = document.getElementById('section').value;

async function AddSection(selected_class) {

    document.getElementById('section').innerHTML = ""
    let section_inner_html = `<option value=""> Choose Section </option>`;

    if (selected_class != "") {

        const sections = await getRequest('/data/get_section?class_id=' + selected_class);
        for (let n in sections) {
            section_inner_html += `<option value="${sections[n].id}"> ${sections[n].section_name} </option>`
        }
    }

    document.getElementById('section').innerHTML = section_inner_html;

}


ClassInput.addEventListener('change', function (event) {
    AddSection(event.target.value);
})


const attendence_date = document.getElementById('attendence_date').value;


var attendence_data = []

function ShowAttendenceTable(status) {

    let tbody = document.getElementsByTagName('tbody')[0];
    tbody.innerHTML = '';
    let g = 1
    let present_student_counts = 0;
    let absent_student_counts = 0;
    let leave_students_counts = 0;
    let total_students_counts = 0;

    for (let i = 0; i < attendence_data.length; i++) {
        total_students_counts += 1
        if (status == 'all') {
            let tr = document.createElement('tr');
            let tr_html = `<td>${g}</td>
                    <td>${attendence_data[i].roll_number}</td>
                    <td>${attendence_data[i].name}</td>
                    <td>${attendence_data[i].father_name}</td>
                    <td>${attendence_data[i].gender}</td>
                    `;
            if (attendence_data[i].present_status == 'Present') {
                present_student_counts += 1;
                tr_html += `<td><div class='btn btn-info  btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
            }
            if (attendence_data[i].present_status == 'Absent') {
                absent_student_counts += 1;
                tr_html += `<td><div class='btn btn-danger btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
            }
            if (attendence_data[i].present_status == 'Leave') {
                leave_students_counts += 1;
                tr_html += `<td><div class='btn btn-warning text-grey btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
            }

            tr.innerHTML = tr_html;
            tbody.appendChild(tr);
            g += 1;
        }

        else {
            if (attendence_data[i].present_status == status) {
                let tr = document.createElement('tr');
                let tr_html = `<td>${g}</td>
                    <td>${attendence_data[i].roll_number}</td>
                    <td>${attendence_data[i].name}</td>
                    <td>${attendence_data[i].father_name}</td>
                    <td>${attendence_data[i].gender}</td>
                    `;
                if (attendence_data[i].present_status == 'Present') {
                    present_student_counts += 1;
                    tr_html += `<td><div class='btn btn-info  btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
                }
                if (attendence_data[i].present_status == 'Absent') {
                    absent_student_counts += 1;
                    tr_html += `<td><div class='btn btn-danger btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
                }
                if (attendence_data[i].present_status == 'Leave') {
                    leave_students_counts += 1;
                    tr_html += `<td><div class='btn btn-warning text-grey btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
                }
                tr.innerHTML = tr_html;
                tbody.appendChild(tr);
                g += 1;
            }
            else {
                if (attendence_data[i].present_status == 'Present') {
                    present_student_counts += 1;
                }
                if (attendence_data[i].present_status == 'Absent') {
                    absent_student_counts += 1;
                }
                if (attendence_data[i].present_status == 'Leave') {
                    leave_students_counts += 1;
                }

            }
        }


    }

    console.log(present_student_counts, absent_student_counts, leave_students_counts, total_students_counts);

    let present_students = present_student_counts;
    let total_students = total_students_counts;
    let student_percentage = parseInt((present_students / total_students) * 100);
    document.getElementById('present_students').style.width = `${student_percentage}%`;

    let absent_students = absent_student_counts;
    let absent_perscentage = parseInt((absent_students / total_students) * 100);
    document.getElementById('absent_students').style.width = `${absent_perscentage}%`

    let leave_students = leave_students_counts;
    let leave_perscentage = parseInt((leave_students / total_students) * 100)
    document.getElementById('leave_students').style.width = `${leave_perscentage}%`

    document.getElementById('total_students').style.width = `100%`

    let present_student_labek = document.getElementById('present_student_labek');
    present_student_labek.innerText = `${present_students} / ${total_students}`

    let absent_student_label = document.getElementById('absent_student_label');
    absent_student_label.innerText = `${absent_students} / ${total_students}`

    let leave_students_label = document.getElementById('leave_students_label');
    leave_students_label.innerText = `${leave_students} / ${total_students}`

    let total_student_label = document.getElementById('total_student_label');
    total_student_label.innerText = `${total_students} / ${total_students}`


}


async function GetAttendenceData() {
    if (selected_class_value == "" || section_id == "" || attendence_date == "") {

    }
    else {
        let data_url = Complete_url('DataApi', '/get_attendence?request_for=SingleClass&class_id=' + selected_class_value + '&section_id=' + section_id + '&attendence_date=' + attendence_date)
        console.log(data_url);
        attendence_data = await getRequest(data_url);
        ShowAttendenceTable('all');
    }

}


GetAttendenceData()



const leave_card = document.getElementById('leave_card');
console.log(leave_card);
leave_card.addEventListener('click', function () {
    console.log('going to show leave')
    ShowAttendenceTable('Leave')
})

const present_card = document.getElementById('present_card');
present_card.addEventListener('click', function () {
    ShowAttendenceTable('Present')
});

const absent_card = document.getElementById('absent_card');

absent_card.addEventListener('click', function () {
    ShowAttendenceTable('Absent')
});

const all_staff_card = document.getElementById('all_staff_card');
all_staff_card.addEventListener('click', function () {
    ShowAttendenceTable('all');
});
