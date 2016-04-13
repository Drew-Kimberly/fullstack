/*
Global JS Functions
 */

function process(requestJsonData, successCallback, errorCallback) {

    $.ajax(
    {
        url: "/catalog",
        type: "POST",
        data: requestJsonData,
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