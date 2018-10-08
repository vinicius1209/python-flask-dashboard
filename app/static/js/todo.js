/********************************** DOCUMENT ******************************************************/
$(document).ready(function() {
    $("#mySearch").on("keyup", function() {
        var value = $(this).val().toLowerCase();
            $("#drag-elements *").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
   });
   
});

/********************************** DRAGULA ******************************************************/

//primeiro param sao os container, o segundo as options, e no final o .on que s�o os eventos
dragula(
    [document.querySelector('#drag-elements'), document.querySelector('#drag-target')], {
        invalid: function(el, handle) {
            return el.classList.contains('legend'); //desconsidero o tipo da classe legend
        },

        accepts: function(el, target, source, sibling) {
            if (target.id == 'drag-elements') { //se vai jogar na div de "a fazer" tudo bem...
                return true;
            } else {
                if ((target.childNodes.length) < 2) {
                    return true; //Pode dropar
                } else {
                    return false;
                }
            }
        }
    }
).on('drop', function(el, source) { //quando dropar, condiciona os tipos das classes dos cards
    if (el.classList.contains('bg-info')) {
        if (source.id == 'drag-target') {
            el.className = el.className.replace('info', 'warning');
            start_timer();
        }
    } else if (el.classList.contains('bg-warning')) {
        if (source.id == 'drag-elements') {
            el.className = el.className.replace('warning', 'info');
            pause_timer();
        }
    }
});

/***************************************** TIMER **********************************************/

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