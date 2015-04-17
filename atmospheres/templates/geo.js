var app = angular.module('app', [])

.directive('mapViz', function() {
    var width = 600;
    var height = 400;

    return {
        restrict: 'E',
        link: function (scope, element, attrs) {
            var viz = d3.select('body')
                .append('div')
                .attr('id', 'map')
                .style('width', width + 'px')
                .style('height', height + 'px');

            var map = new google.maps.Map(viz.node(), {
                zoom: 12,
                center: new google.maps.LatLng(37.76487, -122.41948),
                mapTypeId: google.maps.MapTypeId.TERRAIN,
                min-zoom: 2
            });

            queue()
                .defer(d3.json, "static/sf_zips.topo.json")
                .await(ready);

            var svg, overlay;

            function ready(error, world) {
                var countries = topojson.feature(world, world.objects.geo).features,  
                    //land = topojson.feature(world, world.objects.land);

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
                        .attr('id','countries')
                        .selectAll('path')
                            .data(countries)
                          .enter().append('path')
                            .attr('class','country');
                    
                    overlay.draw = redraw;
                    google.maps.event.addListener(map, 'bounds_changed', redraw);
                    google.maps.event.addListener(map, 'center_changed', redraw);
                };
                overlay.setMap(map);
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
                
                svg.select('#countries').attr('transform', 
                    'scale('+width/(p1[0]-p2[0])+','+height/(p2[1]-p1[1])+')'+
                    'translate('+(-p2[0])+','+(-p1[1])+') ');
                          
                svg.selectAll('path').attr('d', path);
            }                               
        }
    };
});