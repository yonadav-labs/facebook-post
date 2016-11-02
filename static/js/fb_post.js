var old_keyword;

$('.login-navigation li').click(function() {
    $('.login-error-message').hide();
});

$('.query_form').submit(function(event) {
    event.preventDefault();
    var keyword = $('#q').val();
    if (keyword != old_keyword) {
        old_keyword = keyword;
        console.log(keyword);
        $.ajax({
        	method: 'POST',
            url: '/retrieve_post',
            data: {
                'q': keyword,
                "csrfmiddlewaretoken": csrf_token,
            },
            success: function(ret) {
                if (ret['status'] == 'complete') {
                    window.location.href = '/post/' + keyword;
                } else {
                    $('.query-preloader').removeClass('hidden');
                    $('#btn-query').prop('disabled', true);

                    setTimeout(function() {
                        window.location.href = '/post/' + keyword + '/_';
                    }, 5000);
                }
            }
        });

    }
})
