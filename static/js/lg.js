$(function () {
    $('#check-img').click(function () {
        $(this).attr('src', $(this).attr('src') + '?')
    });
    $('#lsubmit').click(function () {
        //$(this).children(':eq(0)').addClass('hide');
        //$(this).addClass('not-allow').children(':eq(1)').removeClass('hide');
        // 发送Ajax请求
        //完成之后
        $('#model_login  .error').remove();

        var post_dict = {};
        $('#model_login input').each(function () {
            post_dict[$(this).attr("name")] = $(this).val();
        });
        console.log(post_dict);
        $.ajax({
            url: '/',
            type: 'POST',
            data: post_dict,
            dataType: 'json',
            success: function (arg) {
                if (arg.status) {
                    alert('1');
                    window.location.href = '/hostinfo/';
                } else {
                    $.each(arg.message, function (k, v) {

                        //<span class="error">s</span>
                        var tag = document.createElement('span');
                        tag.style.color = "red";
                        tag.className = 'error';
                        tag.innerText = v[0]['message'];
                        $('#model_login input[name="' + k + '"]').after(tag);
                    })
                }
            }
        });
        //$(this).removeClass('not-allow').children(':eq(1)').addClass('hide');
        //$(this).children(':eq(0)').removeClass('hide');
    });
    $("#fetch_code").click(function () {
        // 整体错误清空
        $('#yerr').empty();

        // 点击的按钮
        if ($(this).hasClass('sending')) {
            // 遇到return下面不再继续执行
            return;
        }
        var ths = $(this);
        var time = 60;
        var email = $('#model_login input[name="user"]').val();
        alert(email.trim());
        if (email.trim() == "") {
            $('#yerr').text("请输入账户")
        }
        $.ajax({
            url: "/lgecode/",
            type: 'POST',
            data: {email: email},
            dataType: 'json',
            success: function (arg) {
                console.log(arg);
                // {'status': False, "summary": '整体错误错误', 'error': {}}
                if (!arg.status) {
                    $('#yerr').text(arg.summary);
                } else {
                    // 后台已经发送成功
                    ths.addClass('sending');
                    var interval = setInterval(function () {
                        ths.text("已发送(" + time + ")");
                        time -= 1;
                        if (time <= 0) {
                            clearInterval(interval);
                            ths.removeClass('sending');
                            ths.text("获取验证码");
                        }
                    }, 1000);
                }
            }
        });
    });
});