var timer = new Timer();

    timer.addEventListener('secondsUpdated', function (e) {
        $('#timerTask').html(timer.getTimeValues().toString());
    });

function start_timer(){
    timer.start();
}

function pause_timer(){
    timer.pause();
}