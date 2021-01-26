google.charts.load('current', {'packages':['line', 'corechart']});
google.charts.setOnLoadCallback(fetchSymbolData);

async function fetchSymbolData() {
    sym = document.getElementById("symName").innerHTML;
    document.getElementById("lineChart").innerHTML = '<div class="spinner-border text-success" role="status"><span class="visually-hidden">Loading Reddit Heat Data...</span></div>';

    let res = await axios.get(`/api/sym/${sym}`);
    console.log(res.data);
    if (res.data.error) {
        document.getElementById("lineChart").innerHTML = res.data.error;
    }
    else {
        drawChart(res.data);
    }
}
function drawChart(chartData) {
    console.log(chartData);
let chartDiv = document.getElementById('lineChart');

let data = new google.visualization.DataTable();
data.addColumn('string', 'Date');
data.addColumn('number', "Reddit Heat");

data.addRows(chartData.data);

let materialOptions = {
  chart: {
    title: chartData.chart.title
  },
  width: 1000,
  height: 500,
  series: {
    // Gives each series an axis name that matches the Y-axis below.
    0: {axis: 'Reddit Heat'},
  },
  axes: {
    // Adds labels to each axis; they don't have to match the axis names.
    y: {
      Temps: {label: 'Reddit Heat Index'},
    }
  }
};
      function drawMaterialChart() {
        let materialChart = new google.charts.Line(chartDiv);
        document.getElementById("lineChart").innerHTML = "";
        materialChart.draw(data, materialOptions);
      }
      drawMaterialChart();
}