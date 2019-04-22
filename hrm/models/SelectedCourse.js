const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const CourseSchema = Schema({
  employeeId:{
    type:String,
    required:true
  },
  name:{
    type:String,
    requierd:true    
  },
  code:{
    type:String,
    required:true
  },
  coordinator:{
    type:String,
    required:true
  },
  trainer:{
    type:String,
    required:true,
  },
  paymentType:{
    type:String,
    required:true
  }
});

module.exports = Course = mongoose.model("SelectedCourse",CourseSchema);

module.exports.addCourse = function(course,callback){
  course.save(callback);
}

module.exports.getCourseById = function(id, callback){
  Course.findById(id,callback);
}

module.exports.updateCourseById = function(id,updatedTrainingSession,callback){
  query = {_id:id};
  Course.updateOne(query,updatedTrainingSession,callback)
}

module.exports.deleteCourseById = function(id,callback){
  query = {_id:id};
  Course.remove(query,callback)
}