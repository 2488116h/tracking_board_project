
  $(document).ready(function (){
    // Global Trends Tab
    loadMap("cases", "New Cases");
    loadCharts("cases", "New Cases");
  })




  $("#nav-data").find("a").click(function () {
    var data = $(this).attr("id")
    var label = $(this).attr('aria-label')
    loadMap(data, label)
    loadCharts(data, label)
    console.log($(this).attr("id"))
    console.log($(this).attr('aria-label'))
  })



  //loading Script function
  function loadScript(url, callback) {
    var script = document.createElement("script");
    script.type = "text/javascript";
    if (script.readyState) {  //IE
      script.onreadystatechange = function () {
        if (script.readyState == "loaded" ||
          script.readyState == "complete") {
          script.onreadystatechange = null;
          callback();
        }
      };
    } else {  //Others
      script.onload = function () {
        callback();
      };
    }
    script.src = url;
    document.getElementsByTagName("head")[0].appendChild(script);
  }

  function loadMap(params, label) {
    var url = '/static/js/worldmap.js';
    loadScript(url, function () {
      var mapdata = Highcharts.maps['custom/world'];
      var data = [];

      $.getJSON('/tracker/map/', function (info) {
        // var params = 'cases'
        for (let index = 0; index < info.map_data.length; index++) {
          const element = info.map_data[index];
          if (element[params] > 0) {
            data[index] = {
              'id': element.code,
              'value': parseInt(element[params])
            };
          }

        }
        // console.log(data)

        $('#map').highcharts('Map', {
          title: {
            text: label + ' Global Map'
          },
          mapNavigation: {
            enabled: true,
            buttonOptions: {
              verticalAlign: 'bottom',
              align: 'right'
            }
          },
          colorAxis: {

            min: 1,
            type: 'logarithmic',
            minColor: '#FFFFFF',
            maxColor: '#800000',
            stops: [
              [0, '#FFFFFF'],
              [0.5, '#F08080'],
              [1, '#800000']
            ]
          },
          series: [{
            data: data,
            mapData: mapdata,
            joinBy: 'id',
            name: label,
            states: {
              hover: {
                color: '#a4edba'
              }
            },
            dataLabels: {
              enabled: false,
              format: '{point.name}'
            }
          }]
        });
      });
    })

  }


  var date = []
  var total_value = []
  var new_value = []
  var country = []
  var country_value = []
  function loadCharts(params, label) {

    // World & Country list Charts

    var total_chart = echarts.init(document.getElementById('total'));
    var new_chart = echarts.init(document.getElementById('new'));
    // var country_chart = echarts.init(document.getElementById('country_list'));



    $.getJSON('/tracker/location/', function (data) {

      $('#location').text(function (){
      return data.location.city + ','+ data.location.country
    })
      $('#location').click(function (){
        window.location.href = "/tracker/country/"+data.location.countryCode;
      })

      console.log(data)
      })

    $.getJSON('/tracker/json_data/', function (data) {

      // world data chart
      for (let index = 0; index < data.world_data.length; index++) {
        const element = data.world_data[index];
        date[index] = element.date;
        total_value[index] = element[params + '_per_million'];
        new_value[index] = element[params];

      }

      // country list
      for (let index = 0; index < data.country_data.length; index++) {
        const element = data.country_data[index];
        country[index] = element.country__country_name;
        country_value[index] = element[params];

      }
      console.log(country)


      total_chart.setOption({
        title: {
          text: label + ' per Million',
        },
        tooltip: {
          trigger: 'axis'
        },
        grid: {
          left: '15%'
        },
        xAxis: {
          type: 'category',
          data: date
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            name: label + '/M',
            type: 'line',
            smooth: true,
            data: total_value
          }]

      })
      new_chart.setOption({
        title: {
          text: label,
        },
        tooltip: {
          trigger: 'axis'
        },
        grid: {
          left: '15%'
        },
        xAxis: {
          type: 'category',
          data: date
        },
        yAxis: {
          type: 'value',
          axisLabel: {
            formatter: function (value, index) {
              if (value >= 1000 && value < 1000000) {
                value = value / 1000 + 'K';
              } else if (value >= 1000000) {
                value = value / 1000000 + 'M'
              } else {
                value = value;
              }
              return value
            }
          }
        },
        series: [
          {
            name: label,
            type: 'bar',
            data: new_value

          }]
      })

    })
    window.addEventListener("resize", function () {
      new_chart.resize();
      total_chart.resize();
    //   country_chart.resize();
    });

  }


  // View by Continent Tab

  $("#nav-continent-tab").click(function () {

    load_continent_charts($('#continent_select option:selected').val())
  });

  $('#continent_select').change(function () {
    load_continent_charts($(this).children('option:selected').val())

  })



  function load_continent_charts(params) {
    var myChart = echarts.init(document.getElementById('chart'));
    var lineChart = echarts.init(document.getElementById('continent_line_chart'));


    var continent = ['Africa', 'Asia', 'Europe', 'North America','Oceania', 'South America']
    var continent_value = []
    var pie_value =[]
    var value = { 'Africa': [], 'Asia': [], 'Europe': [], 'South America': [], 'North America': [], 'Oceania': [] }


    $.getJSON('/tracker/continent_data/', function (data) {
      console.log(data)

      for (let index = 0; index < data.data_line.length; index++) {
        const element = data.data_line[index];
        value[element['country__continent']].push(element[params])

      }

      for (let index = 0; index < data.data_pie.length; index++) {
        const element = data.data_pie[index];
        continent_value.push(element[params]);
        pie_value.push({
          'name':element.country__continent,
          'value':element[params]
        })

      }

      console.log(continent_value)



      myChart.setOption({
        title: {
          left: 'center'
        },

        legend: {
          orient: 'horizontal',
          left: 10,
          data: continent
        },
        series: [{
          name: 'Total Cases',
          type: 'pie',
          radius: '30%',
          center: ['50%', '50%'],
          label: {
            normal: {
              show: true,
              textStyle: {
                fontWeight: 600,
                fontSize: 14
              },
              formatter: '{d}%'
            }

          },
          data: pie_value
        }]
      })

      lineChart.setOption({
        title: {
        //   text: 'Line Chart'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: continent
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: date
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'Africa',
            type: 'line',
            data: value['Africa']
          },
          {
            name: 'Asia',
            type: 'line',
            data: value['Asia']
          },
          {
            name: 'Europe',
            type: 'line',
            data: value['Europe']
          },
          {
            name: 'North America',
            type: 'line',
            data: value['North America']
          },
          {
            name: 'Oceania',
            type: 'line',
            data: value['Oceania']
          },
          {
            name: 'South America',
            type: 'line',
            data: value['South America']
          }
        ]


      })


    });

    $(this).on('shown.bs.tab', function (e) {
      myChart.resize();
      lineChart.resize();

    });
    window.addEventListener("resize", function () {
      myChart.resize();
      lineChart.resize();

    });

  }




