
//Regular pie chart example
nv.addGraph(function() {
  var chart = nv.models.pieChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .showLabels(true)     //Display pie labels
      .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
      .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
      .donut(true)
      .showLegend(false)
      .color(['#E62020', '#50C878'])
      .donutRatio(0.50);

    d3.select("#chart").append('svg')
        .datum(getData("production_year"))
        .transition().duration(350)
        .call(chart);

  return chart;
});

//Donut chart example
nv.addGraph(function() {
  var chart = nv.models.pieChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .showLabels(true)     //Display pie labels
      .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
      .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
      .donut(true)
      .showLegend(false)
      .color(['#E62020', '#50C878'])
      .donutRatio(0.50);

    d3.select("#chart2").append('svg')
        .datum(getData("spectator_rate"))
        .transition().duration(350)
        .call(chart);

  return chart;
});

nv.addGraph(function() {
  var chart = nv.models.pieChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .showLabels(true)     //Display pie labels
      .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
      .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
      .donut(true)
      .showLegend(false)
      .color(['#E62020', '#50C878'])
      .donutRatio(0.50);

    d3.select("#chart3").append('svg')
        .datum(getData("language"))
        .transition().duration(350)
        .call(chart);

  return chart;
});

nv.addGraph(function() {
  var chart = nv.models.pieChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .showLabels(true)     //Display pie labels
      .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
      .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
      .donut(true)
      .showLegend(false)
      .color(['#E62020', '#50C878'])
      .donutRatio(0.50);

    d3.select("#chart4").append('svg')
        .datum(getData("original_movie_title"))
        .transition().duration(350)
        .call(chart);

  return chart;
});

nv.addGraph(function() {
  var chart = nv.models.pieChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .showLabels(true)     //Display pie labels
      .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
      .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
      .donut(true)
      .showLegend(false)
      .color(['#E62020', '#50C878'])
      .donutRatio(0.50);

    d3.select("#chart5").append('svg')
        .datum(getData("critic_rate"))
        .transition().duration(350)
        .call(chart);

  return chart;
});

nv.addGraph(function() {
  var chart = nv.models.pieChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .showLabels(true)     //Display pie labels
      .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
      .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
      .donut(true)
      .showLegend(false)
      .color(['#E62020', '#50C878'])
      .donutRatio(0.50);

    d3.select("#chart6").append('svg')
        .datum(getData("budget"))
        .transition().duration(350)
        .call(chart);

  return chart;
});

nv.addGraph(function() {
  var chart = nv.models.pieChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .showLabels(true)     //Display pie labels
      .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
      .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
      .donut(true)
      .showLegend(false)
      .color(['#E62020', '#50C878'])
      .donutRatio(0.50);

    d3.select("#chart7").append('svg')
        .datum(getData("realisator"))
        .transition().duration(350)
        .call(chart);

  return chart;
});

nv.addGraph(function() {
  var chart = nv.models.pieChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .showLabels(true)     //Display pie labels
      .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
      .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
      .donut(true)
      .showLegend(false)
      .color(['#E62020', '#50C878'])
      .donutRatio(0.50);

    d3.select("#chart8").append('svg')
        .datum(getData("actors"))
        .transition().duration(350)
        .call(chart);

  return chart;
});

nv.addGraph(function() {
  var chart = nv.models.pieChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .showLabels(true)     //Display pie labels
      .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
      .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
      .donut(true)
      .showLegend(false)
      .color(['#E62020', '#50C878'])
      .donutRatio(0.50);

    d3.select("#chart9").append('svg')
        .datum(getData("distributor"))
        .transition().duration(350)
        .call(chart);

  return chart;
});

nv.addGraph(function() {
  var chart = nv.models.pieChart()
      .x(function(d) { return d.label })
      .y(function(d) { return d.value })
      .showLabels(true)     //Display pie labels
      .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
      .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
      .donut(true)
      .showLegend(false)
      .color(['#E62020', '#50C878'])
      .donutRatio(0.50);

    d3.select("#chart10").append('svg')
        .datum(getData("summary"))
        .transition().duration(350)
        .call(chart);

  return chart;
});
//Pie chart example data. Note how there is only a single array of key-value pairs.
function getData(attribute) {
  null_value[attribute]
  return  [
      {
        "label": "Pourcentage de " + attribute + " manquants",
        "value" : null_value[attribute]
      },
      {
        "label": "Pourcentage de " + attribute + " présent",
        "value" :  100 - null_value[attribute]
      }
    ];
}
