import { getRequest, PostRequest, Complete_url } from "/static/js/pages_script/global_js/requst.js"


async function get_all_notice() {
    let url = Complete_url('DataApi', '/get_all_notice')
    let all_notice_data = await getRequest(url);

    return all_notice_data;
}

var all_notice = await get_all_notice();
ShowAllNotice(all_notice)

function start_countdown() {
    interval = setInterval(() => {
    let notice_counts = document.getElementsByClassName('notice_minutes');
    console.log(notice_counts.length)

    if (notice_counts.length == 0) {
        clearInterval(interval);
    }
    else {
        for (let i = 0; i < notice_counts.length; i++) {
            let notice_minute = notice_counts[i];
            notice_minute = notice_minute.innerText;
            notice_minute = notice_minute.replace("minutes ago", "");
            
            notice_minute = Number(notice_minute);
            notice_minute += 1;

            notice_counts[i].innerText = `${notice_minute} minutes ago`

        }
    }
        
    }, 60000);
    
}

function ShowAllNotice(all_notice_data) {
    const notice_board = document.getElementById('notice_board');

    for (let i = 0; i < all_notice_data.length; i++) {
        let div = document.createElement('div');
        div.setAttribute('class', 'chatcontainer shadow-sm rounded col-xl-12"');
        div.style.width = "100%"

        let div_html = `
        
        <div class="mt-1 mb-1 d-flex align-items-center justify-content-between">
        <p class="float-left mb-0 text-dark btn bg-warning">${all_notice_data[i].notice_date}
        </p>
    </div>
    
    <div class="col-xl-11 col-lg-11">
    <h6 class="mb-0 font-weight-bold mt-2">${all_notice_data[i].notice}</h6>
    </div>
    `
    
    if (window.location.href.includes("notice")){

        div_html += `<a href='${all_notice[i].delete_url}' class="float-right col-xl-1 col-lg-1 text-white btn btn-info del_button">Delete</a>`
    } 

    div_html += `
    <div class="col-xl-12 col-lg-12">
    <small class="float-left small text-left mt-2 notice_minutes">${all_notice_data[i].time} </small>
    <small class="float-right small text-right mt-2">By:- ${all_notice_data[i].assigned_by} </small>
    </div>
    <div class="clearfix"></div>
        `
        div.innerHTML = div_html;
        notice_board.appendChild(div);


    }

    // start_countdown()

}
