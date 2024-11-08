const attendence_type = document.getElementById('attendence_type');

attendence_type.addEventListener('change', function(event){
    const attendence_date_input = document.getElementById('attendence_date');
    if (event.target.value == 'Daily') {
        attendence_date_input.value = "";
        attendence_date_input.type = 'date';
    }
    else {
        attendence_date_input.value = "";
        attendence_date_input.type = 'month';
    }
})