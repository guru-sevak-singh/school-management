import { getRequest, PostRequest } from "/static/js/pages_script/global_js/requst.js"

const url = "/data/get_subjects";

const all_subjects = await getRequest(url)

async function GetSubjects() {
    console.log(all_subjects);
    const subject_speciliest = document.getElementById('subject_speciliest');
    for (let i = 0; i < all_subjects.length; i++) {
        const option = document.createElement('option');
        option.value = all_subjects[i].id;
        option.text = all_subjects[i].subject_name;
        subject_speciliest.appendChild(option);
    }
    document.getElementById('subject_box').style.display = 'block';
    document.getElementById('designation_box').style.display = 'block';

}

const teacher_status = document.getElementById('staff_type');

teacher_status.addEventListener('change', async (event) => {
    if (event.target.value == 'true') {
        await GetSubjects();
    }
    else {
        // hide subjects
        console.log('hide subjects');
        document.getElementById('subject_box').style.display = 'none'
        document.getElementById('designation_box').style.display = 'none';
    }
})

const gender = document.getElementById('gender');
gender.addEventListener('change', function (event) {

    if (event.target.value == 'Female') {
        document.getElementById('merage_box').style.display = 'block';
    }
    else {
        document.getElementById('merital_status').value = 'Unmarried';
        document.getElementById('merage_box').style.display = 'none';
        document.getElementById('husband_box').value = "";
        document.getElementById('husband_box').style.display = 'none';
    }
})

const merital_status = document.getElementById('merital_status');
merital_status.addEventListener('change', function (event) {
    if (event.target.value == 'Married') {
        document.getElementById('husband_box').style.display = 'block';
    }
    else {
        document.getElementById('husband_box').value = "";
        document.getElementById('husband_box').style.display = 'none';
    }
})
