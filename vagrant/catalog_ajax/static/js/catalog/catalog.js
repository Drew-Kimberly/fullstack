/*
 */

var requestData = {};
var JSONPost;
var responseData;

$(function() {

    //Actions for on page render
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


    //Add/Edit onclick logic
    $('.btn-add').on('click', function(e) {
        $('add-confirm').prop('id', $(this).data('add'));
    });


    //Add Category logic
    $('#btnAddCategory').on('click', function(e) {
        var name = "";

        requestData =
        {
            "action": "AddCategory",
            "name": name
        };
    });
});