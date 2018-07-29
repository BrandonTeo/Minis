function getFrequencies(word) {
    var dict = []
    var sortedSplits = word.split("").sort();

    // The loop below utilizes the fact that `sortedSplits` is sorted
    for (var i = 0; i < sortedSplits.length; i++) {
        var last_elem = dict[dict.length - 1];
        if (last_elem && last_elem.character === sortedSplits[i]) {
            last_elem.count += 1;
        } else { // This is a newly seen character
            dict.push({character: sortedSplits[i], count: 1});
        }
    }

    return dict
}

// Deal with submit button -- essentially our update function
d3.select("form").on("submit", function() {
    // Prevent actually submitting the form
    d3.event.preventDefault();

    var input = d3.select("input").property("value");
    
    var updates = d3.select("#letters").selectAll(".letter")
                                       .data(getFrequencies(input), function(d) {
                                            return d.character;
                                       });
                              
    // Step 1 & 2 of update pattern
    updates
        .classed("new", false)
        .exit()
        .remove();
    
    updates
        .enter() // Step 3 of update pattern
        .append("div")
          .classed("letter", true)
          .classed("new", true)
        .merge(updates)
          .style("width", "20px")
          .style("line-height", "20px")
          .style("margin-right", "5px")
          .style("height", function(d) {
            return d.count * 20 + "px";
          })
          .text(function(d) {
            return d.character;
          });

    d3.select("#phrase").text("Analysis of: " + input);
    d3.select("#count").text("(new chars: " + updates.enter().nodes().length + ")");
    d3.select("input").property("value", "");
});

d3.select("#reset").on("click", function() {
    d3.selectAll(".letter").remove();
    d3.selectAll("#phrase").text("");
    d3.selectAll("#count").text("");
});
