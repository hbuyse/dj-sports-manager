$(".custom-file-input").change(function () {
    var fieldVal = $(this).val();
    console.log(fieldVal)

    // Change the node's value by removing the fake path (Chrome)
    fieldVal = fieldVal.replace("C:\\fakepath\\", "");
    console.log($(this).attr('id') + " changed with new value: " + fieldVal);

    if (fieldVal != undefined || fieldVal != "") {
        // Change the value to show it to user
        $(this).next(".custom-file-label").text(fieldVal);
    }
});
