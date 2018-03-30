$(function () {
    $('#m1-1').find('div').removeClass('hidden');
    $('#m1-1').find('button').addClass('active');
    $('#m1-1').find('button span').removeClass('glyphicon-chevron-left');
    $('#m1-1').find('button span').addClass('glyphicon-chevron-down');
    $('#m1-1').find('div').children('a:eq(0)').addClass('active')

})