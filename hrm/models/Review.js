const mongoose = require("mongoose")
const Schema = mongoose.Schema;

const ReviewSchema = Schema({
  employeeId:{
    type:String,
    requierd:true    
  },
  reviewer:{
    type:String,
    required:true
  },
  template:{
    type:String,
    required:true
  },
  status:{
    type:String,
    required:true
  },
  reviewDate:{
    type:Date,
    default:Date.now()
  },
  dueOn:{
    type:String,
    default:Date.now()
  },
  start:{
    type:Date,
    default:Date.now()
  },
  end:{
    type:Date,
    default:Date.now()
  }
});

module.exports = Review = mongoose.model("review",ReviewSchema);

module.exports.addReview = function(review,callback){
  review.save(callback);
}

module.exports.getReviewById = function(id, callback){
  Review.findById(id,callback);
}

module.exports.updateReviewById = function(id,updatedReview,callback){
  query = {_id:id};
  Review.updateOne(query,updatedReview,callback)
}

module.exports.deleteReviewById = function(id,callback){
  query = {_id:id};
  Review.remove(query,callback)
}