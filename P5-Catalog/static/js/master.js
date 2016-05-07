/*
Global JS Functions
 */

function process(formData, successCallback, errorCallback) {

    $.ajax(
    {
        url: "/catalog",
        type: "POST",
        data: formData,
        cache: false,
        processData: false,
        contentType: false,
        dataType: 'json',
        success: function (response) {
            if (successCallback != null) {
                successCallback(response);
            }
        },
        error: function (error) {
            alert(error.status + ' error occured!');

            if (errorCallback != null) {
                errorCallback(error);
            }
        }
    });
}