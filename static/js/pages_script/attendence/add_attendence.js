import { getRequest } from "/static/js/pages_script/global_js/requst.js"

const all_classes = await getRequest('/data/get_all_clases')
console.log(all_classes);


function AddClassSelect() {
    var class_selection = `
    <div class="item form-group">
        <label class="col-form-label col-md-5 col-sm-5 label-align" for="class"> Class
            <span class="required">*</span>
        </label>
        <div class="col-md-7 col-sm-7">
    
            <select type="text" class="form-control" id="class" name="class">
    
    `

    for (let i = 0; i < all_classes.length; i++) {
        class_selection += `<option value='` + all_classes[i].id + `'>` + all_classes[i].class_name + `</option>`
    }
    class_selection += `
    </select>
    </div>
    </div>
    `

    var div = document.createElement('div');
    div.setAttribute('class', 'col-md-4 col-sm-4 form-group has-feedback');
    div.innerHTML = class_selection;
    document.getElementById('detail_form').appendChild(div);

}

async function AddSection() {
    try {
        document.getElementsByTagName('tbody')[0].remove();
    }
    catch (error) {
        console.log(error);
    }
    try {
        document.getElementById('section_box').remove();
    }
    catch (error) {
        console.log(error.message);
    }
    try {
        document.getElementById('submit_form').remove();
    }
    catch (error) {
        console.log(error.message);

    }
    const selected_class = document.getElementById('class').value;

    if (selected_class == 'teachers') {
        const thead = document.getElementsByTagName('thead')[0];
        thead.innerHTML = "";
        thead.innerHTML = `
                        <tr class="headings">
                            <th class="column-title">Roll Number </th>
                            <th class="column-title">Name </th>
                            <th class="column-title">Father Name </th>
                            <th class="column-title"><span class="nobr">Attendence</span>
                            </th>
                        </tr>
                    `
        const table = document.getElementsByTagName('table')[0];

        try {

            const tbody = table.getElementsByTagName('tbody')[0];
            tbody.remove();
            const submit_button = document.getElementById('submit_form')
            submit_button.remove()
        }
        catch {
            // 
        }

        var students = await getRequest('/data/get_attendence?request_for=Teachers')
        if (students.length == 0){
            students = await getRequest('/data/get_teachers')
        }

        var tbod = document.createElement('tbody')


        for (let i = 0; i < students.length; i++) {
            let student = students[i];
            let tr = document.createElement('tr');
            tr.setAttribute('class', 'pointer');
            let td = document.createElement('td');
            td.innerText = student.roll_no;
            tr.appendChild(td);
            td = document.createElement('td');
            td.innerText = student.name;
            tr.appendChild(td);

            td = document.createElement('td');
            td.innerText = student.father_name;
            tr.appendChild(td)

            td = document.createElement('td');
            let select = document.createElement('select');
            select.setAttribute('class', 'form-control');
            select.setAttribute('name', student.id);

            let option = document.createElement('option');
            option.value = 'Present';
            option.innerText = 'Present';

            select.appendChild(option);

            option = document.createElement('option');
            option.value = 'Absent';
            option.innerText = 'Absent';
            select.appendChild(option);

            option = document.createElement('option');
            option.value = 'Leave';
            option.innerText = "Leave";

            select.appendChild(option);

            option = document.createElement('option');
            option.value = 'Half Day';
            option.innerText = 'Half Day';
            select.appendChild(option);

            option = document.createElement('option')
            option.value = 'One Third';
            option.innerText = 'One Third';
            select.appendChild(option);

            td.appendChild(select);


            if (student.present_status != undefined) {
                select.value = student.present_status;
            }


            tr.appendChild(td);

            tbod.appendChild(tr);


        }

        table.appendChild(tbod);

        const button = document.createElement('button');
        button.setAttribute('id', 'submit_form');
        button.type = 'submit';
        button.setAttribute('class', 'btn btn-primary');
        button.innerText = 'Add Attendence';

        const form = document.getElementsByTagName('form')[0];
        form.appendChild(button);


    }
    else {

        const sections = await getRequest('/data/get_section?class_id=' + selected_class);

        var section_selection = `<div class="item form-group">
                                    <label class="col-form-label col-md-5 col-sm-5 label-align" for="class"> Section
                                        <span class="required">*</span>
                                    </label>
                                    <div class="col-md-7 col-sm-7">

                                <select type="text" class="form-control" id="section" name="section">
                                <option value=""> Choose Section</option>`

        for (let i = 0; i < sections.length; i++) {
            section_selection += "<option value='" + sections[i].id + "'>" + sections[i].section_name + "</option>"
        }
        section_selection += "</select> </div> </div>"
        var div = document.createElement('div');
        div.setAttribute('id', 'section_box')
        div.setAttribute('class', 'col-md-4 col-sm-4 form-group has-feedback');
        div.innerHTML = section_selection;
        document.getElementById('detail_form').appendChild(div);

        const SectionSelect = document.getElementById('section')
        SectionSelect.addEventListener('change', async () => {
            await AddStudents()

        })

    }
}

async function AddStudents() {
    const thead = document.getElementsByTagName('thead')[0];
    thead.innerHTML = "";
    thead.innerHTML = `
                        <tr class="headings">
                            <th class="column-title">Roll Number </th>
                            <th class="column-title">Name </th>
                            <th class="column-title">Father Name </th>
                            <th class="column-title"><span class="nobr">Attendence</span>
                            </th>
                        </tr>
    `
    const table = document.getElementsByTagName('table')[0];
    const class_id = document.getElementById('class').value;
    const section_id = document.getElementById('section').value;

    try {

        const tbody = table.getElementsByTagName('tbody')[0];
        tbody.remove();
        const submit_button = document.getElementById('submit_form')
        submit_button.remove()
    }
    catch {
        // 
    }

    let student_url = `/data/get_attendence?request_for=SingleClass&class_id=${class_id}&section_id=${section_id}`
    var students = await getRequest(student_url)

    console.log(students)
    if (students.length == 0) {
        student_url = '/data/get_students?class_id=' + class_id + '&section_id=' + section_id;
        var students = await getRequest(student_url);

    }
    var tbod = document.createElement('tbody')


    for (let i = 0; i < students.length; i++) {
        let student = students[i];
        let tr = document.createElement('tr');
        tr.setAttribute('class', 'pointer');
        let td = document.createElement('td');
        td.innerText = student.roll_number;
        tr.appendChild(td);
        td = document.createElement('td');
        td.innerText = student.name;
        tr.appendChild(td);

        td = document.createElement('td');
        td.innerText = student.father_name;
        tr.appendChild(td)

        td = document.createElement('td');
        let select = document.createElement('select')
        select.setAttribute('class', 'form-control')
        select.setAttribute('name', student.id)

        let option = document.createElement('option')
        option.value = 'Present'
        option.innerText = 'Present'

        select.appendChild(option);

        option = document.createElement('option')
        option.value = 'Absent'
        option.innerText = 'Absent'
        select.appendChild(option)

        option = document.createElement('option');
        option.value = 'Leave';
        option.innerText = "Leave";

        select.appendChild(option);

        td.appendChild(select)


        if (student.present_status != undefined) {
            select.value = student.present_status;
        }

        tr.appendChild(td);

        tbod.appendChild(tr);


    }

    table.appendChild(tbod);

    const button = document.createElement('button');
    button.setAttribute('id', 'submit_form');
    button.type = 'submit';
    button.setAttribute('class', 'btn btn-primary');
    button.innerText = 'Add Attendence';

    const form = document.getElementsByTagName('form')[0];
    form.appendChild(button);

}

AddClassSelect()

const class_select = document.getElementById('class')

class_select.addEventListener('change', async (event) => {
    await AddSection();
})