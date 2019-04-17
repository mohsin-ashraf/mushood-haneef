const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const CourseSchema = Schema({
  employeeId:{
    type:String,
    requierd:true    
  },
  trainingType:{
    trainingType:String,
    required:true
  },
  courseName:{
    type:String,
    required:true
  },
  paymentType:{
    type:String,
    required:true
  }
});

module.exports = Course = mongoose.model("Course",CourseSchema);

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