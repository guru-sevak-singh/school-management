import { getRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"


var table = $('#example').DataTable();

const min_id = document.getElementById('min_id').innerText;

var sr_no = 0

try {
    var s_no_columns = document.getElementsByClassName('s_no')
    for (let n=0; n < s_no_columns.length; n++) {
        sr_no += 1
        s_no_columns[n].textContent = sr_no;
    }

}
catch (error) {
    alert(error.message);
    console.log(error.message)

}

setTimeout(() => {
    element = document.getElementsByName('example_length')[0].parentElement.parentElement.parentElement.parentElement.style.display = 'none';
    console.log(element);
}, 10);


var old_url = window.location.href;
var url = old_url.split("?")
url = url[url.length - 1]
url = Complete_url('DataApi', `/get_remaining_staff_list?min_id=${min_id}&${url}`)

console.log(url);

const remaining_data = await getRequest(url)

for (let i = 0; i < remaining_data.length; i++) {
    sr_no += 1;
    var newData = [
        sr_no,
        remaining_data[i].name,
        remaining_data[i].father_name,
        remaining_data[i].designation,
        // / Create a link for the URL
        '<a href="' + remaining_data[i].action_url + '"><i class="fa fa-eye"></i> View </a>'
    ];
    table.row.add(newData).draw();
}

