/*
*  This pages main purpose is to handle creating and binding controls to grids
*  an creates the user input controls for the pages as well as custom controls developed by Micah Bell.
*
* */

function createElement(type){
    /*
            creates a dom element and converts it to a jquery object
     */
    var element = document.createElement(type);        // Create a <button> element
    return new Element($(element));
}
function Element(elem){
    this.jqObj = elem;  // element in the form of a jquery object
    this.validate = false;
    var jqObj = elem;
    this.regEx = null;
    this.filter = null;
    this.setText = function(str){
        this.jqObj.text(str);
    };
    this.tagName = function(){
        return jqObj.prop('tagName');
    }
    this.innerHTML = function (){
        return jqObj.html();
    }
    this.append = function(obj){
        this.jqObj.append(obj.jqObj);
    }
    this.prepend  = function(obj){
        this.jqObj.prepend(obj.jqObj);
    }
    this.setCSS = function(css){
        this.jqObj.css(css);
    },
    this.getCSS = function(name){
        return this.jqObj.css(name);
    }
    this.setAttributes = function(attr){
        this.jqObj.attr(attr);
    }
    this.getAttribute = function(name){
        return jqObj.attr(name);
    }
    this.setAttr = function(name,value){
        this.jqObj.attr(name,value);
    }
    this.setXY  = function(x,y){
        // sets the X and Y coordinates of a element.
        this.jqObj.css("top",y);
        this.jqObj.css("left",x);
    }
    this.getXY = function(){
        return {"x":this.jqObj.css("left"),"y":this.jqObj.css("top")}
    }
    this.setX = function(x){
        this.jqObj.css("top",x)
    }
    this.setY = function(y){
        this.jqObj.css("top",y);

    }
    this.event = function(type,callback){
        /*
            The event associated with the element.
        */
        // type is the type of event
        this.jqObj[type](  callback ) ;
    }
    this.reset = function(){

    };
    this.val = function(){
        if(this.filter===null)
            return this.jqObj.val();
        else
            return this.filter(this.jqObj.val()); // apply a filter to the ouput result for the query string for example.
    }
    this.regExValidate = function(regEx){

        return this.regEx.test(this.jqObj.val());
    }
    this.hide = function(){
        this.jqObj.css("display","none");
    }
    this.show = function(){
        this.jqObj.css("display","show");
    }
    this.custom = null;  // add a custom function to a control
    this.effect =   {
                        flashing:function(){   jqObj.fadeIn(500).fadeOut(500).fadeIn(500).fadeOut(500).fadeIn(500);}
                    }
}

function DataTableCustom(name, con,appendId) {
    /* Custom DataTables class */
    // Creates the table element.
    this.table = createElement("table"); // creates a table element
    this.table.jqObj.attr("id", name.toString()); // name the table by assigning an id
    $("#" + appendId).append(this.table.jqObj);  // I believe you have to append a table to an element and create it in the dom before you can assign columns to it.
    this.table.setAttr("class", "table table-bordered table-condensed table-striped table-hover");
    this.table = new Table(this.table); // Creates a ne
    var dt = this.table.jqObj.DataTable(con); // extends the table prototype by assigning the datatable class to it.
    dt.buttons().container().appendTo('#' + name.toString() + '_wrapper .col-sm-6:eq(0)'); // used to assing the CSV buttons to the table;

   /*
    if (clickEvent !== null) {
        dt.on('click', 'tr', function () {
            clickEvent(dt.row(this).id());
        });

    }
    */
    this.bindData = function (data) {
        /* This function is used to bind data to the datatable */
        this.table.bindJSON(data, dt)

    }
}


function collapsibleContainer(name,titleText,textText,attachTo,scroll){
    var style = 'style=';
    this.name = name;
    this.panels = [];
    style =   scroll==true ? style+'max-height:300px;overflow-y:auto;' : style;
    console.log(style);
    var  test = '<div id='+this.name+' class=".container-fluid" >\n' +
              '  <h4>'+titleText+'</h4>\n' +
              '  <p>'+textText+'</p>\n' +
              '  <div id="panel-group" class="panel-group" '+style+'>\n' +
              '  </div>\n' +
              '</div>';
    attachTo.html(test);


    this.addPanel = function(name,titleText, contents,data) {
        String.prototype.fixSpecialChars =   function(){ return this.replace(/[!"#$%&'()*+,.\/:;<=>?@[\\\]^`{|}~]/g, "\\\\$&") };
        name = name.replace(/\s/g, '_').replace('/','Slash').fixSpecialChars();
        this.panels.push(data);
        var panel =  '    <div id="'+name+'-panel" data-cat="'+data+'" class="panel panel-primary">\n' +
                    '      <div class="panel-heading">\n' +
                    '        <h4 class="panel-title"><input id="'+name+'-check-all" class="'+this.name+'-select-all" type="checkbox"/>&nbsp;&nbsp;\n' +
                    '          <a data-toggle="collapse" href="#'+name+'">'+titleText+'</a>\n' +
                    '</h4> '+
                    '      </div>\n' +
                    '      <div id="'+name+'" class="panel-collapse collapse">\n'+contents.jqObj.html()+
                    '      </div>\n' +
                    '    </div>\n';

        $('#'+this.name+' .panel-group').append(panel);
        $('#'+name+'-panel .'+this.name+'-select-all').unbind().on('click',function(){
            $('#'+name+' input[type=checkbox]').prop('checked',this.checked);


        });



    }
    this.addSearch = function(){
        var search  = createElement('input');
        search.jqObj.css({margin:'2px','left-margin':'5px'});
        search.jqObj.attr({type:'text',id:'search'});
        $('#'+this.name+' p').after('<p><span id="glyph" class="glyphicon glyphicon-search"></span></p>')
        $('#'+this.name+' p #glyph').after(search.jqObj);

        var scope_this = this;
        $('#search').unbind().keyup(function(){
            var searchVal = $(this).val();

            var showPanels = _.filter(scope_this.panels,function(obj){
                return obj.toLowerCase().search(searchVal.toLowerCase()) + 1; // you need to escape the slashes
            });
            var hidePanels = _.difference(scope_this.panels,showPanels);

            showPanels.forEach(function(panel){  $('[data-cat="'+panel+'"]').show();  })
            hidePanels.forEach(function(panel){ $('[data-cat="'+panel+'"]').hide();  });
        })

    }


}


function List(name,store){
    this.list = createElement("ul");

    this.jqObj = this.list.jqObj;
    this.jqObj.attr("id",name);
    this.jqObj.css({
        filter:'none !important'
    });
    this.items = [];
    this.list.jqObj.attr("class","list-group nonselected");
    this.list.jqObj.css({"list-style-type":"none","margin":"0","padding":"0","width":"50x"});
    var storeElements = store || false;
    var elements = [];


    this.add = function(text,flash){
        var li = createElement("li");

        li.jqObj.attr("class","list-group-item mt-0");
        li.jqObj.css("font-size","9pt")
        li.setText(text);
        li.jqObj.css("display","hide");
        this.list.append(li);
        if(flash)
            li.effect.flashing()
    }
    this.count = function(){
        return this.list.jqObj.children().length;
    }
    this.addHtml = function(html,flash){
        var li = createElement("li");

        li.jqObj.attr("class","list-group-item mt-0");
        li.jqObj.css("font-size","9pt")
        li.jqObj.html(html);
        li.jqObj.css("display","hide");
        this.list.append(li);
        if(flash)
            li.effect.flashing()

    }
    this.title = function(text){
        var li = createElement("li");
        li.jqObj.attr("class","list-group-item active");
        li.jqObj.attr('id','title');
        li.setText(text);
        this.list.append(li);
    }
    this.fromArray = function(arr){
        var scope_this = this;
        arr.forEach(function(elem){ scope_this.add(elem);    });
    }
    this.addWithId = function(name,text,icon){
        var li = createElement("li");
        li.setAttr("id",name);
        li.jqObj.attr("class","list-group-item");
        li.setText(text);
        li.jqObj.css("display","hide");
        if(icon) {
            var glyph = createElement("span");
            glyph.jqObj.attr("class", "glyphicon " + icon);
            li.prepend(glyph);
            glyph.effect.flashing();

        }
        this.list.append(li);
    }
    this.remove = function(id){
        this.list.jqObj.find('#'+id).remove();

    }
    this.destroy = function(){
        this.list.jqObj.empty();
    }
    this.sort =function() {
        var mylist = this.list.jqObj;
        var listitems = mylist.children('li[id!=title]').get();
        listitems.sort(function(a, b) {
            return $(a).text().toUpperCase().localeCompare($(b).text().toUpperCase());
        })
        $.each(listitems, function(idx, itm) { mylist.append(itm); });
    }
}

function bindElements(bindObjects,callback) {
    // Binds data to a table or other object.
    var obj = bindObjects.pop();
    var url =  obj.url;
    var obj = obj.obj;;
    $.ajax({
        url: url,
        cache: false,
        dataType: "json",
        success: function(data) {
            callback(data,obj);
            if(bindObjects.length>0) {
                bindElements(bindObjects, callback);
            }
        },
        error: function (request, status, error) { alert(status + ", " + error); }
    });
}

function Component(comp){
    this.comp = comp;
    this.jqObj = comp;
    this.elements = []; //element array
    this.addElement = function(elem,name){
        this.elements.push({name:name,elem:elem});
        this.comp.append(elem.jqObj);
    }
    this.getElement = function(name){
        /*
            Gets a particular element from the element array by name
         */
        return $.where(elements,{name:name});
    }
}
Component.prototype = new Element();

Modal.prototype = new Element();
//TODO: Redesign Modal
function Modal(name){

    this.modal = createElement("div");
    this.modal.setAttr("id",name);
    this.modal.setAttr("class","modal fade");
    this.modal.setAttr("role","document");
    this.modalDialog = createElement("div");
    this.modalDialog.jqObj.attr({class:"modal-dialog  modal-lg"});
    this.modal.jqObj.append(this.modalDialog.jqObj);
    this.elem = this.modal;
    this.jqObj = this.modal.jqObj;
    this.header = createElement("div");
    this.header.jqObj.attr("class","modal-header");
    this.button = createElement("button");
    this.button.jqObj.attr({type:"button",class:"close","data-dismiss":"modal"});
    this.button.jqObj.html("Close");
    this.header.jqObj.append(this.button.jqObj);
    this.H4   = createElement("h4");
    this.header.jqObj.append(this.H4.jqObj);
    this.header.jqObj.append(this.button);
    this.modalDialog.jqObj.append(this.header.jqObj);
    this.body = createElement("div");
    this.modalDialog.jqObj.attr("class","modal-content");
    this.modalDialog.jqObj.append(this.body.jqObj);
    this.body.setAttr("class","modal-body");
    this.modalDialog.jqObj.append(this.body.jqObj);
    this.footer = createElement("div");
    this.footer.jqObj.attr("class","modal-footer");
    this.buttonClose = createElement("button");
    this.buttonClose.jqObj.attr({type:"button",class:"close","data-dismiss":"modal"});
    this.buttonClose.setText('Close');
    this.footer.jqObj.append(this.buttonClose.jqObj);
    this.modalDialog.jqObj.append(this.footer.jqObj);
    $("body").append(this.modal.jqObj);
    this.addHeader = function(content){
        this.H4.jqObj.append(content);

    }
    this.addContent = function(content){
        this.body.jqObj.append(content);
    }
    this.removeContent = function(){
        this.body.jqObj.html("");
        this.header.jqObj.html("");
    }
    this.close  = function(){
        this.modal.jqObj.modal("hide");
    }
    this.open = function(){
        this.modal.jqObj.modal("show");
        //this.modal.jqObj.empty();
        //this.modal.jqObj.destroy();
    }

}

MultiSelect.prototype = new Element();

function MultiSelect(name,text){
     /* The multi select button created in bootstrap */
     this.jqObj = createElement("div").jqObj;
     this.select = createElement("select");
     this.select.setAttr("multiple","multiple");
     this.select.setAttr("id",name);
     var name = name;
     this.jqObj.append(this.select.jqObj);
     this.val = function(){
         var checked = [];
         $("#"+name + " option:selected").each(function () {

             checked.push($(this).val());

         });
         return checked;

     }
     this.bindJSON = function(JSON){
         var scope_this = this;

         JSON.forEach(function(obj){

             var option = createElement("option");
             option.setText(obj.name);
             option.setAttr("value",obj.id  );
             scope_this.select.jqObj.append(option.jqObj);

         });
         this.select.jqObj.multiselect({
             includeSelectAllOption: true,
             allSelectedText: 'All Selected',
             numberDisplayed: 2
         });
         this.select.jqObj.multiselect("rebuild");


     }
}

ClickStateButton.prototype = new Element();
function ClickStateButton(name,metadata,states,defaultState,imgUrl) {
    /* Click state control button. As you click on the object the state of the button changes.
       If images are added to the element then the image will also change.

     */
    this.elem = createElement("img");
    var metadata = metadata; // Meta data used depending on the developers needs.
    var imgUrl = imgUrl;
    this.jqObj = this.elem.jqObj;
    this.jqObj.attr("id", name);
    this.jqObj.attr("src", "../../assets/images/"+defaultState+".png");  // sets where the images are accessed.
    this.jqObj.attr("value", defaultState);
    this.jqObj.parent().parent().attr("class","row text-center");
    this.jqObj.parent().attr("class","");
    var state = defaultState;
    var jqObj = this.jqObj;
    var count = 1;  //sets the default state.
    var states = states;
    this.getState = function(){
        return state;
    }
    this.reset = function(){
        count = 0;
        console.log(count);
        jqObj.attr("src",imgUrl+states[count]+".png");
        jqObj.attr("value",states[count]);
        ++count;
    }
    this.val = function(){
        return  state;
    }
    this.getStateData = function(){
        return metadata[state];
    }
    this.switch_event = function(range,callback){
            var range = range;
            return function(){

                state = states[count];
                jqObj.attr("src",imgUrl+states[count]+".png");
                jqObj.attr("value",states[count]);
                ++count;
                if(count>=range)
                    count = 0;
                callback(metadata[state]);
            }
    }
}

function buildControl(obj){
    // Builds a control based off a JSON object
    var name = obj.name;  // Name of the element
    var css = obj.css;  // CSS of the element
    var attr = obj.attr; // element attr
    var type = obj.type; // element type

    if(typeof(obj.name)==="string") {
        obj.attr.id = obj.name;

    }
    if(obj.type==="date"){
        var elem = createElement("input");
    }else{
        var elem = createElement(type);
    }


    if(typeof(obj.attr)!==undefined) // if there are no attributes for the objects it will be set here.
        elem.setAttributes(obj.attr);
    if(typeof(obj.event)==="object") // if the element has an event attached to it will be binded to the object.
        elem.event(obj.event.type,obj.event.function);
    if(typeof(obj.text)!==undefined)
        elem.setText(obj.text);
    if(typeof(obj.name)!==undefined)
        elem.setAttr('name',obj.name);
    if(obj.css) {
        elem.jqObj.css(obj.css);
    }
    return elem;
}


exports.buildComponentFromJson =  function(json){
    var comp = new Component($("#queryControl"));


    json.forEach(function (obj) {


    });


}

Grid.prototype = new Element();
function Grid(container){
    /* Dependant on bootstrap */
    this.container = container;
    this.jqObj = container;
    this.addColumns = function(arr,row){
       /*
            Adds columns to a specified row.
       */
        var colClassArr = ['col-lg','col-md','col-sm'];  //bootstrap names
        var numCol = arr.length>3 ? 3 : 4;
        var colClass = colClassArr.map(function(str){  return str+"-"+(numCol).toString();  }).join(" ")
        // adds a column to the row of a grid.
        arr.forEach(function(obj){
            // Div Column Element
            var divCol = createElement("div");
            divCol.setAttr("class","form-group form-group-sm "+colClass);
            // Builds the column along with the grid html node
            if(obj.type==="object" || obj.type==="multiSelect" || obj.type==="vinButton") {
                var gridElement = obj.obj;
                if(typeof(obj.event)==="object"){
                     obj.obj.elem.event(obj.event.type,obj.event.function);
                }

            }else {
                var gridElement = buildControl(obj);
                if(obj.type==="date"){
                    gridElement.regEx =  /^(0?[1-9]|1[0-2])\/(0?[1-9]|1\d|2\d|3[01])\/(19|20)\d{2}$/;
                    gridElement.validate = true;
                    gridElement.jqObj.datepicker( {
                        dateFormat: 'mm/dd/yy',
                        changeMonth: true,
                        changeYear: true,
                        yearRange: "-100:+0"
                    });


                }

                obj.obj = gridElement;

            }

            if(obj.label){
                var label = createElement("label");
                label.jqObj.text(obj.label);
                label.jqObj.css("control-label");
                divCol.jqObj.append(label.jqObj);

            }

            row.jqObj.append(divCol.jqObj.append(gridElement.jqObj));
        });

    }
    // Adds a row to the grid
    this.addRows = function(rows){

        var scope_this = this;
        rows.forEach(function(row){
            var divRow  = createElement("div");
            divRow.setAttr("class","row");
            scope_this.addColumns(row,divRow);
            scope_this.jqObj.append(divRow.jqObj);

        });

    }
}
Table.prototpe = new Element();
function Table(table){
    /*
        Binds an HTML table element to this class.

    */
    this.table = table;
    this.jqObj = table.jqObj;
    this.elem = table;
    this.elem.jqObj = table.jqObj;
    function colMap(columns,tag){
        /*
            Creates the <th> tags for a row. Uses an array to build the columns.
        */
        return columns.map(function(col){ return "<"+tag+">"+col+"</"+tag+">"; });
    }
    this.addRow = function(columns){
        /*
            Adds rows to the table
         */
        this.table.append("<tr> "+ colMap(columns,"td")+"</tr>");
    }
    this.addColHeaders = function(columns){
        /*
            Adds columns headers to the table
         */
        this.table.prepend("<thead><tr> "+ colMap(columns,"th")+"</tr></thead>");

    }
    this.bindJSON = function(JSON,table){
        /*
            Populates the table using JSON data
         */
        var _this = this;
        table.clear();
        JSON.forEach(function(row){

                table.row.add(row);

           // _this.addRow(values);
        });
        table.draw();
    }

}
// Exports
exports.createElement = createElement;
exports.Element = Element;
exports.Table = Table;
exports.Component = Component;
exports.Grid = Grid;
exports.MultiSelect = MultiSelect;
exports.bindElements = bindElements;
exports.ClickStateButton =  ClickStateButton;
exports.Modal = Modal;
exports.List = List;
exports.DataTableCustom = DataTableCustom;
exports.collapsibleContainer = collapsibleContainer;
exports.inputTypes = ['multiSelect','date','vinButton','input']; // the allowed input types.