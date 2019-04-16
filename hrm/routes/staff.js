const express = require("express");
const router = express.Router();

router.get("/",(req, res) => {
  res.render('ourstaff');
});

module.exports = router;