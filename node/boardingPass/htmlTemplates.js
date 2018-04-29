var list = {};
list.wrapper = '<div class="list-group">\n' +
                '</div>'
list.row = function(content,link,data) {
        console.log(link);
        let  html =   '  <a href="'+link.toString()+'" class="list-group-item" data="'+data+'">\n' +
                        '    <div class="d-flex w-100 justify-content-between">\n' +content +
                        '    </div>\n' +
                        '  </a>\n';
        return html
}

let profile = function(username,firstName,lastName,country,img){
     let html  = '<div class="card" style="width: 18rem;">\n' +
         '  <ul class="list-group list-group-flush">\n' +
         '    <li class="list-group-item">Username:'+username+'</li>\n' +
         '    <li class="list-group-item">First Name:'+firstName+'</l+i>\n' +
         '    <li class="list-group-item">Last Name:'+lastName+'</li>\n' +
         '    <li class="list-group-item">Country:'+country+'</li>\n' +
         '  </ul>\n' +
         '</div>';
     return  '<div><img src="'+img+'" style="width:200px;height:200px"></div>'+html;

}

let lesson_card = function(index,id,name,description,max_students,length_in_minutes,cost,currency){
    let html  =   '<div class="card card-block">\n' +
                '    <h4 class="card-header">'+name+'</h4>\n' +
                '    <p class="card-text">'+description+'</p>\n' +
                '    <a href="#" id="lesson'+index+'" class="lesson btn btn-primary">Button Primary</a>\n' +
                 '</div>'

     return  html;


}


module.exports.list = list;
module.exports.profile = profile
module.exports.lesson_card = lesson_card;