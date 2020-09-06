
        $(document).ready(function(){
        var searchUrl = $('#search').attr('data-url');

        $.get(searchUrl, {'key': ''},  function(response) {
              $(".autocomplete").autocomplete({
              source: response.countryList
              });
            });
        })

        $("#search").keypress(function (even) {
          if (even.which == 13) {

            $.get('/tracker/search/',{'value': $(this).val()},function (data) {
              if (data.status == 'success') {
                window.location.href = '/tracker/country/'+data.value
              } else {
                alert('No results! Please try again')
              }
            })
          }
        });
