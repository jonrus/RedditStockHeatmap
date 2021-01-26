async function fetchFilterData(event) {
    event.preventDefault();
    const data_date = document.getElementById("startDatePicker").value;
    const heat_limit = document.getElementById("minRedditHeat").value;
    let res = await axios.get(`/api/date/${data_date}?heat=${heat_limit}`);
    //TODO: ADD error handling - Show user when they get no results with their limits, etc
    buildBubbleChart(res.data);
}

function buildBubbleChart(formData) {
    dataset = {
        "children": formData
    }

    document.getElementById("bubbleMap").innerHTML = '';

    const diameter = 870;
    var color = d3.scaleOrdinal(d3.schemeCategory20);

    var bubble = d3.pack(dataset)
        .size([diameter, diameter])
        .padding(3);

    var svg = d3.select("main")
        .append("svg")
        .attr("width", diameter)
        .attr("height", diameter)
        .attr("class", "bubble");

    var nodes = d3.hierarchy(dataset)
        .sum(function(d) { return d.Count; });

    var node = svg.selectAll(".node")
        .data(bubble(nodes).descendants())
        .enter()
        .filter(function(d){
            return  !d.children
        })
        .append("g")
        .attr("class", "node")
        .attr("transform", function(d) {
            return "translate(" + d.x + "," + d.y + ")";
        });

    node.append("title")
        .text(function(d) {
            return d.data.Name;
        });

    node.append("circle")
        .attr("r", function(d) {
            return d.r;
        })
        .style("fill", function(d,i) {
            return color(i);
        });
    
    node.append("a")
        .attr("href", function(d) {
            return "/sym/" + d.data.Symbol;
        })
    .append("text")
        .attr("dy", "-0.4em")
        .style("text-anchor", "middle")
        .text(function(d) {
            return d.data.Symbol;
        })
        .attr("font-family",  "Gill Sans", "Gill Sans MT")
        .attr("font-size", function(d){
            return d.r/2;
        })
        .attr("fill", "black");    

    node.append("text")
            .attr("dy", ".2em")
            .style("text-anchor", "middle")
            .text(function(d) {
                if (d.data.Name.length > 14) {
                    return d.data.Name.substring(0, d.r / 3) + "...";
                }
                return d.data.Name;
            })
            .attr("font-family", "sans-serif")
            .attr("font-size", function(d){
                return d.r/5;
            })
            .attr("fill", "black");

    node.append("text")
        .attr("dy", "1.3em")
        .style("text-anchor", "middle")
        .text(function(d) {
            return d.data.Count;
        })
        .attr("font-family",  "Gill Sans", "Gill Sans MT")
        .attr("font-size", function(d){
            return d.r/2;
        })
        .attr("fill", "black");

    d3.select(self.frameElement)
        .style("height", diameter + "px");
}

//////////////////////////
// Event Listeners
//////////////////////////
document.addEventListener("DOMContentLoaded", fetchFilterData); // Perform first data fetch after page loads
document.getElementById("submitFilterForm").addEventListener("click", fetchFilterData);