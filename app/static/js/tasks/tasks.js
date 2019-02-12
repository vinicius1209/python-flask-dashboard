/************************ DOCUMENT *************************************/
//Barra de pesquisa para pesquisar os componentes na table
$(document).ready(function () {

    $("#mySearch").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#myTask tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });

    //Busca pelo click no tr da table, o id da tarefa, ou seja, coluna 0
    $("#myTask tr").on("click", function () {
        var task_id = $(this).find("td").eq(0).text();
        var modal = '#modalTask' + task_id;
        $(modal).modal();
        //window.open('/ncs', '_blank');
    });
});

/*************************** UTILS *******************************/

//Tooltip para cada linha da tabela
$('[data-toggle="tooltip"]').tooltip();

//Obrigado Leonardo
$('.modal').on('shown.bs.modal', function () {
    $(this).find("#id").trigger('focus')
})

//Nav-item do tipo forum
$('.nav-forum').on('click', function (e) {
    var tarefa = $(this).attr("value");
    $.ajax({
        url: "/modalforum/" + tarefa,
        type: 'GET',
        beforeSend: function () {
            console.log('Buscando forum para tarefa = ' + tarefa)
        },
        success: function (res) {
            document.getElementById('nav-forum'+tarefa).innerHTML = '';
            for (var x = 0; x < res.length; x++){
                var card_forum = 
                '<div class="card" style="margin-top: 1rem;"> ' +
                    '<h5 class="card-header">De: ' + res[x].usuario + '</h5> ' +
                    '<div class="card-body"> ' +
                        '<blockquote class="blockquote mb-0"> ' +
                            '<pre>'+ res[x].comentario + '</pre> ' +
                            '<footer class="blockquote-footer"> ' +
                                ' Respondida em ' + 
                                '<cite title="Source Title"> ' + res[x].dt_cadastro + '</cite> ' +
                            '</footer> ' +
                        '</blockquote> ' +
                    '</div> ' +
                '</div> ';
            document.getElementById('nav-forum'+tarefa).innerHTML += card_forum;
            }
            document.getElementById('nav-forum'+tarefa).innerHTML +=
                '<div style="margin-top: 1rem;"> ' +
                    '<a class="btn btn-outline-secondary btn-block" target="_blank" href="forum/' + tarefa + '">...</a>' +
                '</div>';
        },
        complete: function (data) {
            console.log('finalizou...');
        }
    });
})

//Nav-item do tipo Anexo
$('.nav-anexo').on('click', function (e) {
    var tarefa = $(this).attr("value");
    console.log(tarefa)
})