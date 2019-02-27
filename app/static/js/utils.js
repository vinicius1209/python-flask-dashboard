
//Evento da barra de pesquisa
$("#mySearch").on("keyup", function () {
    var value = $(this).val().toLowerCase();
    $("#tableListTasksNcs tr").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
});

//Busca pelo click no tr da table, o id da tarefa, ou seja, coluna 0
$("#tableListTasksNcs tr").on("click", function () {
    var task_id = $(this).find("td").eq(0).text();
    var modal = '#modalDefault' + task_id;
    $(modal).modal();
});

//Tooltip para cada linha da tabela
$('[data-toggle="tooltip"]').tooltip();

//Setar o focus no campo ID quando abrir o modal
$('.modal').on('shown.bs.modal', function () {
    $(this).find("#id").trigger('focus')
})

//Nav-item do tipo forum
$('.nav-forum').on('click', function (e) {
    var tarefa = $(this).attr("value");
     $("#loader").show();
     setTimeout(function() {
        getForumAndAppendHtml(tarefa);
     }, 2000);
})

function getForumAndAppendHtml(tarefa){
    $.ajax({
        url: "/modalforum/" + tarefa,
        type: 'GET',
        success: function (res) {
            var cards = '';
            var footer = '';
            var header =
            '<div class="container"> ' +
                '<div style="margin-bottom: 1rem;"> ' +
                    '<div class="accordion" id="accordion' + tarefa + '" >' +
                    '<a class="btn btn-outline-secondary btn-block" role="button" data-toggle="collapse" data-target="#collapse' + tarefa + '" aria-expanded="true" aria-controls="collapseOne"> Inserir </a> ' +
                            '<div id="collapse' + tarefa +  '" class="collapse" aria-labelledby="headingOne" data-parent="#accordion' + tarefa + '"> ' +
                                '<div class="card" style="margin-top: 1rem;"> ' +
                                    '<div class="card-body"> ' +
                                        '<textarea class="form-control" id="novaMensagemForum" style="margin-bottom: 1rem;" name="mensagem" value=""  required="" autofocus></textarea> ' +
                                        '<a href="modalforum/' + tarefa + '" class="btn btn-outline-secondary">Publicar</a> ' +
                                    '</div> ' +
                                '</div> ' +
                            '</div> ' +
                    '</div> ' +
                '</div>';

            for (var x = 0; x < res.length; x++) {
                cards +=
                    '<div class="card" style="margin-top: 1rem;"> ' +
                        '<h5 class="card-header">De: ' + res[x].usuario + '</h5> ' +
                            '<div class="card-body"> ' +
                                '<blockquote class="blockquote mb-0"> ' +
                                '<pre>' + res[x].comentario + '</pre> ' +
                                '<footer class="blockquote-footer"> ' +
                                    ' Respondida em  <cite title="Source Title"> ' + res[x].dt_cadastro + '</cite> ' +
                                '</footer> ' +
                                '</blockquote> ' +
                            '</div> ' +
                    '</div> ';
            }
            footer =
                    '<div style="margin-top: 1rem;"> ' +
                        '<a class="btn btn-outline-secondary btn-block" target="_blank" href="forum/' + tarefa + '">...</a>' +
                    '</div> ' +
                   '</div>';
            document.getElementById('nav-forum' + tarefa).innerHTML = header + cards + footer;
        }
    });
}