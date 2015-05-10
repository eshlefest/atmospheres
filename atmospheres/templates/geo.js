var app = angular.module('app', ['ngRoute']);


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
    $scope.getData = function(URL,embed_graph) {
        $http.get(URL).success(function(data) {
            embed_graph(data)

        })
        return false;
    }
}]);

// the following code was shamelessly lifted from:
// http://leafletjs.com/examples/choropleth.html

app.directive('map', function() {
    var linker = function (scope, element, attrs) {




L.control.Button = L.Control.extend({
  options: {
    position: 'topleft'
  },
  initialize: function (options) {
    this._button = {};
    this.setButton(options);
  },
 
  onAdd: function (map) {
    this._map = map;
    var container = L.DomUtil.create('div', 'info leaflet-control-button');
    
    this._container = container;
    
    this._update();
    return this._container;
  },
 
  onRemove: function (map) {
  },
 
  setButton: function (options) {
    var button = {
      'text': options.text,                 //string
      'iconUrl': options.iconUrl,           //string
      'onClick': options.onClick,           //callback function
      'hideText': !!options.hideText,         //forced bool
      'maxWidth': options.maxWidth || 70,     //number
      'doToggle': options.toggle,           //bool
      'toggleStatus': false                 //bool
    };
 
    this._button = button;
    this._update();
  },
  
  getText: function () {
    return this._button.text;
  },
  
  getIconUrl: function () {
    return this._button.iconUrl;
  },
  
  destroy: function () {
    this._button = {};
    this._update();
  },
  
  toggle: function (e) {
    if(typeof e === 'boolean'){
        this._button.toggleStatus = e;
    }
    else{
        this._button.toggleStatus = !this._button.toggleStatus;
    }
    this._update();
  },
  
  _update: function () {
    if (!this._map) {
      return;
    }
 
    this._container.innerHTML = '';
    this._makeButton(this._button);
 
  },
 
  _makeButton: function (button) {
    var newButton = L.DomUtil.create('div', 'leaflet-buttons-control-button', this._container);
    if(button.toggleStatus)
        L.DomUtil.addClass(newButton,'leaflet-buttons-control-toggleon');
        
    var image = L.DomUtil.create('img', 'leaflet-buttons-control-img', newButton);
    image.setAttribute('src',button.iconUrl);
    
    if(button.text !== ''){
 
      L.DomUtil.create('br','',newButton);  //there must be a better way
 
      var span = L.DomUtil.create('span', 'leaflet-buttons-control-text', newButton);
      var text = document.createTextNode(button.text);  //is there an L.DomUtil for this?
      span.appendChild(text);
      if(button.hideText)
        L.DomUtil.addClass(span,'leaflet-buttons-control-text-hide');
    }
 
    L.DomEvent
      .addListener(newButton, 'click', L.DomEvent.stop)
      .addListener(newButton, 'click', button.onClick,this)
      .addListener(newButton, 'click', this._clicked,this);
    L.DomEvent.disableClickPropagation(newButton);
    return newButton;
 
  },
  
  _clicked: function () {  //'this' refers to button
    if(this._button.doToggle){
        if(this._button.toggleStatus) { //currently true, remove class
            L.DomUtil.removeClass(this._container.childNodes[0],'leaflet-buttons-control-toggleon');
        }
        else{
            L.DomUtil.addClass(this._container.childNodes[0],'leaflet-buttons-control-toggleon');
        }
        this.toggle();
    }
    return;
  }
 
});





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
                    html = '<h4>'+e.target.feature.id+', Sentiment</h4>' +
                        e.target.feature.sentiment + '</br>' +'<a id="shrink-button" href="#">shrink</a>'+
                        '<iframe id="graph-frame" width="320" height="240" frameborder="0" seamless="seamless" scrolling="no" src='+scope.getData(url)+'></iframe>';
                
                    this.setHTML(html)
                }
                else
                    this._div.innerHTML = '<h4>Zipcode, Sentiment</h4>' 
            };

            info.setHTML = function(html){
                this._div.innerHTML = html;

            }

            info.embedGraph = function(graph_url){
                html = '<a id="shrink-button" href="#">shrink</a>'+
                        '<iframe id="graph-frame" width="320" height="240" frameborder="0" seamless="seamless" scrolling="no" src='+graph_url+'></iframe>';
                
                    info.setHTML(html)
                    growFrame()
            }

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
            
            var barGraphClicked = function(){
                growFrame();

                var url = "/data/sf/bar";
                scope.getData(url, info.embedGraph);
                
            }

              var growFrame = function(){
                
                    $( "#graph-frame" ).animate({
                    height: "500",
                    width: "900"
                    }, 1000, function() {
                    // Animation complete.
                });

                    $( "#shrink-button" ).click(shrinkFrame)
            }

            var shrinkFrame = function(){
                
                    $( "#graph-frame" ).animate({
                    height: "320",
                    width: "240"
                    }, 1000, function() {
                    // Animation complete.
                })}


            var myButtonOptions = {
                'text': 'Bar Graph',  // string
                'iconUrl': 'http://simpleicon.com/wp-content/uploads/bar-chart-down-64x64.png',  // string
                'onClick': barGraphClicked,  // callback function
                'hideText': true,  // bool
                'maxWidth': 30,  // number
                'doToggle': false,  // bool
                'toggleStatus': false  // bool
                }   

                var myButton = new L.control.Button(myButtonOptions).addTo(map);


            geojson = L.geoJson(data,{style: style,onEachFeature: onEachFeature}).addTo(map);
            
            drawArrows(data,map)
            

            
        }

        function drawArrows(data,map)
        {
            var LeafIcon = L.Icon.extend({
            options: {
                iconSize:     [20, 20],
                shadowSize:   [50, 64],
                iconAnchor:   [0, 0],
                shadowAnchor: [4, 62],
                popupAnchor:  [-3, -76]
            }
        });

        var greenIcon = new LeafIcon({iconUrl: 'http://png-2.findicons.com/files/icons/42/basic/64/up.png'}),
            redIcon = new LeafIcon({iconUrl: 'http://iconbug.com/data/9c/48/ec0ddc3c64be1bbbc5340ff91bd7dff2.png'});

            var icon;
            features = data.features;
            for(var i = 0; i<features.length; i++)
            {
                if(features[i].trend == "up")
                    icon = greenIcon;
                else
                    icon = redIcon;
                
                var point =  features[i].point
                point = [parseFloat(point[1]),parseFloat(point[0])];
                L.marker(point,{icon:icon}).addTo(map);

            }

        }


        function getColor(d) {

            return  d > .7 ? '#CC0066' :
                    d > .5  ? '#FF0066' :
                    d > .3  ? '#FF6699' :
                    d > 0  ? '#FFCCCC' :
                    d > -.3   ? '#66FFFF' :
                    d > -.5   ? '#6699FF' :
                    d > -.7   ? '#3366FF' :
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
            scope.getData(url, info.embedGraph);
            


            
        }   
    
    };

    return {
        restrict: 'E',
        template: "<div id=\"map\"></div>",
        link: linker
    };


});




