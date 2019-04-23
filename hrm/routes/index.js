const express = require("express");
const router = express.Router();
const Employee = require("../models/Employee")
const SelectedCourse = require("../models/SelectedCourse");
const TrainingSession = require("../models/TrainingSessions");

router.get("/",(req,res)=>{
  Employee.find({}).then(data=>{
    console.log("Data: ",data)
    res.render('index',{
      data:data
    });
  }).catch(()=>{
    console.log("Sorry Server Error");
    res.redirect("/page_not_found")
  })
});

router.get("/specific-jobs/:jobTitle",(req,res)=>{
  jobTitle = req.params.jobTitle
  Employee.find({jobTitle:jobTitle}).then(data=>{
    console.log(data)
    res.render("specificjobs",{
      data:data
    })
  }).catch(err=>{
    console.log("Error: ",err);
    res.redirect("/")
  })
})

//delete Job title record
router.get("/delete/:id",(req,res)=>{
  Employee.deleteEmployeeById(req.params.id,(err,data)=>{
    res.redirect("/");
  })
})

// edit employee get request
router.get("/update-employee/:id",(req,res)=>{
  const id = req.params.id;
  Employee.find({_id:id}).then(data=>{
    console.log(data)
    res.render("editEmployee",{
      data:data
    })
  }).catch(err =>{
    console.log(err);
    res.send("Cannot update employee")
  })
})

//edit employee post request
router.post("/update-employee/:id",(req,res)=>{
  const id = req.params.id;
  Employee.updateEmployeeById(id,req.body,(result)=>{
    console.log("Updated user successfully")
    res.redirect()
  })
})

router.get("/training-courses/:id",(req,res)=>{
  const employeeId = req.params.id;
  SelectedCourse.find({employeeId:employeeId}).then(data => {
    res.render("training-courses",{
      data:data
    })
  })
});

router.get("/training-sessions/:id/:name",(req,res)=>{
  const employeeId = req.params.id;
  const cname = req.params.name
  console.log(cname)
  TrainingSession.find({employeeId:employeeId}).then(data => {
    data['cname'] = cname;
    console.log("After changing data"+data)
    res.render("training-sessions",{
      data:data,
    });
  });
});

// Add employee Post
router.post("/add-new-employee",(req,res)=>{
  const code = req.body.code;
  const name = req.body.name;
  const jobTitle = req.body.jobtitle;
  const joiningDate = req.body.joiningdate;
  const salaryComponentType = req.body.salaryComponentType;
  const salaryDetails = req.body.salaryDetails;
  const currency = req.body.currency;
  const salary = req.body.salary;
  console.log(req.body)
  const employee = new Employee({
    code,
    name,
    jobTitle,
    joiningDate,
    salaryComponentType,
    salaryDetails,
    currency,
    salary
  });
  Employee.addEmployee(employee,(err)=>{
    console.log(err);
  })
  res.redirect("/")
});

router.get("/job-description/:jobTitle",(req,res)=>{
  res.render("job-description")
})

module.exports = router;