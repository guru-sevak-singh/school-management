import { getRequest, PostRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"

let url = Complete_url('DataApi', '/get_all_clases');
console.log(url);
var all_classes = await getRequest(url);

const all_calss_select = document.getElementById('class_id');
let option;

for (let i = 0; i < all_classes.length; i++) {
    if (all_classes[i].id == "") {
        option = document.createElement('option');
        option.value = "";
        option.innerText = "Class";
        all_calss_select.appendChild(option);
    }
    else if (all_classes[i].id != 'teachers') {
        option = document.createElement('option');
        option.value = all_classes[i].id;
        option.innerText = all_classes[i].class_name;
        all_calss_select.appendChild(option);
    }
    
}

all_calss_select.addEventListener('change', async function (event) {

    var exam_date = document.getElementById('exam_date').value;
    var max_marks = document.getElementById('max_marks').value;
    var exam_name = document.getElementById('exam_name').value;

    console.log(exam_date, max_marks, exam_name);

    if (exam_date == "" || max_marks == "" || exam_name == "") {
        event.target.value = "";
        if (exam_date == "") {
            alert('Please Enter The Exam Date');
        }
        else if (max_marks == "") {
            alert('Please Enter The Maximum Marks of The Exam');
        }
        else {
            alert('Please Enter The Exam Name');
        }
    }
    else {
        let sections = "";
        let section_id = document.getElementById('section_id');
        section_id.innerHTML = "";
        url = Complete_url('DataApi', '/get_section?class_id=')
        url = url + String(event.target.value);
        sections = await getRequest(url);
        let option = document.createElement('option');
        option.value = "";
        option.innerText = "Section";
        section_id.appendChild(option);

        for (let i = 0; i < sections.length; i++) {

            option = document.createElement('option');
            option.value = sections[i].id;
            option.innerText = sections[i].section_name;
            section_id.appendChild(option);
        }

    }
})

const subject = document.getElementById('subject');
subject.addEventListener('change', async function(event){
    let max_marks = document.getElementById('max_marks').value;
    let class_id = document.getElementById('class_id').value;
    let section_id = document.getElementById('section_id').value;
    let students;
    url = Complete_url('DataApi', `/get_students?class_id=${class_id}&section_id=${section_id}`);
    students = await getRequest(url);
    
    let tbody = document.getElementById('tbody');
    tbody.innerHTML = "";
    let submit_button_area = document.getElementById('submit_button_area');
    submit_button_area.innerHTML = "";

    let tr;
    let td;
    for (let i = 0; i < students.length; i++) {
        let student = students[i]
        tr = document.createElement('tr');
        tr.setAttribute('class', 'pointer');
        td = document.createElement('td');
        td.textContent = student.roll_no;
        tr.appendChild(td);
        td = document.createElement('td');
        td.innerText = student.name;
        tr.appendChild(td);

        td = document.createElement('td');
        let marks_input = document.createElement('input');
        marks_input.setAttribute('class', 'form-control');
        marks_input.setAttribute('required', "");
        marks_input.setAttribute('type', 'number');
        marks_input.setAttribute('name', student.id);
        marks_input.setAttribute('min', 0)
        marks_input.setAttribute('max', max_marks)

        td.appendChild(marks_input);
        tr.appendChild(td);

        td = document.createElement('td');
        td.innerText = max_marks;
        tr.appendChild(td);

        tbody.appendChild(tr);
    }

    try {
        let button = document.createElement('button');
        button.setAttribute('id', 'submit_button');
        button.setAttribute('class', 'btn btn-success');
        button.innerText = 'Upload Exam';
        button.setAttribute('type', 'submit');

        submit_button_area.appendChild(button);
    }
    catch (error) {
        alert('There is Error');
        console.log(error);
    }
})

const section_id = document.getElementById('section_id');
section_id.addEventListener('change', async function (event) {
    let class_id = document.getElementById('class_id').value;
    let subjects
    url = Complete_url('DataApi', `/get_all_subjects_for_class?class_id=${class_id}&section_id=${event.target.value}`);
    subjects = await getRequest(url);
    let subject = document.getElementById('subject');
    subject.innerHTML = "";
    let option = document.createElement('option');
    option.value = "";
    option.innerText = "Subject";
    subject.appendChild(option);
    
    for (let i = 0; i < subjects.length; i++) {
        let subject_name = subjects[i].subject_name
        console.log(subject_name);
        option = document.createElement('option');
        option.value = subject_name;
        option.textContent = subject_name;
        subject.appendChild(option);
    }


      
})