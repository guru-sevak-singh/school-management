import { getRequest, PostRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"

const attendence_date = document.getElementById('attendence_date').value;

async function ShowAttendence() {
    let dynamic_data_url = Complete_url('DataApi', '/get_monthly_attendence_data?attendence_date=' + attendence_date);
    console.log(dynamic_data_url);
    let attendence_data = await getRequest(dynamic_data_url);
    
    let present_students = attendence_data.student_attendence_data.present;
    let total_students = present_students + attendence_data.student_attendence_data.absent + attendence_data.student_attendence_data.leave;
    let student_percentage = parseInt((present_students/total_students) * 100);
    document.getElementById('present_students').style.width = `${student_percentage}%`;

    let absent_students = attendence_data.student_attendence_data.absent;
    let absent_perscentage = parseInt((absent_students/total_students) * 100);
    document.getElementById('absent_students').style.width = `${absent_perscentage}%`

    let leave_students = attendence_data.student_attendence_data.leave;
    let leave_perscentage = parseInt((leave_students/ total_students)* 100)
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

function ShowAttendenceTable() {
    let tbody = document.getElementsByTagName('tbody')[0];
    tbody.innerHTML = '';

    for (let i = 0; i <= attendence_data.length; i++) {


        let tr = document.createElement('tr');
        let tr_html = `<td>${i + 1}</td>
                    <td>${attendence_data[i].class_name}</td>
                    <td class="text-center">
                        <div class='btn btn-info btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_count} </div>
                    </td>
                    <td class="text-center">
                        <div class='btn btn-danger btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].absent_count} </div>
                    </td>
                    <td class="text-center">
                        <div class='btn btn-warning text-grey btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].leave_counts} </div>
                    </td>`

        tr.innerHTML = tr_html;
        tbody.appendChild(tr);

    }

}

await ShowAttendence();

var attendence_data = []

async function GetAttendenceData() {
    let data_url = Complete_url('DataApi', '/get_monthly_attendence?request_for=AllClasses&attendence_date=' + attendence_date)
    console.log(data_url);
    attendence_data = await getRequest(data_url);
    ShowAttendenceTable();

}


GetAttendenceData()

