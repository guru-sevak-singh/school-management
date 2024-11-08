import { getRequest, PostRequest } from "/static/js/pages_script/global_js/requst.js"


const session_year_dropdown = document.getElementById('session_year');

const home_url = window.location.href

const perms = new URLSearchParams(new URL(home_url).search)
const running_year = perms.get('session_year')

if (running_year == null) {
    console.log('nothing')
}
else {
    session_year_dropdown.value = running_year
}

session_year_dropdown.addEventListener('change', function (event) {
    let selected_year = event.target.value;

    let url = window.location.href;
    let urlObject = new URL(url);
    urlObject.searchParams.set('session_year', selected_year);
    let modifiedUrl = urlObject.toString();

    window.open(modifiedUrl, self);




})



const class_input = document.getElementById('class_id');

var sections = await getRequest('/data/get_section?class_id=' + class_input.value);

function SetSections(sections) {
    var section_element = document.getElementById('section');
    section_element.innerHTML = "";

    for (let n in sections) {
        const option = document.createElement('option');
        option.value = sections[n].id;
        option.innerText = sections[n].section_name;
        section_element.appendChild(option);
    }
}


SetSections(sections);


class_input.addEventListener('change', async function (event) {
    const selectedOption = event.target.value;
    sections = await getRequest('/data/get_section?class_id=' + selectedOption);
    SetSections(sections);
})

