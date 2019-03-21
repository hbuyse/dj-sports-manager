$("#id_player").change(function () {
    // get the url of the `load_cities` view
    var url = $("#licenseForm").attr("data-categories-url");

    // get the selected country ID from the HTML input
    var playerId = $(this).val();
    console.log("Player ID changed to " + playerId);

    // initialize an AJAX request
    $.ajax({
        // set the url of the request (= localhost:8000/hr/ajax/load-cities/)                  
        url : url,
        data: {
            // add the country id to the GET parameters
            'player': playerId
        },
        // `data` is the return of the `load_cities` view function
        success: function (data) {
            console.log(data);
            // replace the contents of the city input with the data that came from the server
            $("#id_category").html(data);
            $("#div_id_category").show();
        }
    });
});