// Polyfills
var date = require("./date");
var element = require("../utils/elements");
var network = require("../utils/network");
function hasValue(obj){
   // Determines if a object has a value.
   try{
       if(typeof(obj.value)==="function")
           return true;
   } catch(err){
       return false;
   }
}

function Page(components,JSON){
    this.JSON = JSON;
    this.gridRows = components;
    this.grid = null;
    this.inputComponent = components;
    this.components = _.flatten(components);

    this.bindData = function(data){
        // creates the databindings for all the elements
        var  JSON =this.JSON;

        this.gridRows.forEach(function(row){
             /*
                Function binds the data to ethe proper inputs
             */
              var componentsToBind = row.filter(function(obj){   return typeof(obj.binding)!=='undefined';  });
              componentsToBind.forEach(function(obj){

                     obj.obj.bindJSON(JSON[obj.binding]);


              });

        });


    };

    this.render = function(){
       this.grid = new element.Grid($("#control"));
       this.grid.addRows(this.gridRows);
    }
    this.bindEvent = function(componentName,callback){

        // Maps the event to the input values, so when an even is fired that control has access to the input values that the user has entered or selected.
        var component = _.findWhere(this.components,{name:componentName });
        var values = this.components.filter(function(obj){ return hasValue(obj)===true; }).map(function(obj){ return obj.value; });
        if(component!==undefined)
            component.event.function =  function(){ callback(values); };
    }
    this.getInputs = function(callback1,callback2){
        // the first callback is used to determine what the specific event does with the input values. Callback2 is used to use the input values after callback1 has done something with them.
        var query = {};
        var meta =  {};
        var userInput = this.components.filter(function(obj){ return element.inputTypes.indexOf(obj.type)!==-1 });
        var valid = []; //used to validate the input
        userInput.forEach(function(obj){
            if(obj.obj.custom!==null){
                var metadata = obj.obj.custom();
                meta[metadata.name] = metadata.value;
                query[obj.varName] = obj.obj.val();
            }else {

                if (obj.obj.validate === true) {
                    if(obj.type==="date")
                        obj.obj.filter = function(val){ return new Date(val).toMysqlFormat() };
                    valid.push({name: obj.name, valid: obj.obj.regExValidate(), type: obj.type});
                }
                query[obj.name] = obj.obj.val();
            }
        });
        callback1({validation:valid,query:query,meta:meta},callback2);

    }
    this.clearInputs = function(data){

        $("input").val('');

        var unbind= this.components.filter(function(obj){   return typeof(obj.binding)!=='undefined';  });
        unbind.forEach(function(obj){
            obj.obj.jqObj.empty();
            obj.obj.select.jqObj.empty();
            delete obj.obj;
            obj.obj =  new element.MultiSelect( obj.binding )
        })

        $("#control").empty();
        var con = element.createElement("div");
        con.jqObj.attr("id","control");
        $("#divForm").append(con.jqObj);
        var reportsPage = new Page(components,data);

        this.components.forEach(function(comp){ comp.obj.reset(); });
        this.render();
        this.bindData();
    }


}



module.exports.Page = Page;