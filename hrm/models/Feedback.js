const mongoose = require("mongoose");
const Schema = mongoose.Schema;

const FeedbackSchema = Schema({
  employeeId:{
    type:String,
    requierd:true    
  },
  review:{
    type:String,
    required:true
  },
  status:{
    type:String,
    requierd:true
  },
  employeeName:{
    type:String,
    requierd:true
  }
});

module.exports = Feedback = mongoose.model("feedback",FeedbackSchema);


module.exports.addFeedback = function(feedback,callback){
  feedback.save(callback);
}

module.exports.getFeedbackById = function(id, callback){
  Feedback.findById(id,callback);
}

module.exports.updateFeedbackById = function(id,updatedFeedback,callback){
  query = {_id:id};
  Feedback.updateOne(query,updatedFeedback,callback)
}

module.exports.deleteFeedbackById = function(id,callback){
  query = {_id:id};
  Feedback.remove(query,callback)
}