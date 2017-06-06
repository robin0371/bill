// JS-шаблон создания денежного перевода
$(document).on("submit", "form", function(event)
{
    event.preventDefault();
    $.ajax({
        url: $(this).attr("action"),
        type: $(this).attr("method"),
        dataType: "JSON",
        data: new FormData(this),
        processData: false,
        contentType: false,
        success: function (data, status)
        {
             $("#info").removeClass("alert alert-info alert-danger alert-success");

             if (data.success == 'true') {
                $("#info").addClass("alert alert-success");
             } else {
                $("#info").addClass("alert alert-danger");
             }

             $("#info")["0"].innerText = data.message;
        },
        error: function (xhr, desc, err)
        {
             $("#info").addClass("alert alert-danger");
             $("#info")["0"].innerText = "Непредвиденная ошибка";
        }
    });
});