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
                if (res == true){ $('#addservice').modal('hide');window.location.href='/hostinfo/hostlist/';}
                else {alert(res);$('#addservice').modal('hide');}
                }
            })
    });
    $('table tbody').on('click','.hostlist_edit',function () {
        var get_ip=$(this).parent().parent().children().first().text();
        $('#uip').text(get_ip);
        var oldtype=$(this).parent().parent().children(':eq(2)').text();
        $('#utype option').each(function () {
                if ($(this).text() == oldtype){$(this).attr('selected',true)}
                else{$(this).attr('selected',false)}
            }
        );
        var oldlabels = $(this).parent().parent().children(':eq(4)').text();
        $('#uservices option').each(function () {
                var pp= new RegExp($(this).text());
                var bh=pp.test(oldlabels);
                if (bh){$(this).attr('selected',true)}
                else{$(this).attr('selected',false)}
            }
        );
        var oldgip = $(this).parent().parent().children(':eq(3)').text();
        $('#ugip').attr('placeholder',oldgip);
        var oldremarks=$(this).parent().parent().children(':eq(7)').text();
        $('#uremarks').val(oldremarks);
        $('#updateservice_submit').click(function () {
            var d={'ip':null,'type':null,'labels':"",'remarks':"",'gip':null};
            d.ip=get_ip;
            d.type=$('#utype').get(0).selectedIndex;
            $('#uservices option:selected').each(function () {
                d.labels += $(this).val()+' ';
            });
            d.gip=$('#ugip').val();
            d.remarks=$('#uremarks').val();
            $.ajax('/hostinfo/updatehost/',{"data":d,"type":'POST',"dataTtype":"JSON",success:function (res) {
                console.log(typeof(inres));
                if ( res != '0' ) {alert(res);console.log('failed');}
                else {$('#hostlist_edit').modal('hide');alert('修改成功');top.location.reload(true);}

            }});
        })

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
    // $('#filter form div button').click(function () {
    //    var label=$('#filter_label').find('option:selected').text();
    //    alert(label);
    //    var type=$('#filter_type').find('option:selected').val();
    //    alert(type);
    //    d={'filter_label':null,'filter_type':null};
    //    d.filter_label=label;
    //    d.filter_type=type;
    //    $.ajax('/hostinfo/filter/',{'data':d,'type':"POST",'dataType':'JSON',success:function (res) {
    //         if (res.err != '0'){
    //             $('#filter_label option').each(function () {
    //                 if ($(this).text() == res.data.filter_label){$(this).attr('selected',true)}
    //                 else{$(this).attr('selected',false)}
    //             });
    //             $('#filter_type option').each(function () {
    //                 if ($(this).text() == res.data.filter_type){$(this).attr('selected',true)}
    //                 else{$(this).attr('selected',false)}
    //             });
    //         }
    //         else{alert(res.err)}
    //     }})
    // });
    $('#autoaddhost').click(function () {
        $.ajax('/hostinfo/autoaddhost/',{type:'POST',dataType:'JSON',success:function (res) {
                if (res == '1'){alert("done")}
                else{alert('err')}
            }})
    });
})