import { SetAllClasses, SetAllSection, SetSelectedValue } from "/static/js/pages_script/all_students/search_bar.js"
import { getRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"

var table = $('#example').DataTable();

var min_id = 0
let pointers = document.getElementsByClassName('pointer');
for (let i = 0; i < pointers.length; i++) {
    let tr = pointers[i]
    let tds = tr.getElementsByTagName('td');
    min_id = tds[0].innerText
}
setTimeout(() => {
    element = document.getElementsByName('example_length')[0].parentElement.parentElement.parentElement.parentElement.style.display = 'none';
    console.log(element);
}, 10);

async function GetStudents() {
    let url = Complete_url('DataApi', '/all_students');

    let class_id = document.getElementById('class_id').value;
    let section_id = document.getElementById('section_id').value;
    let name = document.getElementById('name').value;
    let father_name = document.getElementById('father_name').value;
    let mother_name = document.getElementById('mother_name').value;
    let admision_number = document.getElementById('admision_number').value;
    let aadhar_number = document.getElementById('aadhar_number').value;
    let phone_number = document.getElementById('phone_number').value;

    url = `${url}?class_id=${class_id}&section_id=${section_id}&name=${name}&father_name=${father_name}&mother_name=${mother_name}&admision_number=${admision_number}&aadhar_number=${aadhar_number}&phone_number=${phone_number}&min_id=${min_id}`
    console.log(url);
    let remaining_students = await getRequest(url)
    try {
        for (let i = 0; i < remaining_students.length; i++) {
            // sr_no += 1;
            var newData = [
                // sr_no,
                remaining_students[i].admision_number,
                remaining_students[i].name,
                remaining_students[i].father_name,
                remaining_students[i].mother_name,
                remaining_students[i].class,
                // / Create a link for the URL
                '<a href="' + remaining_students[i].action_link + '"><i class="fa fa-eye"></i> View </a>'
            ];
            table.row.add(newData).draw();
        }
    }
    catch (error) {
        console.log(error);
    }
}


await GetStudents();
