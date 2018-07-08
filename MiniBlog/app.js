// Import required packages
var express = require("express");
var app = express();

// Set app.js settings
app.set("view engine", "ejs");

// ------- RESTFUL ROUTES ------- 
app.get("/", function(req, res) {
    res.redirect("/blogs");
});

app.get("/blogs", function(req, res) {
    res.render("index");
});


// app.get("/blogs/new")
// app.post("/blogs")

// app.get("/blogs/:id")
// app.get("/blogs/:id/edit")
// app.put("/blogs/:id")

// app.delete("/blogs/:id")


// Listen on port 4000
app.listen(4000, function(req, res) {
    console.log("Server has started...");
});
