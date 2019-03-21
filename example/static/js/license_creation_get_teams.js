$("#id_category").change(function () {
    // get the url of the `load_cities` view
    var url = $("#licenseForm").attr("data-teams-url");

    // get the selected player ID from the HTML input
    var categoryId = $(this).val();
    var playerId   = $("#id_player").val();
    console.log("Category ID changed to " + categoryId);

    // initialize an AJAX request
    $.ajax({
        // set the url of the request (= localhost:8000/hr/ajax/load-cities/)                  
        url : url,
        data: {
            // add the category and player ids to the GET parameters
            'category': categoryId,
            'player'  : playerId,
        },
        // `data` is the return of the `load_cities` view function
        success: function (data) {
            console.log(data);
            // replace the contents of the city input with the data that came from the server
            $("#div_id_teams div").html(data);
            $("#div_id_teams").show();
        }
    });
});