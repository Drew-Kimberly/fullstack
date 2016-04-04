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
    

    $('body')

        //Add/Edit/Delete onclick for modal

        .on('click', '.btn-add', function(e) {
            $('.add-confirm').prop('id', $(this).data('add'));
        })
        .on('click', '.btn-edit', function(e) {
            //var category_name = $(this).parent().find('.categoryLink')[0].text;
            $('.edit-confirm').prop('id', $(this).data('edit'));
            //$('#editCategory.editCategoryForm#name').val(category_name);
        })
        .on('click', '.btn-delete', function(e) {
            $('.delete-confirm').prop('id', $(this).data('delete'));
        })


        //Core CRUD logic


        //Add Category logic
        .on('click','#btnAddCategory', function(e) {
            var name = $('#name').val();

            requestData =
            {
                "action": "AddCategory",
                "name": name
            };

            JSONPost = JSON.stringify(requestData);

            process(
                JSONPost,
                function(response) {
                    $('#categories').replaceWith(response);
                },
                null
            );
        })


        //Edit Category Logic
        .on('click', '#confirmEditCategory', function(e) {
            var category_id = $(this).parent().find('.categoryLink')[0].id;

            requestData =
            {
                "action": "EditCategory",
                "id": category_id
            };

            JSONPost = JSON.stringify(requestData);

            process(
                JSONPost,
                function(response) {

                },
                null
            );
        })


        //Delete Category Logic
        .on('click', '#confirmDeleteCategory', function(e) {
            var category_id = $(this).parent().find('.categoryLink')[0].id;

            requestData =
            {
                "action": "DeleteCategory",
                "id": category_id
            };

            JSONPost = JSON.stringify(requestData);

            process(
                JSONPost,
                function(response) {

                },
                null
            );
        });
});