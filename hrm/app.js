var express = require('express');
var exphbs  = require('express-handlebars');
const mongoose = require("mongoose");

mongoose.connect("mongodb://localhost:27017/e-hrm",{useNewUrlParser:true}).then(()=>{
    console.log("Connected to mongodb server");
}).catch(err => {
    console.log("Error while connecting to database: ",err)
});

const port = process.env.PORT || 3000;
var app = express();

app.engine('handlebars', exphbs({defaultLayout: 'main'}));
app.set('view engine', 'handlebars');


// Requiring routes...
const indexRoute = require("./routes/index");
const salaryRoute = require("./routes/salary");
const staffRoute = require("./routes/staff");
const courseRoute = require("./routes/course");


// Using routes
app.use('/', indexRoute);
app.use('/salary', salaryRoute);
app.use('/staff',  staffRoute);
app.use('/course', courseRoute );

app.use((req,res)=>{
    res.send("Invalid Request")
})
app.listen(port,()=>{
    console.log("Server is running on port "+port);
});