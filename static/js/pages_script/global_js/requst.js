export async function getRequest(url) {
    // console.log(url);
    return fetch(url)
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {

            return data;

        })
        .catch(function (error) {
            console.error('Error:', error);
            throw new Error('Failed to fetch data');
        });
}


export async function PostRequest(url, data) {
    // console.log(data);
    return fetch(url, {
        method: 'POST',
        body: data,
    })
        .then(function (response) {
            return response.json();
        })
        .then(function (data) {
            return data;
        })
        .catch(function (error) {
            console.error('Error:', error);
            throw new Error('Failed to fetch data');
        });
}

export function Complete_url(url_type, url_name) {
    let complete_url = ""
    if (url_type == "Admin_url"){
        complete_url = "/admin" + url_name
    }
    else if (url_type == 'DataApi') {
        complete_url = "/data" + url_name
    }
    else {
        alert("This Url Doesn't Exist...")
    }

    if (complete_url == "") {
        alert("This Url Doesn't Exist")
    }

    return complete_url
}
