// Import required packages
var express = require("express");
var app = express();
var mongoose = require("mongoose");
var bodyParser = require("body-parser");

// Set app.js settings
app.set("view engine", "ejs");
app.use(bodyParser.urlencoded({extended: true}));

// Setup mongoDB database
mongoose.connect('mongodb://localhost/miniblog_app');
var blogSchema = new mongoose.Schema({
    title: String,
    content: String,
    image: String,
    date: {type: Date, default: Date.now}
});
var Blog = mongoose.model("Blog", blogSchema);

// Blog.create({title: "B1", content:"This is B1..", image: "https://www.w3schools.com/w3css/img_lights.jpg"});
// Blog.create({title: "B2", content:"This is B2..", image: "https://www.w3schools.com/w3css/img_lights.jpg"});
// Blog.create({title: "B3", content:"This is B3..", image: "https://www.w3schools.com/w3css/img_lights.jpg"});

// ------- RESTFUL ROUTES -------
app.get("/", function(req, res) {
    res.redirect("/blogs");
});

// INDEX route
app.get("/blogs", function(req, res) {
    // Retrieve all the blogs
    Blog.find({}, function(err, foundBlogs) {
        if(err) {
            console.log("Error occurred when trying to list all blogs.");
        } else {
            // Passes `foundBlogs` into `index.ejs` as the argument `blogs` for use
            res.render("index", {blogs: foundBlogs});
        }
    });
});

// NEW route
app.get("/blogs/new", function(req, res) {
    // We only need to render the "new" form
    res.render("new");
});

// CREATE route
app.post("/blogs", function(req, res) {
    // Extract `newBlog` from `req.body` and add it to database
    var newBlog = req.body.newBlog;
    Blog.create(newBlog, function(err, addedBlog) {
        if(err) {
            console.log("Error occurred when trying to add new blog.");
            res.render("new");
        } else {
            res.redirect("/blogs");
        }
    })
});

// SHOW route
// app.get("/blogs/:id", function(req, res) {
//     res.render("show");
// });

// EDIT route
// app.get("/blogs/:id/edit", function(req, res) {
//     res.render("edit");
// });

// UPDATE route
// app.put("/blogs/:id", function(req, res) {
//     res.render("show");
// });

// DESTROY route
// app.delete("/blogs/:id", function(req, res) {
//     res.render("index");
// });

app.get("*", function(req, res) {
    res.render("nopage");
});
// ------------------------------


// Listen on port 4000
app.listen(4000, function(req, res) {
    console.log("Server has started...");
});
