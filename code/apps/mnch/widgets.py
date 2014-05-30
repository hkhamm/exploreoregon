from django import forms
from sky_settings.models import Setting

from django.utils.safestring import mark_safe

class MapboxWidget(forms.HiddenInput):
    class Media:
        css = {
            'all': ('http://api.tiles.mapbox.com/mapbox.js/v1.3.1/mapbox.css',),
        }
        js = ('js/mapbox-1.3.1.js',)

    def render(self, name, value, attrs=None):
        context = {
            'mapbox_api_key': Setting.get_value('mapbox_api_key'),
            'name': name,
            'value': value,
        }
        html = """<section class="mapbox_widget" id="id_%(name)s"></section>
        <style>
        .mapbox_widget {
            width: 600px;
            height: 400px;
        }
        </style>
        <script>

        (function($) {

            $(function() {

                var map = L.mapbox.map('id_%(name)s', '%(mapbox_api_key)s');
                var geocoder = L.mapbox.geocoderControl('%(mapbox_api_key)s')
                map.addControl(geocoder);
                map.scrollWheelZoom.disable();

                var layer = L.mapbox.tileLayer('%(mapbox_api_key)s');
                var marker = L.marker([0,0], {
                    icon: L.mapbox.marker.icon({
                        'type': "Feature", 
                        'geometry': {
                            'type': "Point",
                        },
                    }),
                    draggable: true
                });

                layer.on('ready', function(e) {
                    var tj = layer.getTileJSON();

                    var $latitude = $('#id_latitude');
                    var $longitude = $('#id_longitude');
                    var latlng = null;

                    if ($latitude.val() && $longitude.val()) {
                        latlng = [Number($latitude.val()), Number($longitude.val())];
                        marker.setLatLng(latlng);
                    }
                    else {
                        latlng = [tj.center[1], tj.center[0]]
                        marker.setLatLng(latlng);
                        $latitude.val(tj.center[1]);
                        $longitude.val(tj.center[0]);
                    }
                    marker.addTo(map);

                    if (latlng) 
                        map.setView(latlng, 9);

                    var update_marker = function() {
                        var ll = [Number($latitude.val()), Number($longitude.val())]
                        marker.setLatLng(ll);
                    };
                    $latitude.change(update_marker);
                    $longitude.change(update_marker);
                });

                marker.on('dragend', function(e) {
                    $('#id_latitude').val(marker._latlng.lat)
                    $('#id_longitude').val(marker._latlng.lng)
                });

                geocoder.on('found', function(e) {
                    $('#id_latitude').val(e.latlng[0])
                    $('#id_longitude').val(e.latlng[1]);
                    marker.setLatLng(e.latlng)

                });


            })

        })(jQuery);

        </script>

        """ % context;
        return mark_safe(html);