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
    

    //Add/Edit/Delete onclick for modal

    $('body')

        .on('click', '.btn-delete', function(e) {
            var category_id = $(this).parent().find('.categoryLink')[0].id;
            if ($('#deleteCategoryForm').find("input[name='category_id']").length == 0) {
                $('<input />').attr('type', 'hidden')
                    .attr('name', 'category_id')
                    .attr('value', category_id)
                    .appendTo('#deleteCategoryForm');
            }
            else {
                $('#deleteCategoryForm').find("input[name='category_id']").val(category_id);
            }
        })
        .on('click', '.btn-edit', function(e) {
            var categoryLink = $(this).parent().find('.categoryLink')[0];
            var category_id = categoryLink.id;
            if ($('#editCategoryForm').find("input[name='category_id']").length == 0) {
                $('<input />').attr('type', 'hidden')
                    .attr('name', 'category_id')
                    .attr('value', category_id)
                    .appendTo('#editCategoryForm');
            }
            else {
                $('#editCategoryForm').find("input[name='category_id']").val(category_id);
            }

            var category_name = $.trim(categoryLink.text);
            $('#editCategoryForm').find('input#name').val(category_name);
        });



    //Core CRUD logic

    $('body')

        //Add Category
        .on('click','#confirmAddCategory', function(e) {
            var newCategoryForm = $('#newCategoryForm');
            var nameInput = newCategoryForm.find('#name');
            var name = $.trim(nameInput.val());
            //nameInput.val('');

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


        //Edit Category
        .on('click', '#confirmEditCategory', function(e) {
            var editForm = $('#editCategoryForm');
            var idInput = editForm.find("input[name='category_id']");
            var nameInput = editForm.find('input#name');

            var category_id = idInput.val();
            idInput.remove();
            var name = $.trim(nameInput.val());

            requestData =
            {
                "action": "EditCategory",
                "id": category_id,
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


        //Delete Category
        .on('click', '#confirmDeleteCategory', function(e) {
            var deleteForm = $('#deleteCategoryForm');
            var idInput = deleteForm.find("input[name='category_id']");
            var category_id = idInput.val();
            idInput.remove();

            requestData =
            {
                "action": "DeleteCategory",
                "id": category_id
            };

            JSONPost = JSON.stringify(requestData);

            process(
                JSONPost,
                function(response) {
                    $('#categories').replaceWith(response);
                },
                null
            );
        });




    $('#addCategory').on('hidden.bs.modal', function() {
        $('#newCategoryForm').find('#name').val('');
    })
});