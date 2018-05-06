let page = require("./boardingPass/pages");
global._=  require('underscore');



$(function() {




    $('#login').click(function(e){

        page.render('landing');
        return false;
    });
    $('#create_class_button').click(function(e){

        page.render('create_class');
        return false;
    })
    $('#find_sensei').click(function(e){

        page.render('sensei_list');
        return false;
    })
     $('#edit_profile').click(function(e){

        page.render('edit_profile');
        return false;
    })
    //
/*
http.GET('/scheduler/',function(html){

$('#content').append(html)
console.log(html)
scheduler.init('scheduler_here', new Date(),"month");
var events = [
{id:1, text:"Meeting",   start_date:"04/11/2018 14:00",end_date:"04/11/2018 17:00"},
{id:2, text:"Conference",start_date:"04/15/2018 12:00",end_date:"04/18/2018 19:00"},
{id:3, text:"Interview", start_date:"04/24/2018 09:00",end_date:"04/24/2018 10:00"}
];

scheduler.parse(events, "json");//takes the name and format of the data source
    },"html")

*/



});