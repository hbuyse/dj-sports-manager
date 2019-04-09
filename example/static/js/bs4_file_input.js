$(".custom-file-input").change(function () {
    var fieldVal = $(this).val();

    // Change the node's value by removing the fake path (Chrome)
    fieldVal = fieldVal.replace("C:\\fakepath\\", "");

    if (fieldVal != undefined || fieldVal != "") {
        // Change the value to show it to user
        $(this).next(".custom-file-label").text(fieldVal);
    }
});

// When the page is ready and that we found a 
$( document ).ready(function() {
    $("input.custom-file-input").each(function( index ) {
        var url = $(this).attr("data-onload");
        if (url !== undefined && url != "") {
            var prepend = `<div class="input-group-prepend"><a target="_blank" href="` + url + `" class="btn btn-outline-secondary" type="button">Download</a></div>`
            $(this).closest(".input-group").prepend(prepend);
            $(this).next(".custom-file-label").text(url.replace(/.*\//, ''));
        }
    });
});