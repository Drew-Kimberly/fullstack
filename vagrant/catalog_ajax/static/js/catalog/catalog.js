/*
 */

var requestData = {};
var JSONPost;
var responseData;

$(function() {

    requestData = 
    {
        "action": "GetCategories"
    };
    
    JSONPost = JSON.stringify(requestData);
    
    process(
        JSONPost,
        function(response) {
            $('#categories').replaceWith(response);
        },
        null
    );


    /*$('.testLink').click(function() {

        requestData =
        {
            "action": "testAjax",
            "id": this.id,
            "drew": "Drew is King of AJAX"
        };

        JSONPost = JSON.stringify(requestData);

        process(
            JSONPost,
            function(response) {
                $('#items').append(response);
            },
            null
        );
    });*/
});