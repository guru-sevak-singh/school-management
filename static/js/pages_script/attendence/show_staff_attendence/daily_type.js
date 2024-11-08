import { getRequest, PostRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"

const attendence_date = document.getElementById('attendence_date').value;



async function ShowAttendence() {
    let dynamic_data_url = Complete_url('DataApi', '/get_todays_attendence_data?attendence_date=' + attendence_date);
    let attendence_data = await getRequest(dynamic_data_url);

    let present_teacher = attendence_data.staff_attendence_data.present;
    let total_staff = present_teacher + attendence_data.staff_attendence_data.absent + attendence_data.staff_attendence_data.leave;
    let student_percentage = parseInt((present_teacher / total_staff) * 100);
    document.getElementById('present_teacher').style.width = `${student_percentage}%`;

    let absent_staff = attendence_data.staff_attendence_data.absent;
    let absent_perscentage = parseInt((absent_staff / total_staff) * 100);
    document.getElementById('absent_staff').style.width = `${absent_perscentage}%`

    let leave_staff = attendence_data.staff_attendence_data.leave;
    let leave_perscentage = parseInt((leave_staff / total_staff) * 100)
    document.getElementById('leave_staff').style.width = `${leave_perscentage}%`

    document.getElementById('total_staff').style.width = `100%`

    let present_student_labek = document.getElementById('present_student_labek');
    present_student_labek.innerText = `${present_teacher} / ${total_staff}`

    let absent_student_label = document.getElementById('absent_student_label');
    absent_student_label.innerText = `${absent_staff} / ${total_staff}`

    let leave_staff_label = document.getElementById('leave_staff_label');
    leave_staff_label.innerText = `${leave_staff} / ${total_staff}`

    let total_staff_label = document.getElementById('total_staff_laebl');
    total_staff_label.innerText = `${total_staff} / ${total_staff}`

}


await ShowAttendence()

var attendence_data = []

function ShowAttendenceTable(status) {
    let tbody = document.getElementsByTagName('tbody')[0];
    tbody.innerHTML = '';
    let g = 1
    for (let i = 0; i <= attendence_data.length; i++) {
        if (status == 'all') {

            let tr = document.createElement('tr');
            let tr_html = `<td>${g}</td>
                    <td>${attendence_data[i].name}</td>
                    <td>${attendence_data[i].designation}</td>
                    `;
            if (attendence_data[i].present_status == 'Present') {
                tr_html += `<td><div class='btn btn-info  btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
            }
            else if (attendence_data[i].present_status == 'Absent') {
                tr_html += `<td><div class='btn btn-danger btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
            }
            else if (attendence_data[i].present_status == 'Leave') {
                tr_html += `<td><div class='btn btn-warning text-grey btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
            }
            else {
                tr_html += `<td><div class='btn btn-secondary text-grey btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
            }

            tr.innerHTML = tr_html;
            tbody.appendChild(tr);
            g+= 1;
        }

        else {
            if (attendence_data[i].present_status == status) {
                let tr = document.createElement('tr');
                let tr_html = `<td>${g}</td>
                    <td>${attendence_data[i].name}</td>
                    <td>${attendence_data[i].designation}</td>
                    `;
                if (attendence_data[i].present_status == 'Present') {
                    tr_html += `<td><div class='btn btn-info  btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
                }
                else if (attendence_data[i].present_status == 'Absent') {
                    tr_html += `<td><div class='btn btn-danger btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
                }
                else if (attendence_data[i].present_status == 'Leave') {
                    tr_html += `<td><div class='btn btn-warning text-grey btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
                }
                else {
                    tr_html += `<td><div class='btn btn-secondary text-grey btn-sm rounded-pill'><i class="fa fa-circle" aria-hidden="true"></i> ${attendence_data[i].present_status} </div></td>`
                }
    
                tr.innerHTML = tr_html;
                tbody.appendChild(tr);
                g+= 1;
            }
        }


    }
}


async function GetAttendenceData() {
    let data_url = Complete_url('DataApi', '/get_attendence?request_for=Teachers&attendence_date=' + attendence_date)
    console.log(data_url);
    attendence_data = await getRequest(data_url);
    ShowAttendenceTable('all');

}


GetAttendenceData()


const leave_card = document.getElementById('leave_card');
leave_card.addEventListener('click', function () {
    console.log('going to show leave')
    ShowAttendenceTable('Leave')
})

const present_card = document.getElementById('present_card');
present_card.addEventListener('click', function() {
    ShowAttendenceTable('Present')
});

const absent_card = document.getElementById('absent_card');

absent_card.addEventListener('click', function() {
    ShowAttendenceTable('Absent')
});

const all_staff_card = document.getElementById('all_staff_card');
all_staff_card.addEventListener('click', function() {
    ShowAttendenceTable('all');
});
