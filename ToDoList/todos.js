// Completed items should toggle `completed` class
$("ul").on("click", "li", function() {
    $(this).toggleClass("completed");
});

// `li`s should be removed when the span is clicked
$("ul").on("click", ".trash", function(e) {
    $(this).parent().fadeOut(300, function() {
        $(this).remove();
    });
    e.stopPropagation();
});

// Toggles the input interface
$(".fa-pencil-alt").click(function() {
    $("input").fadeToggle(0);
    $("input").focus();
});

// New todo should be added when `enter` key is pressed
$("input").keypress(function(e) {
    // Input is required
    if(e.which === 13 && $(this).val() !== "") {
        var toDoHTML = "<li>" + $(this).val() + "<span class=\"trash\"><i class=\"fas fa-minus-square\"></i></span></li>";
        $("ul").append(toDoHTML);
        $(this).val("");
    }
});

