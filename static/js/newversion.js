$(function () {
    $('#m1-3').find('div').removeClass('hidden');
    $('#m1-3').find('button').addClass('active');
    $('#m1-3').find('button span').removeClass('glyphicon-chevron-left');
    $('#m1-3').find('button span').addClass('glyphicon-chevron-down');
    $('#m1-3').find('div').children('a:eq(0)').addClass('active');
})