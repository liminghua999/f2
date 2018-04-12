$(function () {
    active_zuo();
    addapi_submit();
});
function active_zuo() {
    $('#m1-3').find('div').removeClass('hidden');
    $('#m1-3').find('button').addClass('active');
    $('#m1-3').find('button span').removeClass('glyphicon-chevron-left');
    $('#m1-3').find('button span').addClass('glyphicon-chevron-down');
    $('#m1-3').find('div').children('a:eq(2)').addClass('active');
}
function addapi_submit() {
    var num=1;
    $('#addmoreapi').click(function () {
        num+=1;
        var newapi=document.createElement('div');
        newapi.innerHTML="<div class=\"col-sm-6 col-sm-offset-4\">\n" +
            "<input type=\"text\" id=\"yapi"+num+"\" placeholder=\"本次版本新增的api; 若无，不填写\" class=\"form-control\">\n" +
            "</div><span class=\"glyphicon glyphicon-minus btn btn-default pull-left \"></span>";
        newapi.classList.add('form-group');newapi.classList.add('row');
        $('#yanfa .modal-body').append(newapi);
    });
    $('#yanfa .modal-body').on('click','.glyphicon-minus',function () {
        num-=1;
        $(this).parent().remove();
    });
    $('#yanfa_submit').click(function () {
        alert(num);
        d={'yoperateman':null,'yinform_nextman':null,'yapi1':null,'apinum':null};
        d.yoperateman=$('#yoperateman').val();
        d.yinform_nextman=$('#yinform_nextman').val();
        for (var i=1;i<num+1;i++){y='yapi'+i;d[y]=$('#'+y).val();}
        d.apinum=num;
        $.ajax("{% url 'unfinished' %}{{ data_dict.newversion.id }}/yanfa",
        {'type':'POST','dataType':'JSON',success:function (res) {
            if (res){}
            else{}
        }})
    });
}