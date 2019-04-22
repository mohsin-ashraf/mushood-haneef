const express = require("express");
const router = express.Router();
const Employee = require("../models/Employee")
router.get("/",(req,res)=>{
  Employee.find({}).then(data =>{
    res.render('salary',{
      data:data
    });
  }).catch(err =>{
    console.log("ERROR:",err);
    res.send("Error while loading the salary module")
  })
});

module.exports = router;