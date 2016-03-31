$(function() {
    $('.testLink').click(function() {

        var data = {
            "action": "testAjax",
            "id": this.id,
            "drew": "Drew is King of AJAX"
        };

        $.ajax({
            url: '/catalog',
            data: JSON.stringify(data),
            type: 'POST',
            contentType: 'application/json;charset=UTF-8',
            success: function(response) {
                console.log(response);
                $('#items').append(response);
            },
            error: function(error) {
                alert(error.message);
            }
        });
    });
});