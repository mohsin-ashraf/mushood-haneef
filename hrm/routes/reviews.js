const express = require("express");
const router = express.Router();
const Employee = require("../models/Employee");
const Review = require("../models/Review")
const Feedback = require("../models/Feedback")

// get route for giving reivew
router.get("/give-review/:id",(req,res)=>{
  const id = req.params.id
  Employee.getEmployeeById(id,(err,employee)=>{
    console.log(employee)  
    if (err){
        console.log(err);
        res.send("Error while loading review data for this employee")
      }else{
        res.render("givereview",{
          name:employee.name,
          _id:employee._id
      })
      }
  })
})

// post route for giving review
router.post("/givereview/:id",(req,res)=>{
  const id = req.params.id;
  review = req.body;
  new Review(review).save().then(result =>{
    console.log("Review saved successfully")
    res.redirect("/")
  }).catch(err =>{
    console.log(err);
    res.send("Error while giving review about "+review.name)
  })
});

// performance...
router.get("/performance",(req,res)=>{
  Review.find({}).then(review =>{
    Feedback.find({}).then(feedback =>{
      res.render("performance",{
        review:review,
        feedback:feedback
      });
    });
  }).catch(err =>{
    console.log("Error while loading data about the reviews")
  })
});

// delete review
router.get("/delete/:id",(req,res)=>{
  const id = req.params.id
  Review.deleteReviewById(id,()=>{
    res.redirect("/reviews/performance"); 
  })
})

module.exports = router;