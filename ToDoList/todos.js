// Completed items should toggle `completed` class
$("ul").on("click", "li", function() {
    $(this).toggleClass("completed");
});

// `li`s should be removed when the span is clicked
$("ul").on("click", ".trash", function(e) {
    $(this).parent().fadeOut(500, function() {
        $(this).remove();
    });
    e.stopPropagation();
});

// new todo should be added when `enter` key is pressed
$("input").keypress(function(e) {
    if(e.which === 13) {
        var toDoHTML = "<li><span class=\"trash\">O</span> " + $(this).val() + "</li>";
        $("ul").append(toDoHTML);
        $(this).val("");
    }
});

