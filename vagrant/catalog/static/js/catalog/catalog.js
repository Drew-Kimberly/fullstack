/*
 */

ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif'];

var formData;
var requestData = {};
var JSONPost;
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
            $('#categories').replaceWith(response[0]);
            $('#items').replaceWith(response[1]);
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
                    $('#editItem').find('#itemForm').replaceWith(response[0]);
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
                    $('#addItem').find('#itemForm').replaceWith(response[0]);
                },
                null
            );
        })
        //File Upload
        //Reference: http://www.html5rocks.com/en/tutorials/file/dndfiles/
        .on('change', '.fileInput', function(e) {
            uploadFile = e.target.files[0];
            if ($.inArray(uploadFile.name.split('.').pop().toLowerCase(), ALLOWED_EXTENSIONS) == -1) {
                var fileInput = $(this);
                fileInput.val("");
                alert('File extension is not allowed!');
                return;
            }

            var reader = new FileReader();
            var itemForm = $(this.form);

            //Show the image in the modal when it loads
            reader.onload = function(e) {
                var container = itemForm.find('.imageContainer');
                var prevImage = itemForm.find('.previewImage');
                if (prevImage.length > 0) {
                    prevImage.remove();
                }
                else {
                    container.removeClass('noImage');
                    container.children('#itemImageUpload').remove();
                }
                container.prepend('<img class="previewImage" src="' + e.target.result + '" />');
            };

            reader.readAsDataURL(uploadFile);

            //Show edit image options
            itemForm.find('.editImgOptionsWrapper').show();

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
                    $('#categories').replaceWith(response[0]);
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
                    $('#categories').replaceWith(response[0]);
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
                    $('#categories').replaceWith(response[0]);
                    // Response only contains Items response if it's necessary to re-render
                    if (response.length > 1) {
                        $('#items').replaceWith(response[1]);
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

            process(
                formData,
                function(response) {
                    $('#items').replaceWith(response[0]);
                },
                null
            );
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
                    $('#viewItem').find('.viewItemContainer').replaceWith(response[0]);
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
            var file_data = uploadFile ? uploadFile : null;
            var has_file = file_data ? true : false;
            formData = new FormData();

            if (editItemForm.find('.previewImage').length > 0) {
                has_file = true;
            }

            requestData =
            {
                "action": "EditItem",
                "item_id": itemID,
                "item_name": itemName,
                "category_id": categoryID,
                "description": description,
                "has_file": has_file
            };

            if (file_data) {
                requestData["file_size"] = file_data.size;
                requestData["file_type"] = file_data.type;
            }

            JSONPost = JSON.stringify(requestData);

            formData.append('request_data', JSONPost);
            formData.append('file_data', file_data);

            process(
                formData,
                function(response) {
                    $('#items').replaceWith(response[0]);
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
                    $('#items').replaceWith(response[0]);
                },
                null
            );
        })


        //Delete Item Image
        .on('click', '.deleteImage', function(e) {
            uploadFile = null;

            var container = $('.imageContainer');
            var image = $('.previewImage');
            var imageOptions = $('.editImgOptionsWrapper');

            image.remove();
            imageOptions.hide();
            container.addClass('noImage');
            //container.children('input').each().remove();
            container.append('<input type="file" id="itemImageUpload" class="fileInput" />');
        });




    $('#addCategory').on('hidden.bs.modal', function() {
        $('#newCategoryForm').find('#name').val('');
    });

    $('#addItem').on('hidden.bs.modal', function() {
        $(this).find('form').prop('id', 'itemForm');
        uploadFile = null;
    });

    $('#editItem').on('hidden.bs.modal', function() {
        $(this).find('form').prop('id', 'itemForm');
        uploadFile = null;
    });
});