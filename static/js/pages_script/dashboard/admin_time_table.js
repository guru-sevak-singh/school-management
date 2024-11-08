import { getRequest, PostRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"


const time_table_area = document.getElementById('time-table-area')

var current_time_table = {}

async function getCurrentTimeTable() {
    time_table_area.innerHTML = "";
    let url = Complete_url('DataApi', '/get_current_time_table')
    current_time_table = await getRequest(url);
    console.log(current_time_table);
    let period_name = Object.keys(current_time_table)[0]
    console.log(period_name);
    console.log(current_time_table[period_name])
    console.log('now going to run the loop');
    for (let i = 0; i < current_time_table[period_name].length; i++) {
        console.log(i)
        try {
            console.log(current_time_table[period_name][i])
            let div = document.createElement('div');
            div.setAttribute('class', 'chatcontainer shadow-sm rounded col-xl-12"');
            div.style.width = "100%"

            let div_html = `
        
                <div class="mt-1 mb-1 d-flex align-items-center justify-content-between">
                <p class="float-left mb-0 text-dark btn bg-warning">${current_time_table[period_name][i].class}
                </p>
                </div>
                
                <div class="col-xl-11 col-lg-11">
                <h6 class="mb-0 font-weight-bold mt-2">${current_time_table[period_name][i].subject}</h6>
                </div>
                <div class="col-xl-12 col-lg-12">
                <small class="float-left small text-left mt-2">${current_time_table[period_name][i].teacher}</small>
                <small class="float-right small text-right mt-2">${period_name} </small>
                </div>
                <div class="clearfix"></div>
                `

            div.innerHTML = div_html;

            time_table_area.appendChild(div);


        }
        catch (error) {
            console.log(error.message)
        }
    }
}

getCurrentTimeTable()