$(document).ready(function(){
        var searchUrl = $('#search').attr('data-url');

        $.get(searchUrl, {'key': ''},  function(response) {
              $(".autocomplete").autocomplete({
              source: response.countryList
              });
            });
        })


        $('#searchButton').click(function (){
            $.get('/tracker/search/',{'value': $("#search").val()},function (data) {
              if (data.status == 'success') {
                window.location.href = '/tracker/mobile/country/'+data.value
              } else {
                alert('No results! Please try again')
              }
            })
        })