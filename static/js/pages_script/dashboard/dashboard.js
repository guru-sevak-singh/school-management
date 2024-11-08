import { getRequest, PostRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"


async function ShowAttendence() {
    let dynamic_data_url = Complete_url('DataApi', '/get_todays_attendence_data');
    let attendence_data = await getRequest(dynamic_data_url);
    
    let present_students = attendence_data.student_attendence_data.present;
    let total_students = present_students + attendence_data.student_attendence_data.absent + attendence_data.student_attendence_data.leave;
    let student_percentage = parseInt((present_students/total_students) * 100);
    document.getElementById('student_percentage').style.width = `${student_percentage}%`;

    let present_staff = attendence_data.staff_attendence_data.present;
    let total_staff = present_staff + attendence_data.staff_attendence_data.absent + attendence_data.staff_attendence_data.leave;
    let staff_percentage = parseInt((present_staff/ total_staff) * 100);
    document.getElementById('staff_percentage').style.width = `${staff_percentage}%`

    let student_attendence_label = document.getElementById('student_attendence_label');
    student_attendence_label.innerText = `${present_students} / ${total_students}`

    let staff_attendence_label = document.getElementById('stff_attendence_label');
    staff_attendence_label.innerText = `${present_staff} / ${total_staff}`
    
}

await ShowAttendence()


// let interval;

// interval = setInterval(() => {
//     let current_time = new Date;
//     let current_hours = current_time.getHours();
//     console.log(current_hours);
//     if (current_hours >=7 && current_hours <= 13){
//         ShowAttendence();
//     }
//     else {
//         clearInterval(interval);
//     }
    
// }, 5000);




