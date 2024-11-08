// Importing multiple values
import { getRequest } from "/static/js/pages_script/global_js/requst.js"

export function SetAllClasses(clases) {
    class_input.innerHTML = "";
    let html_text = "";

    for (let n in clases) {
        let clas = clases[n];
        html_text += "<option value='" + clas.id + "'>" + clas.class_name + "</option>"
    }

    class_input.innerHTML = html_text;

}

export function SetAllSection(sections) {
    const all_section_input = document.getElementById('section_id');
    all_section_input.innerHTML = "";
    let html_text = "<option value=''> Chose Section </option>";

    for (let n in sections) {

        let section = sections[n];
        html_text += "<option value='" + section.id + "'>" + section.section_name + "</option>";
    }

    all_section_input.innerHTML = html_text

}

export function SetSelectedValue() {
    let home_url = window.location.href;
    let urlObject = new URL(home_url);
    let class_id = urlObject.searchParams.get('class_id');
    document.getElementById('class_id').value = class_id

    if (class_id != undefined) {
    

        let section_id = urlObject.searchParams.get('section_id');
        document.getElementById("section_id").value = section_id;

    }

}



const class_input = document.getElementById('class_id');

class_input.addEventListener('change', async (event) => {
    let selected_class_id = event.target.value;
    if (selected_class_id == "") {
        all_sections = await getRequest('/data/get_all_sections');
    }
    else {
        all_sections = await getRequest('/data/get_section?class_id=' + selected_class_id);
    }

    SetAllSection(all_sections);
})

var all_classes = await getRequest('/data/get_all_clases');

var all_sections = await getRequest('/data/get_all_sections');


SetAllClasses(all_classes);

SetAllSection(all_sections);

SetSelectedValue()

