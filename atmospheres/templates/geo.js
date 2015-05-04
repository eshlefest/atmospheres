var app = angular.module('app', ['ngRoute']);

// app.directive('mapViz', function() {
//      return {
//          restrict: 'E',
//          template: "<p>Hello World</p>"
//      };
// });

 app.directive('mapViz', function() {

    return {
        restrict: 'E',
        link: function (scope, element, attrs) {
var width = 600,
    height = 400,
    div = d3.select('body')
        .insert('div', 'footer')
        .attr('id','map')
        .style('width', width + 'px')
        .style('height', height + 'px')
        .style('margin-left', 'auto')
        .style('margin-right', 'auto');

// Create the Google Map…
var map = new google.maps.Map(div.node(), {
  zoom: 12,
  center: new google.maps.LatLng(37.76487, -122.41948),
  mapTypeId: google.maps.MapTypeId.TERRAIN,
  minZoom: 2  // stuff goes wrong if we allow world wraparound
});



// Load the  data. When the data comes back, create an overlay.
queue()
    .defer(d3.json, "{{ url_for('static', filename='sf_zips.topo.json') }}")
    .await(ready)

var svg, overlay;

function ready(error, world) {
    var zipcodes = topojson.feature(world, world.objects.geo).features,
        // land = topojson.feature(world, world.objects.land);

    overlay = new google.maps.OverlayView();
    overlay.onAdd = function() {
        // create an SVG over top of it.
        svg = d3.select(overlay.getPanes().overlayLayer)
            .append('div')
                .attr('id','d3map')
                .style('width', width + 'px')
                .style('height', height + 'px')
            .append('svg')
                .attr('width', width)
                .attr('height', height);

        svg.append('g')
            .attr('id','zipcodes')
            .selectAll('path')
                .data(zipcodes)
              .enter().append('path')
                .attr('class','zipcode')
                .attr("id",function(d){return "zip_"+d.id})

        overlay.draw = redraw;
        google.maps.event.addListener(map, 'bounds_changed', redraw);
        google.maps.event.addListener(map, 'center_changed', redraw);
    };
    overlay.setMap(map);

    //this is a hack!
    setTimeout(updateColors, 1000)
}

function updateColors()
{
    d3.select("#zip_94105")
        .style('fill', 'red');

    d3.select("#zip_94111")
        .style('fill', 'aquamarine');

    d3.select("#zip_94132")
        .style('fill', 'purple');
}

function redraw() {

    var bounds = map.getBounds(),
        ne = bounds.getNorthEast(),
        sw = bounds.getSouthWest(),
        projection = d3.geo.mercator()
            .rotate([-bounds.getCenter().lng(),0])
            .translate([0,0])
            //.center([0,0])
            .scale(1),
        path = d3.geo.path()
            .projection(projection);

    var p1 = projection([ne.lng(),ne.lat()]),
        p2 = projection([sw.lng(),sw.lat()]);

    svg.select('#zipcodes').attr('transform',
        'scale('+width/(p1[0]-p2[0])+','+height/(p2[1]-p1[1])+')'+
        'translate('+(-p2[0])+','+(-p1[1])+') ');

    svg.selectAll('path').attr('d', path);
    }
        }
    };
});

app.config(function($routeProvider) {
    $routeProvider
        .when('/', {
            templateUrl: 'geo_new.html',
            controller: 'MapController'
        })
        .when('/about', {
            templateUrl: 'about.html'
        })
        .otherwise({
            redirectTo: '/'
        });
});

/**
 * controller to make a ajax call to a URL
 */

app.controller('MapController', ['$scope', '$http', function($scope, $http) {
    $scope.data = '';
    $scope.getData = function(URL) {
        $http.get(URL).success(function(data) {
            $scope.data = data;
        })
        return $scope.data;
    }
}]);

// the following code was shamelessly lifted from:
// http://leafletjs.com/examples/choropleth.html

app.directive('map', function() {
    var linker = function (scope, element, attrs) {
        var geojson;
        var info;
        

        var zip_data = $.getJSON("data/live", function(data){on_json_received(data)})


        function on_json_received(data){
            L.mapbox.accessToken = 'pk.eyJ1IjoicnlhbmVzaGxlbWFuIiwiYSI6IjNjV2FjaHcifQ.OnIpYYJr64Vnl4Y_buDzNw';
            var map = L.mapbox.map('map', 'ryaneshleman.lonika6m')
            .setView([37.760, -122.435], 13);
            info = L.control();
            

            info.onAdd = function (map) {
                this._div = L.DomUtil.create('div', 'info'); // create a div with a class "info"
                this.update();
                return this._div;
            };

            // method that we will use to update the control based on feature properties passed
            info.update = function (e) {
                if(e) {
                    var zipcode = e.target.feature.id;
                    var url = "/data/zipcode/"+zipcode;
                    this._div.innerHTML = '<h4>'+e.target.feature.id+', Sentiment</h4>' +
                        e.target.feature.sentiment + '</br>' +
                        '<iframe width="320" height="240" frameborder="0" seamless="seamless" scrolling="no" src='+scope.getData(url)+'></iframe>';
                }
                else
                    this._div.innerHTML = '<h4>Zipcode, Sentiment</h4>' 
            };

            info.addTo(map);

            var legend = L.control({position: 'bottomright'});

            legend.onAdd = function (map) {

                var div = L.DomUtil.create('div', 'info legend'),
                    grades = [-1,-.7, -.5, -.3, 0, .3, .5, .7,1],
                    labels = [];

                // loop through our density intervals and generate a label with a colored square for each interval
                for (var i = 0; i < grades.length; i++) {
                    div.innerHTML +=
                        '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
                        grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+</br>');
                }

                return div;
            };

            legend.addTo(map);



            geojson = L.geoJson(data,{style: style,onEachFeature: onEachFeature}).addTo(map);
            
            
        }

        function getColor(d) {

            return  d > .7 ? '#800026' :
                    d > .5  ? '#BD0026' :
                    d > .3  ? '#E31A1C' :
                    d > 0  ? '#FC4E2A' :
                    d > -.3   ? '#FD8D3C' :
                    d > -.5   ? '#FEB24C' :
                    d > -.7   ? '#FED976' :
                               '#FFEDA0';
        }

        function style(feature) {
            return {
                fillColor: getColor(feature.sentiment),
                weight: 2,
                opacity: 1,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.7
                };
        }
        function highlightFeature(e) {
            var layer = e.target;

            layer.setStyle({
            weight: 5,
            color: '#666',
            dashArray: '',
            fillOpacity: 0.7
        });

        if (!L.Browser.ie && !L.Browser.opera) {
            layer.bringToFront();
            }
        info.update(e);
        }

        function resetHighlight(e) {
            geojson.resetStyle(e.target);
        }

        function onEachFeature(feature, layer) {
            layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight,
            click: regionClicked
            });

            info.update();
        }

        function regionClicked(e)
        {
            var zipcode = e.target.feature.id;
            var url = "/data/zipcode/"+zipcode;
            return scope.getData(url);
        }   
    
    };

    return {
        restrict: 'E',
        template: "<div id=\"map\"></div>",
        link: linker
    };
});







