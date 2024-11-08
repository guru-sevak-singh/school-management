import {WriteCurrentPageSerialNumber} from '/static/js/pages_script/all_student.js'

var students_detail = [];

function ShowStudents(students_detail){
    const table_body = document.getElementsByTagName('tbody')[0];
    table_body.innerHTML = "";
    for (let i=0; i < students_detail.length; i++){
        const student_detail = students_detail[i];
        var tr = document.createElement('tr');
        var td = document.createElement('td');
        td.setAttribute('class', 's_no');
        tr.appendChild(td);

        for (let detail in student_detail) {
            td=document.createElement('td');
            if (detail == 'action'){
                const a = document.createElement('a')
                a.setAttribute('href', student_detail[detail])
                a.innerText = 'View'
                td.appendChild(a);
                tr.appendChild(td);
            }
            else{
                td.innerText = student_detail[detail];
                tr.appendChild(td)
            }

        }

        table_body.append(tr);
    }
    
    WriteCurrentPageSerialNumber()
    // alert('kaam ho gya h...')
}

function SaveVisibleData () {
    let VisibleData = []
    const table_body = document.getElementsByTagName('tbody')[0];
    const trs = table_body.getElementsByTagName('tr');

    for (let i=0; i < trs.length; i++) {
        let tr = trs[i];
        VisibleData.push({"name": tr.getElementsByTagName('td')[1].innerText, "father_name": tr.getElementsByTagName('td')[2].innerText, "mother_name": tr.getElementsByTagName('td')[3].innerText, "admision_number": tr.getElementsByTagName('td')[4].innerText, "class": tr.getElementsByTagName('td')[5].innerText, "action": tr.getElementsByTagName('a')[0].href})
    }
    return VisibleData;

}

students_detail = SaveVisibleData();

function SortAscending(key) {
    console.log('old visible data');
    console.log(students_detail);

    students_detail.sort((a, b) => {
        // Convert names to lowercase to ensure case-insensitive sorting
        const nameA = a[key].toLowerCase();
        const nameB = b[key].toLowerCase();
    
        if (nameA > nameB) {
            return -1;
        }
        if (nameA < nameB) {
            return 1;
        }
        return 0; // Names are equal
    });
    
    console.log('New Visible data');
    console.log(students_detail);
    return students_detail
}

function SortDescending(key) {
    console.log('old visible data');
    console.log(students_detail);

    students_detail.sort((a, b) => {
        // Convert names to lowercase to ensure case-insensitive sorting
        const nameA = a[key].toLowerCase();
        const nameB = b[key].toLowerCase();
    
        if (nameA > nameB) {
            return -1;
        }
        if (nameA < nameB) {
            return 1;
        }
        return 0; // Names are equal
    });
    
    console.log('New Visible data');
    console.log(students_detail);
}

document.getElementById('sort_by_name').addEventListener('click', ()=>{
    const visible_details = SortAscending('mother_name');
    ShowStudents(visible_details);
})

