// Import required packages
var express = require("express");
var app = express();
var mongoose = require("mongoose");
var bodyParser = require("body-parser");
var methodOverride = require("method-override");

// Set app.js settings
app.set("view engine", "ejs");
app.use(express.static('public'));
app.use(bodyParser.urlencoded({extended: true}));
app.use(methodOverride('_method'));

// Setup mongoDB database
var dbName = 'miniblog_app'
mongoose.connect('mongodb://localhost/' + dbName);
var blogSchema = new mongoose.Schema({
    title: String,
    content: String,
    image: String,
    date: {type: Date, default: Date.now}
});
var Blog = mongoose.model("Blog", blogSchema);

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
    Blog.create(req.body.newBlog, function(err, createdBlog) {
        if(err) {
            console.log("Error occurred when trying to add new blog.");
            res.redirect("/blogs/new");
        } else {
            res.redirect("/blogs");
        }
    })
});

// SHOW route
app.get("/blogs/:id", function(req, res) {
    // Attempt to find the blog with id `:id`
    Blog.findById(req.params.id, function(err, foundBlog) {
        if(err) {
            console.log("Error occurred when trying to find and show blog.");
            res.redirect("/blogs");
        } else {
            res.render("show", {blog: foundBlog});
        }
    });
});

// EDIT route
app.get("/blogs/:id/edit", function(req, res) {
    // Attempt to find the blog with id `:id`
    Blog.findById(req.params.id, function(err, foundBlog) {
        if(err) {
            console.log("Error occurred when trying to find and edit blog.");
            res.redirect("/blogs");
        } else {
            res.render("edit", {blog: foundBlog});
        }
    });
});

// UPDATE route
app.put("/blogs/:id", function(req, res) {
    // Attempt to find the blog with id `:id` and update it in our database
    Blog.findByIdAndUpdate(req.params.id, req.body.updatedBlog, function(err, updatedBlog) {
        if(err) {
            console.log("Error occurred when trying to find and update blog.");
        }
        res.redirect("/blogs/" + updatedBlog._id);
    });
});

// DESTROY route
app.delete("/blogs/:id", function(req, res) {
    // Attempt to find the blog with id `:id` and remove it from database
    Blog.findByIdAndRemove(req.params.id, function(err, removedBlog) {
        if(err) {
            console.log("Error occurred when trying to find and remove blog.");
        }
        res.redirect("/blogs");
    });
});

app.get("*", function(req, res) {
    res.render("nopage");
});
// ------------------------------

// Listen on port 4000
app.listen(4000, function(req, res) {
    console.log("Server has started...");
});
