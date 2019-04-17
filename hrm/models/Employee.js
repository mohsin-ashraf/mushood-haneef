const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const EmployeeSchema = new Schema({
  name:{
    type:String,
    required:true
  },
  code:{
    type:Number,
    require:true
  },
  jobTitle:{
    type:String,
    required:true
  },
  joiningDate:{
    type:Date,
    default:Date.now()
  }
});

module.exports = Employee = mongoose.model("employee",EmployeeSchema);

module.exports.addEmployee = function(newEmployee,callback){
  newEmployee.save(callback);
}

module.exports.getEmployeeById = function(id, callback){
  Employee.findById(id,callback);
}

module.exports.updateEmployeeById = function(id,updatedEmployee,callback){
  query = {_id:id};
  Employee.updateOne(query,updatedEmployee,callback)
}

module.exports.deleteEmployeeById = function(id,callback){
  query = {_id:id};
  Employee.remove(query,callback)
}
