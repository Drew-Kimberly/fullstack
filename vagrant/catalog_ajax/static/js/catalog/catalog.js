/*
 */

var requestData = {};
var JSONPost;
var responseData;

$(function() {

    //Actions for on page render
    requestData = 
    {
        "action": "RenderCatalog"
    };
    
    JSONPost = JSON.stringify(requestData);
    
    process(
        JSONPost,
        function(response) {

            responseData = JSON.parse(response);

            $('#categories').replaceWith(responseData[0]);
            $('#items').replaceWith(responseData[1]);
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
        })
        .on('click', '.btn-add-item', function(e) {
            requestData =
            {
                "action": "RenderItemForm",
                "item_id": null
            };
            
            JSONPost = JSON.stringify(requestData);
            
            process(
                JSONPost,
                function(response) {

                    responseData = JSON.parse(response);

                    $('#addItem').find('#itemForm').replaceWith(responseData[0]);
                },
                null
            );
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

                    responseData = JSON.parse(response);

                    $('#categories').replaceWith(responseData[0]);
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

                    responseData = JSON.parse(response);

                    $('#categories').replaceWith(responseData[0]);
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
                    
                    responseData = JSON.parse(response);

                    $('#categories').replaceWith(responseData[0]);
                    // Response only contains Items response if it's necessary to re-render
                    if (responseData.length > 1) {
                        $('#items').replaceWith(responseData[1]);
                    }
                },
                null
            );
        })

        //Select Category
        .on('click', '.categoryLink', function(e) {
            var category_id = this.id;
            $("#items li").hide();
            $("#items").find("li[data-categoryid='" + category_id + "']").show();

            $("#categories").find("div[class='categoryWrapper activeCategory']").removeClass('activeCategory');
            $(this).parent('div').addClass('activeCategory');
        })

        //Add Item
        .on('click', '#confirmAddItem', function(e) {
            var addForm = $('#newItemForm');
            var name = addForm.find('#itemName').val();
            var category_id = addForm.find('#itemCategory').val();
            var description = addForm.find('#itemDescription').val();

            requestData =
            {
                "action": "AddItem",
                "name": name,
                "category_id": category_id,
                "description": description
            };

            JSONPost = JSON.stringify(requestData);

            process(
                JSONPost,
                function(response) {
                    responseData = JSON.parse(response);

                    $('#items').replaceWith(responseData[0]);
                },
                null
            );
        });




    $('#addCategory').on('hidden.bs.modal', function() {
        $('#newCategoryForm').find('#name').val('');
    });

    $('#addItem').on('hidden.bs.modal', function() {
        $(this).find('form').prop('id', 'itemForm');
    });
});