import { getRequest, PostRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"


const time_table_area = document.getElementById('time-table-area')

var current_time_table = {}

async function getCurrentTimeTable() {
    time_table_area.innerHTML = "";
    const teacher_id = document.getElementById('staff_id').innerText;
    let url = Complete_url('DataApi', `/get_today_teacher_time_table?teacher_id=${teacher_id}`);
    current_time_table = await getRequest(url);
    
    
    for (let period in current_time_table){
        let period_details = current_time_table[period];
        for (let i = 0; i < period_details.length; i++) {
            let div = document.createElement('div');
            div.setAttribute('class', 'chatcontainer shadow-sm rounded col-xl-12"');
            div.style.width = "100%"

            let div_html = `
        
                <div class="mt-1 mb-1 d-flex align-items-center justify-content-between">
                <p class="float-left mb-0 text-dark btn bg-warning">${period_details[i].class}
                </p>
                </div>
                
                <div class="col-xl-11 col-lg-11">
                <h6 class="mb-0 font-weight-bold mt-2">${period_details[i].subject}</h6>
                </div>
                <div class="col-xl-12 col-lg-12">
                <small class="float-left small text-left mt-2">${period}</small>
                <small class="float-right small text-right mt-2">(${period_details[i].period_starting_time} - ${period_details[i].period_end_time} )</small>
                </div>
                <div class="clearfix"></div>
                `

            div.innerHTML = div_html;

            time_table_area.appendChild(div);
        }

    }

}

getCurrentTimeTable()