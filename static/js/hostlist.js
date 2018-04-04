$(function () {
    $('[data-toggle="popover"]').popover();
    $('#m1-1').find('div').removeClass('hidden');
    $('#m1-1').find('button').addClass('active');
    $('#m1-1').find('button span').removeClass('glyphicon-chevron-left');
    $('#m1-1').find('button span').addClass('glyphicon-chevron-down');
    $('#m1-1').find('div').children('a:eq(0)').addClass('active');
    laydate.render({ elem: '#ctime',type: 'datetime' });
    $('#addhost_submit').click(function () {
        var d={'ip':null,'type':null,'labels':"",'ctime':null,'gip':null};
        d.ip = $('#IP').val();
        d.type=$('#addhost_type').get(0).selectedIndex;
        $('#addhost_label option:selected').each(function () {
            d.labels += $(this).val()+' ';
        });
        d.ctime=$('#ctime').val();
        d.gip=$('#gIP').val();
        $('#addhost').modal('hide');
        $.ajax('/hostinfo/addhost/', {
            type: 'POST', dataType: 'JSON', data: d,
            success: function (res) {
                if (res['err'] != '0') {
                    alert(res.err);
                }
                else {
                    console.log(res['data']);
                    trr = document.createElement('tr');
                    tip = document.createElement('td');
                    tip.setAttribute('t', 'ip');
                    tip.innerHTML = res['data']['ip'];
                    tname = document.createElement('td');
                    tname.setAttribute('t', 'hostname');
                    tname.innerHTML = res['data']['hostname'];
                    ttype = document.createElement('td');
                    ttype.setAttribute('t', 'type');
                    ttype.innerHTML = res['data']['type'];
                    town_to = document.createElement('td');
                    town_to.setAttribute('t', 'own_to');
                    town_to.innerHTML = res['data']['own_to'];
                    tlabels = document.createElement('td');
                    tlabels.setAttribute('t', 'label');
                    tlabels.innerHTML = res['data']['labels'];
                    tmem = document.createElement('td');
                    tmem.setAttribute('t', 'mem');
                    tmem.innerHTML = res['data']['mem'];
                    tdisk = document.createElement('td');
                    tdisk.setAttribute('t', 'disk');
                    tdisk.innerHTML = res['data']['disk'];
                    console.log(tdisk.innerHTML);
                    tremarks = document.createElement('td');
                    tremarks.setAttribute('t', 'remarks');
                    tremarks.innerHTML = res['data']['remarks'];
                    tctime = document.createElement('td');
                    tctime.setAttribute('t', 'cimte');
                    tctime.innerHTML = res['data']['ctime'];
                    tdtime = document.createElement('td');
                    tdtime.setAttribute('t', 'dimte');
                    tdtime.innerHTML = res['data']['dtime'];
                    tc = document.createElement('td');
                    tc.innerHTML = "<span class=\"label label-success\">编辑</span>&nbsp;<span class=\"label label-warning\">删除</span><br><span class=\"label label-danger\">终端</span>";
                    $(trr).append(tip);
                    $(trr).append(tname);
                    $(trr).append(ttype);
                    $(trr).append(town_to);
                    $(trr).append(tlabels);
                    $(trr).append(tmem);
                    $(trr).append(tdisk);
                    $(trr).append(tremarks);
                    $(trr).append(tctime);
                    $(trr).append(tdtime);
                    $(trr).append(tc);
                    $('table tbody').append(trr);
                }
            }
        });
    });
    $('#addservice_submit').click(function () {
        var d={'cservice_name':null,'ctomcat_name':null};
        d.cservice_name=$('#cservice_name').val();
        d.ctomcat_name=$('#ctomcat_name').val();
        $.ajax('/hostinfo/addservice/',{
            type:'POST',dataType:'JSON',data:d,success:
                function (res) {
                if (res == 'true'){$('#addservice').modal('hide');window.location.reload();}
                else {alert(res);$('#addservice').modal('hide');}
                }
            })
    });
    $('table tbody').on('click','.hostlist_edit',function () {

    });
    $('table tbody').on('click','.hostlist_del',function () {
        var del_ip=$(this).parent().parent().children().first().text();
        $('#hostlist_del .modal-body p span').text(del_ip);
        $(this).parent().parent().attr('id','pre_del');
        var d={'del_ip':del_ip};
        $("#hostlist_del_submit").click(function () {
            $.ajax('/hostinfo/delhost/',{type:'POST',dataType:'JSON',data:d,success:function (res) {
                    if (res != '0'){alert(res)}
                    else{$('#pre_del').remove()}
                }});
            $('#hostlist_del').modal('hide');
        })
    });
})