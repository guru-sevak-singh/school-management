import { getRequest, PostRequest } from "/static/js/pages_script/global_js/requst.js"


const class_input = document.getElementById('class_id');
var sections;
// var sections = await getRequest('/data/get_section?class_id=' + class_input.value);
// console.log(sections)

function SetSections(sections) {
    var section_element = document.getElementById('section_id')
    section_element.innerHTML = ""

    for (let n in sections){
        const option = document.createElement('option')
        option.value = sections[n].id;
        option.innerText = sections[n].section_name;
        section_element.appendChild(option)
    }
}

// SetSections(sections)

class_input.addEventListener('change', async (event) => {
    const selectedOption = event.target.value;
    sections = await getRequest('/data/get_section?class_id=' + selectedOption);
    SetSections(sections)
});

