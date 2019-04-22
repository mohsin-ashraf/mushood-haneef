const express = require("express");
const router = express.Router();
const Course = require("../models/Course")
const SelectedCourse = require("../models/SelectedCourse");
const Employee = require("../models/Employee");
const TrainingSession = require("../models/TrainingSessions")

router.get("/",(req, res) => {
    Course.find({}).then(data =>{
        res.render('coursemanual',{
            data:data
        });
    }).catch(err => {
        console.log("ERROR WHILE LOADING THE COURSES");
        res.send("Error while laoding the courses.")
    })
});

// Add Course
router.get("/add-course",(req,res)=>{
    res.render("add-course");
});

// Add course post request
router.post("/add-course",(req,res)=>{
    const course = req.body;
    new Course(course).save().then(result =>{
        console.log(result);
        res.redirect("/course");
    }).catch(err => {
        console.log("Error: ",err)
        res.send("ERROR while adding course to databse")
    });
})

// Delete Course By Id
router.get("/delete/:id",(req,res)=>{
    const id = req.params.id;
    Course.deleteCourseById(id,()=>{
        res.redirect("/course");
    })
})


// Assign course to employee
router.get("/assign-course/:id",(req,res)=>{
    const id = req.params.id;
    Course.find({}).then(data =>{
        Employee.getEmployeeById(id,(err,employee) =>{
            if (err) throw err;
            res.render("assign-course",{
                data:data,
                employee:employee,
                id:id
            })
        })
    }).catch(err => {
        console.log("Error while loading the course assignment module: ",err)
        res.send("Error while loading the course Assignment module")
    });
});

// Assign course to employee post request
router.post("/assign-course/:id",(req,res)=>{
    console.log(req.body);
    const selectedCourse = {
        employeeId:req.body.employeeId,
        name:req.body.name,
        code:req.body.code,
        coordinator:req.body.coordinator,
        trainer:req.body.trainer,
        paymentType:req.body.paymentType
    }
    const trainingSession = {
        employeeId:req.body.employeeId,
        schedualedTime:req.body.schedualedTime,
        status:req.body.status,
        deliveryMethod:req.body.deliveryMethod,
        deliveryLocation: req.body.deliveryLocation,
        attendanceType:req.body.attendanceType,
        TCRequired:req.body.TCRequired,
    }
    new SelectedCourse(selectedCourse).save().then(courseResult => {
        new TrainingSession(trainingSession).save().then(trainingResult => {
            res.redirect("/course/assign-course/"+req.params.id)
        });
    });
});

module.exports = router;