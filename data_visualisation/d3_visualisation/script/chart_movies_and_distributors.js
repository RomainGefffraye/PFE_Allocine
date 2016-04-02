var chart;
var data = getData(["null"]);

$( "#addData" ).click(function() {
  var e = document.getElementById("dropdown");
  var company = e.options[e.selectedIndex].text;
  var span = document.createElement("SPAN");
  var button = document.createElement("BUTTON");
  span.setAttribute("id", company.replace(/\s/g));
  button.className = "tagButton";
  button.setAttribute("onclick", "deleteFather(this)")
  button.setAttribute("value", company)
  button.appendChild(document.createTextNode(company));
  span.appendChild(button)
  $("#dataInChart").append(span);
  pushData()
});

function deleteFather(company){
  company.parentNode.parentNode.removeChild(company.parentNode);
  pushData();
}

function pushData(listOfCompany){
  var companies = [];
  $(".tagButton").each(function() {
    companies.push(this.value);
  })
  var data = getData(companies);
  d3.select('#chart')
    .datum(data)
    .call(chart);
}

$.each(movies_per_years_per_distributor, function (key, value) {
  $("#dropdown").append("<option id=" + key.replace(/\s/g, '') + ">" + key + "</option>");
});

nv.addGraph(function() {
  chart = nv.models.lineChart()
        .options({
          transitionDuration: 300,
          useInteractiveGuideline: true
        });
        // chart sub-models (ie. xAxis, yAxis, etc) when accessed directly, return themselves, not the parent chart, so need to chain separately
        chart.xAxis
          .axisLabel("Année");
        chart.yAxis
          .axisLabel('Quantité (Unité)');
        d3.select('#chart').append('svg')
            .datum(data)
            .call(chart);
        nv.utils.windowResize(chart.update);
  return chart;
});


$('#dropdown').change(function () {
  var $selected = $(this).find(":selected")[0];
  if ($selected) {
    data = getData([$selected.text]);
      d3.select('#chart')
        .datum(data)
        .call(chart);
  }
});

function getRandomColor() {
  var letters = '0123456789ABCDEF'.split('');
  var color = '#';
  for (var i = 0; i < 6; i++ ) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
}

function getData(companies) {
  var data = [];
  for (company in companies) {
    var graphCompany = {
      area: true,
      values: movies_per_years_per_distributor[companies[company]],
      key: companies[company],
      color: getRandomColor(),
      fillOpacity: 0
    }
    data.push(graphCompany)
  }
  return data;
};
