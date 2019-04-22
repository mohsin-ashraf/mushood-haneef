const express = require("express");
const router = express.Router();
const Employee = require("../models/Employee");
const Feedback = require("../models/Feedback");

router.get("/give-feedback/:id",(req,res)=>{
  const _id = req.params.id;
  Employee.getEmployeeById(_id,(err,data) => {
    if (err) {
      console.log("ERROR: "+err);
      res.send("ERROR while loading feedback template")
    }
    console.log("FEEDBACK: "+data);
    res.render("givefeedback",{
      _id:_id,
      name:data.name
    });
  });
});

router.post("/give-feedback/:id",(req,res)=>{
  const feedback = req.body;
  new Feedback(feedback).save().then(result =>{
    console.log("Feedback saved Successfully");
    res.redirect("/reviews/performance");
  }).catch(err =>{
    console.log("Error while saving the feedback from the employee");
    res.send("Error while saving the feedback from the employee.");
  })
});

router.get("/delete/:id",(req,res)=>{
  const id = req.params.id;
  Feedback.deleteFeedbackById(id,(err,result) => {
    res.redirect("/reviews/performance")
  })
});

module.exports = router;