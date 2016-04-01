nv.addGraph(function() {
  var chart = nv.models.discreteBarChart()
      .x(function(d) { return d.label })    //Specify the data accessors.
      .y(function(d) { return d.value })
      .showXAxis(true)
      .staggerLabels(false)    //Too many bars and not enough room? Try staggering labels.
      .tooltips(true);

  chart.yAxis.tickFormat(d3.format(',f'));

  d3.select('#chart').append('svg')
      .datum(production_years_number)
      .call(chart);

  nv.utils.windowResize(chart.update);

  return chart;
});
