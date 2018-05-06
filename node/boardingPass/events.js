var network = require("../utils/network");
var http = new network.HTTP();
var _ = require('underscore');
var templates = require('./htmlTemplates');
var pages = require('./pages')
var date = require('../utils/date')
var bpScheduler = require('./scheduler');

let login = function(response){

    console.log(response.status);

    var detail;
    console.log(response);
    if(response.status===undefined){

        detail = response.detail;
        if(detail.toLowerCase()==="login successful"){
             $('#login_message').text('');
            pages.render("sensei_list");
            var hrefLog =  $('#login')
            $("#wrapper").toggleClass("toggled");
            hrefLog.text('Logout');
            hrefLog.click(function(){
                hrefLog.text('Log In');
                 $("#wrapper").toggleClass("toggled");
                http.POST('/api/v1/accounts/logout/',{},function(data){
                    console.log(data);

                })
                return false;
            })
        }

        console.log(detail);

    }else{
        detail  = response.responseJSON.detail;
        $('#login_message').text(detail);

    }



}

let click_sensei_card = function(){
    var sensei_id = $(this).attr('data');
    console.log(sensei_id);
    // Builds the profile
    pages.render("sensei_profile",function(){
            http.GET('/rest/sensei/data/'+sensei_id+'/',function(data){
                let profile_data = data[0];
                $('#profile_pic').attr('src',profile_data.image_url);

            },'json')
            http.GET('rest/sensei/lessons/'+sensei_id+'/',function(data){

                data.forEach(function(row,index){
                        $('#lessons').append(templates.lesson_card(index,sensei_id,row.name,row.description));

                        $('#lesson'+index).click(function(){
                            pages.render('scheduler',bpScheduler.scheduler_events);

                        })
                })

            })
    });
    return false;
}

let create_class = function(response){
    return false;
}


let sign_up = function(response){
    var detail = response;
    console.log(response);
    console.log('sign up function');
    if(detail.id!==undefined){
         console.log('Sign Up Successful');
         $('#pills-home').empty();
         $('#pills-home').hide();
         $('#pills-home').html("<h4> You successfully signed up.Please Login.</h4>");
         $("#pills-home").fadeIn(2000);

    }else{
        detail = JSON.parse(response.responseText);
        console.log(detail);
        var keys = _.keys(detail);
        console.log(keys)
        keys.forEach(function(key){
           var message = detail[key][0]+'<br>';

           $('#signup_message').append(message)
        });
        return false;
    }

}

let post_request = function(formId,mappings,url,response_handler){

    var formData = $(formId).serializeArray();
    var keys = _.keys(mappings);
    let payload = {};

    keys.forEach(function(key){
        var obj = _.findWhere(formData, {name:mappings[key].toString()})
        payload[key] = obj.value;
    })

    http.POST(url,payload,response_handler)
}
let build_sensei_list =  function(url){

    http.GET(url,function(data){
        let list = templates.list;
        data.forEach(function(row){
             console.log(row);
             let country = row.country;
             let username =  row.user.username;
             let firstName = row.user.first_name;
             let lastName  = row.user.last_name;
             let sensei = row.user.id;
             let image = row.image_url;
             let profile_card = templates.profile(username,firstName,lastName,country,image);
             let content = templates.list.row(profile_card,'/sensei/profile/'+sensei,sensei);
             $('#sensei_list').append(content);

        });
        $('.list-group-item').click(click_sensei_card)

    },'json');

}

let create_page = function(page,assignEvents){

     // appends html to the content element
     $('#content').empty();

     http.GET(page.templateUrl,function(html){
        $('#content').hide();
        $('#content').append(html);
        $('#content').fadeIn(1250);
        let forms = page.content;
        if(assignEvents){
            assignEvents();
        }

        forms.forEach(function (form) {

             if(form.isForm) {

                 let id = '#' + form.id;

                 $(id).submit(function () {

                     form.post(id, form.mappings, form.ajaxUrl,form.response_handler);
                     return false;
                 })
                 $(id).validate({rules: form.rules, messages: form.messages});
             }else{
                 if(form.get_request) {
                     form.get_request(form.ajaxUrl);
                 }
             }
        })


    },'html')
}


module.exports.build_sensei_list = build_sensei_list;
module.exports.post_request = post_request;
module.exports.login = login;
module.exports.sign_up = sign_up;
module.exports.create_page = create_page;
module.exports.click_sensei_card = click_sensei_card;
module.exports.create_class = create_class;