const express = require("express");
const router = express.Router();

router.get("/",(req,res)=>{
  res.render('index');
});

router.get("/specific-jobs",(req,res)=>{
  res.render("specificjobs")
})

router.get("/training-courses",(req,res)=>{
  res.render("training-courses")
});

router.get("/training-sessions",(req,res)=>{
  res.render("training-sessions")
});

router.get("/performance",(req,res)=>{
  res.render("performance")
});

module.exports = router;