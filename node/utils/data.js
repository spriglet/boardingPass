var compare = require("./JSONrecordsCompare.js");
var  error = require("./error.js");
var compareFields = compare.sameFields;

function DataSet(jsonData){
    this.data = jsonData;
    this.deleteRecords = function(fieldName,fieldValue){
        this.data =  _.filter(this.data,function(record){ return record[fieldName]!== fieldValue;  });

    },this.addRecord = function (record){
        if(!this.data.length || compareFields(record,this.data[0])) {
            this.data.push(record);
        } else {
            var diff1 = _.difference(_.keys(record),_.keys(this.data[0]));
            var diff2 = _.difference(_.keys(this.data[0]),_.keys(record));
            throw new error.UserException("Fields do not Match:("+diff1.concat(diff2)+")");
        }
    },this.valueEquals = function(fieldName,fieldValue){
        return _.filter(this.data,function(record){ return record[fieldName]=== fieldValue  });
    },this.where = function(fieldName,fieldValue){
        return _.filter(this.data,function(record){ return record[fieldName]== fieldValue  });
    },this.select = function(fieldNames){
        return _.map(this.data,function(row){  return '{'+  _.map(fieldNames,function(name){ return name+' :'+ row[name]   }).join(',')+'}';  })
    }
    this.groupBy = function(groupByColumns,aggrColumns,operations){
        var func = {
                    "sum":function(memo,num){ return memo +num; },
                    "count":function(memo){ return memo + 1;   }
                    }

    }
}



function convertJsonToCSV(json){
    var str = "";
    var getColumns = function(column){ return '"'+column+'"';  };
    str +=  _.map(_.keys(json[0]),getColumns ).join(",")+'\n';
    json.forEach(function(row){
        str += _.map(row,getColumns).join(",")+'\n';
    })
    return str;

}

module.exports.jsonToCsv = function(json,filename){


    //converter.json2csv(json,function(error,csv){

        var link = document.createElement('a');
        link.setAttribute('download', filename);
        link.setAttribute('href','data:text/csv;charset=utf-8,' + convertJsonToCSV(json));
        link.click();

    //},options);

}

module.exports.DataSet =  DataSet;
