/*
 */

var formData;
var requestData = {};
var JSONPost;
var responseData;
var uploadFile;

$(function() {
    formData = new FormData();

    //Actions for on page render
    requestData = 
    {
        "action": "RenderCatalog"
    };
    
    JSONPost = JSON.stringify(requestData);
    formData.append('request_data', JSONPost);
    
    process(
        formData,
        function(response) {

            responseData = JSON.parse(response);

            $('#categories').replaceWith(responseData[0]);
            $('#items').replaceWith(responseData[1]);
        },
        null
    );
    

    //Add/Edit/Delete onclick for modal

    $('body')

        .on('click', '#categories .btn-delete', function(e) {
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
        .on('click', '#items .btn-delete', function(e) {
            var itemID = $($(this).parents('.listItemWrapper')[0]).find('.itemLink').data('itemid');
            if ($('#deleteItemForm').find("input[name='item_id']").length == 0) {
                $('<input />').attr('type', 'hidden')
                    .attr('name', 'item_id')
                    .attr('value', itemID)
                    .appendTo('#deleteItemForm');
            }
            else {
                $('#deleteItemForm').find("input[name='item_id']").val(itemID);
            }
        })
        .on('click', '#categories .btn-edit', function(e) {
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
        .on('click', '#items .btn-edit', function(e) {
            var itemID = $($(this).parents('.listItemWrapper')[0]).find('.itemLink').data('itemid');
            formData = new FormData();
            
            requestData = 
            {
                "action": "RenderItemForm",
                "item_id": itemID
            };

            JSONPost = JSON.stringify(requestData);
            formData.append('request_data', JSONPost);

            process(
                formData,
                function(response) {

                    responseData = JSON.parse(response);

                    $('#editItem').find('#itemForm').replaceWith(responseData[0]);
                },
                null
            );
        })
        .on('click', '.btn-add-item', function(e) {
            formData = new FormData();

            requestData =
            {
                "action": "RenderItemForm",
                "item_id": null
            };
            
            JSONPost = JSON.stringify(requestData);
            formData.append('request_data', JSONPost);
            
            process(
                formData,
                function(response) {

                    responseData = JSON.parse(response);

                    $('#addItem').find('#itemForm').replaceWith(responseData[0]);
                },
                null
            );
        })
        //File Upload
        //Reference: http://www.html5rocks.com/en/tutorials/file/dndfiles/
        .on('change', '.fileInput', function(e) {
            uploadFile = e.target.files[0];
            var reader = new FileReader();

            //Show the image in the modal when it loads
            reader.onload = function(e) {
                var container = $('.imageContainer');
                container.removeClass('noImage');
                container.prepend('<img class="previewImage" src="' + e.target.result + '" />');
                container.children('#itemImageUpload').hide();
            };

            reader.readAsDataURL(uploadFile);

        });



    //Core CRUD logic

    $('body')

        //Add Category
        .on('click','#confirmAddCategory', function(e) {
            var newCategoryForm = $('#newCategoryForm');
            var nameInput = newCategoryForm.find('#name');
            var name = $.trim(nameInput.val());
            formData = new FormData();

            requestData =
            {
                "action": "AddCategory",
                "name": name
            };

            JSONPost = JSON.stringify(requestData);
            formData.append('request_data', JSONPost);

            process(
                formData,
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
            formData = new FormData();

            requestData =
            {
                "action": "EditCategory",
                "id": category_id,
                "name": name
            };

            JSONPost = JSON.stringify(requestData);
            formData.append('request_data', JSONPost);

            process(
                formData,
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
            formData = new FormData();

            idInput.remove();

            requestData =
            {
                "action": "DeleteCategory",
                "id": category_id
            };

            JSONPost = JSON.stringify(requestData);
            formData.append('request_data', JSONPost);

            process(
                formData,
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


        //View All Categories
        .on('click', '#viewAllCategories, #home', function(e) {
            $('#items').find('li').show();
            $("#categories").find("div[class='categoryWrapper activeCategory']").removeClass('activeCategory');
        })


        //Add Item
        .on('click', '#confirmAddItem', function(e) {
            formData = new FormData();
            var file_data = uploadFile ? uploadFile : null;
            var addForm = $('#newItemForm');

            requestData =
            {
                "action": "AddItem",
                "name": addForm.find('#itemName').val(),
                "category_id": addForm.find('#itemCategory').val(),
                "description": addForm.find('#itemDescription').val(),
            };

            if (file_data) {
                requestData["file_size"] = file_data.size;
                requestData["file_type"] = file_data.type;
            }

            JSONPost = JSON.stringify(requestData);

            formData.append('request_data', JSONPost);
            formData.append('file_data', file_data);

            $.ajax({
                url: '/catalog',
                type: 'POST',
                data: formData,
                cache: false,
                processData: false,
                contentType: false,
                success: function(response) {

                    responseData = JSON.parse(response);

                    $('#items').replaceWith(responseData[0]);
                },
                error: function(textStatus) {
                    alert('Errors: ' + textStatus);
                }
            });
        })


        //Select Item
        .on('click', '.btnViewItem', function(e) {
            var itemLink = $(this).parents('.itemLink')[0];
            var itemID = $(itemLink).data('itemid');
            formData = new FormData();

            requestData =
            {
                "action": "SelectItem",
                "item_id":itemID
            };

            JSONPost = JSON.stringify(requestData);

            formData.append('request_data', JSONPost);

            process(
                formData,
                function(response) {

                    responseData = JSON.parse(response);

                    $('#viewItem').find('.modal-body').replaceWith(responseData[0]);
                },
                null
            );

        })


        //Edit Item
        .on('click', '#confirmEditItem', function(e) {
            var editItemForm = $('#editItemForm');
            var itemID = editItemForm.data('itemid');
            var itemName = editItemForm.find('#itemName').val();
            var categoryID = editItemForm.find('#itemCategory').val();
            var description = editItemForm.find('#itemDescription').val();
            formData = new FormData();

            requestData =
            {
                "action": "EditItem",
                "item_id": itemID,
                "item_name": itemName,
                "category_id": categoryID,
                "description": description
            };

            JSONPost = JSON.stringify(requestData);
            formData.append('request_data', JSONPost);

            process(
                formData,
                function(response) {

                    responseData = JSON.parse(response);

                    $('#items').replaceWith(responseData[0]);
                },
                null
            );
        })


        //Delete Item
        .on('click', '#confirmDeleteItem', function(e) {
            var itemID = $('#deleteItemForm').find("input[name='item_id']").val();
            formData = new FormData();

            requestData =
            {
                "action":"DeleteItem",
                "item_id":itemID
            };

            JSONPost = JSON.stringify(requestData);
            formData.append('request_data', JSONPost);

            process(
                formData,
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

    $('#editItem').on('hidden.bs.modal', function() {
        $(this).find('form').prop('id', 'itemForm');
    });
});