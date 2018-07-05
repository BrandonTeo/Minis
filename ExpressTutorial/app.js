var express = require("express");
var app = express();

// Set up routes
app.get('/', function(req, res) {
    res.send("Welcome to the root page!");
});

app.get('/speak/:animal', function(req, res) {
    if(req.params.animal === "pig") {
        res.send("Welcome to the pig page!")
    } else if(req.params.animal === "cow") {
        res.send("Welcome to the cow page!")
    } else if(req.params.animal === "dog") {
        res.send("Welcome to the dog page!")
    } else {
        res.send("Sorry, unknown animal!");
    }
});

app.get('/repeat/:phrase/:count', function(req, res) {
    if(Number.isInteger(Number(req.params.count))) {
        var toRet = ""
        for(var i = 0; i < req.params.count; i++) {
            toRet += req.params.phrase + " "
        }
        res.send(toRet);
    } else {
        res.send("Sorry, count has to be a number!");
    }
});

app.get('*', function(req, res) {
    res.send("Sorry, page not found!");
});

// Listen on port 3000
app.listen(3000, "127.0.0.1", function() {
    console.log("Server has started!");
}); 

