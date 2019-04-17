const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const TrainingSchema = Schema({
  employeeId:{
    type:String,
    requierd:true    
  },
  schedualedTime:{
    type:Date,
    requried:true
  },
  status:{
    type:String,
    required:true,
  },
  deliveryMethod:{
    type:String,
    required:true
  },
  deliveryLocation:{
    type:String,
    required:true
  },
  attendanceType:{
    type:String,
    required:true
  },
  TCRequired:{
    type:String,
    required:true
  }
});

module.exports = Training = mongoose.model("employee",TrainingSchema);


module.exports.addTrainingSession = function(training,callback){
  training.save(callback);
}

module.exports.getTrainingById = function(id, callback){
  Training.findById(id,callback);
}

module.exports.updateTrainingSession = function(id,updatedTrainingSession,callback){
  query = {_id:id};
  Training.updateOne(query,updatedTrainingSession,callback)
}

module.exports.deleteTrainingById = function(id,callback){
  query = {_id:id};
  Training.remove(query,callback)
}