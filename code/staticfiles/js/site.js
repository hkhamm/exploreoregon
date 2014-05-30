function prep_geological()
{
    map.markerLayer.setGeoJSON(geological_features);

    map.setView([43.98688630934305, -121.84661865234374], 8);
    $( "#locationlist li").removeClass("active", 0);
}

function prep_volunteer()
{

    map.markerLayer.setGeoJSON(volunteer_features);
    map.setView([43.98688630934305, -121.84661865234374], 8);
    $( "#volunteerlist li").removeClass("active", 0);
}

function great_circle_distance_in_mi(lat1,lon1,lat2,lon2) {
    var deg2rad = function(deg) { return deg * (Math.PI/180); }
    var R = 6371; // Radius of the earth in km
    var dLat = deg2rad(lat2-lat1);
    var dLon = deg2rad(lon2-lon1);
    var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) *
            Math.sin(dLon/2) * Math.sin(dLon/2);
    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    var d = R * c; // Distance in km
    return d*0.621371; // Distance in mi
}

function update_location(new_lat, new_lng) {
    // Returns the distance from the current location
    window.session_handle.location = [new_lat, new_lng];
    $('.distance').each(function(idx, el) {
        var $e = $(el);
        var target_lat = $e.attr("data-lat");
        var target_lng = $e.attr("data-lng");
        if (target_lat && target_lng) {
            var distance = great_circle_distance_in_mi(new_lat, new_lng, target_lat, target_lng);
            var rounded_distance = Math.round(distance);
            if (rounded_distance == 1) {
                $e.html(rounded_distance + " mile");
            } else {
                $e.html(rounded_distance + " miles");
            }

        }
    })


    if (window.map_markers) {
        for (var i in map_markers) {
            var marker = map_markers[i];
            var content = feature_tooltip_content(marker.feature)
            marker.bindPopup(content, {
                closeButton: true,
                minWidth: 320,
            });
        }
    }

}

function update_location_from_browser() {
    navigator.geolocation.getCurrentPosition(function(browser_location) {
        update_location(browser_location.coords.latitude, browser_location.coords.longitude)
    });
}

function display_form_errors(form_selector, errors)
{
    $(form_selector+' ul.errorlist').remove()
    for (var field_id in errors) {
        var errorstr = errors[field_id];
        if (errorstr) {
            $(errorstr).insertBefore(field_id)
        }
    }
    $(form_selector+' .success-message').hide();
}

function display_form_success(form_selector)
{
    $(form_selector+' ul.errorlist').remove()
    $(form_selector+' input[type=text]').val('');
    $(form_selector+' input[type=file]').val('');
    $(form_selector+' textarea').val('');
    $(form_selector+' .success-message').show();

    setTimeout(function() {
        $(form_selector+' .success-message').fadeOut();
    }, 15000)
}

function session_start()
{
    var soft_timeout_in_ms = MnchSettings.session_timeout_soft*60000;
    var hard_timeout_in_ms = MnchSettings.session_timeout_hard*60000;
    var tick_interval = 10000;
    window.session_handle = {
        'hard_max': hard_timeout_in_ms/tick_interval,
        'soft_max': soft_timeout_in_ms/tick_interval,
        'ticks': 0,
        'liked': {},
        'location': MnchSettings.default_location,
    }
    setInterval(session_tick, tick_interval);
}

function session_timeout_reset()
{
    if (!window.session_handle)
        return
    session_handle.ticks = 0;
}

function session_hard_timeout()
{
    window.location.reload();
}

function session_soft_timeout()
{
    if (!window.session_handle)
        return
    window.session_handle.liked = {};
    $( "#modal_container" ).removeClass( "active", 0 );
    $( "#locationlist li").removeClass("active", 0);
    map.setView([43.98688630934305, -121.84661865234374], 8);
}

function session_tick()
{
    window.session_handle.ticks += 1;
    if (window.session_handle.ticks >= session_handle.hard_max) {
        session_hard_timeout();
    }
    else
    if ((window.session_handle.ticks % session_handle.soft_max) == 0) {
        session_soft_timeout();
    }
}

function load_comments(site_pk, sort) {
    var sort = sort || 'all';
    var $comments = $('#modal_container .user_comments');
    $('a.sort-button').removeClass('active')
    $('a.sort-button#sort-comments-'+sort).addClass('active');
    $comments.load(MnchSettings.comments_url+'?site_id='+site_pk+'&sort='+sort, null, update_liked_comments)
}

function update_liked_comments() {
    for (var comment_pk in session_handle.liked) {
        var comment = $('aside.like a[data-pk="'+comment_pk+'"]');
        comment.html('You liked this tip').addClass("liked")
        setTimeout(function(){
            comment.html('Like').removeClass("liked");
        },5000);
    }
}

function close_popup() {
    // Close the modal and perform concomitant modifications.

    var pk = $("#modal_container").attr("class").match(/\w*-[\d*]/)[0].split("-")[1];
    // Remove all classes from modal. Remove 'active' first so that the modal doesn't break as it slides out
    $("#modal_container").removeClass("active").delay(200).queue(function(next){
        $("#modal_container").removeClass();
        // Remove any volunteer opportunity photos
        $('.volunteer-photo').remove();
        next();
    });
    // Pan the map to account for the modal disappearing and define type of location for scrolling the list
    var type;
    if ($("ul#locationlist").css('display') == "block") {
        // geological formations
        map.panBy([-675,0]);
        type = "geological";
    } else {
        // volunteer opportunities
        map.panBy([-500,0]);
        type = "volunteer";
    }
    // Show the nav
    $('nav').show();
    // Show the location and volunteer lists
    $('aside.listcontainer').show();
    enable_map_interactivity();
    scroll_to_location(pk, type, 0);
}

function disable_map_interactivity() {
    map.dragging.disable();
    map.touchZoom.disable();
    map.doubleClickZoom.disable();
    zoomControl.removeFrom(map)
    $('#reload').hide();
    // Add a transparent div in between the map and the modal; then prevent any click events through it.
    $('#modal_container').after("<div class='disable_interactivity' style='width:100%; position:absolute; top:0; bottom:0; z-index:199'></div>");
    $('.disable_interactivity').click(function(e) {
        e.stopPropagation();
        close_popup();
        // Open the cooresponding tooltip
        var pk = $("#modal_container").attr("class").match(/\w*-[\d*]/)[0].split("-")[1];
        var marker = map_markers[pk];
        marker.openPopup();
    });
}

function enable_map_interactivity() {
    map.dragging.enable();
    map.touchZoom.enable();
    map.doubleClickZoom.enable();
    if (!zoomControl._map)
        zoomControl.addTo(map)
    $('#reload').show();
    // Remove the transparent div to allow map click, drag, etc. events as normal.
    $('.disable_interactivity').remove();
}

function scroll_to_location(pk, type, time) {
    // Given the pk of a location, scrolls the location list such that the location item is centered vertically.
    if (type == "volunteer") {
        var $li = $('#volunteerlist li[data-pk="'+pk+'"]');
    } else {
        var $li = $('#locationlist li[data-pk="'+pk+'"]');
    }
    // Calculate the size and position of the li and scroll so it is in the center of the screen
    var eloffset = $li.offset().top;
    var elheight = $li.height();
    var wheight = $(window).height();
    // From the distance from the element to the top of the body,
    // subtract the distance between the top of the element and the top of the window.
    // This yields the position of the window with the element in the center, vertically.
    var scrollTo = eloffset - ((wheight/2) - (elheight/2));
    // Scroll the list
    if (typeof time === 'undefined') {
        var time = 1000;
    }
    $('html, body').animate({scrollTop:scrollTo}, time);
}

function open_tooltip(map, pinlatlng, pk, type) {
    // Position the screen such that the pin is centered between the li and the right side of the screen
    var screenlatlng = {};
    screenlatlng['lat'] = pinlatlng['lat'];
    screenlatlng['lng'] = pinlatlng['lng'] - .065;
    map.setView(screenlatlng, 11, {pan: {animate: true, duration: 1.5}, zoom: {animate: true}});
    scroll_to_location(pk, type);
    $(".listcontainer li").removeClass("active");
    $('li[data-pk="'+pk+'"]').addClass("active");
}

function select_volunteer_opportunity(volunteer_pk)
{
    if (!(volunteer_pk in window.volunteer_opportunities))
        return false
    var opp = window.volunteer_opportunities[volunteer_pk];
    $('#modal_container').removeClass("geological-site")
    $('#modal_container').addClass("volunteer-opportunity")

    $('#modal_container .content').html(opp.description);

    $('#modal_container .modal_header .title').html(opp.name);
    if (opp.resources.length > 0 && !MnchSettings.is_kiosk_display) {
        var $content = $('section#modal_container section.content');
        $content.append('<div class="resources-container"><h3>Resources</h3><ul class="resources"></ul></div>');
        var $resources = $('section#modal_container .resources-container ul.resources');
        for (var i=0; i < opp.resources.length; i++) {
            var r = opp.resources[i];
            $resources.append('<li><img class="favicon" src="'+r.favicon+'"/><a href="'+r.url+'" target="_blank">'+r.name+'</a></li>')
        }
    }

    if (opp.time) {
        $('#modal_container .venue .time').html(opp.time);
        $('#modal_container .venue .time-holder').show();
    } else {
        $('#modal_container .venue .time-holder').hide();
    }

    var d = new Date(opp.date)
    if (d) {
        $('#modal_container .venue .date').html(d.toDateString());
        $('#modal_container .venue .date-holder').show();
    } else {
        $('#modal_container .venue .date-holder').hide();
    }

    if (opp.price) {
        $('#modal_container .venue .price').html(opp.price);
        $('#modal_container .venue .price-holder').show();
    } else {
        $('#modal_container .venue .price-holder').hide();
    }

    $('#modal_container .venue .venue-name').html(opp.venue.name);

    if (opp.venue.address) {
        $('#modal_container .venue .address1').html(opp.venue.address + ", " + opp.venue.city+(opp.venue.state ? ", "+opp.venue.state : "") +" "+opp.venue.zipcode);
        $('#modal_container .venue .address-holder').show();
    } else {
        $('#modal_container .venue .address-holder').hide();

    }
    if (opp.photo) {
        $('#modal_container .modal_header .title').before('<img class="volunteer-photo" src="' + opp.photo + '"></img>');
    }

    open_modal("volunteer-" + volunteer_pk);
}

function select_geological_site(site_pk)
{
    if (!(site_pk in window.geological_sites))
        return false;
    var site = window.geological_sites[site_pk];

    $('#modal_container').addClass("geological-site");
    $('#modal_container').removeClass("volunteer-opportunity");

    $('#modal_container .modal_header .title').html(site.name);
    $('#modal_container .content').html(site.description);

    $('#modal_container form.add_photo #photo_site_id').val(site.id);
    $('#modal_container form.add_comment #comment_site_id').val(site.id);
    if (site.resources.length > 0 && !MnchSettings.is_kiosk_display) {
        var $content = $('section#modal_container section.content');
        $content.append('<div class="resources-container"><h3>Resources</h3><ul class="resources"></ul></div>');
        var $resources = $('section#modal_container .resources-container ul.resources');
        for (var i=0; i < site.resources.length; i++) {
            var r = site.resources[i];
            $resources.append('<li><img class="favicon" src="'+r.favicon+'"/><a href="'+r.url+'" target="_blank">'+r.name+'</a></li>')
        }
    }

    var $slides = $('#modal_container .slides');
    var $tabs = $('#modal_container .tabs');
    $slides.empty();
    $tabs.empty();
    for (var i=0; i < site.photos.length; i++) {
        var p = site.photos[i];
        if (p.credits) {
            $slides.append($('<div class="slide"><img src="'+p.photo+'" alt="#" /><p>Credit: ' + p.credits + '</p></div>'));
        } else {
            $slides.append($('<div class="slide"><img src="'+p.photo+'" alt="#" /></div>'));
        }
        $tabs.append('<li><a href="#"></a></li>');
    }
    $("#modal_container ul.tabs").tabs("div.slides > div.slide", {
        effect: 'fade',
        fadeOutSpeed: "slow",
        rotate: true
    });

    $('#sort-comments-best').off().on('click', function() {
        load_comments(site_pk, 'best')
    })
    $('#sort-comments-all').off().on('click', function() {
        load_comments(site_pk, 'all')
    })
    load_comments(site_pk, 'best');

    if (MnchSettings.is_kiosk_display) {
        $('#modal_container .content a').each(function(idx,el) {
            $(el).replaceWith( $('<span class="replaced-a"></span>').html($(el).html()) );
        })

        $('#modal_container .content-sidebar').hide();
        $('#modal_container .resources-container').hide();

        if (MnchSettings.allow_kiosk_commenting) {
            $('#modal_container .add_comment_open').show();
        } else {
            $('#modal_container .add_comment_open').hide();
        }
    } else {
        $('#modal_container .content-sidebar').show();
        $('#modal_container .add_comment_open').show();
        $('#modal_container .resources-container').show();
    }

    open_modal("geological-" + site_pk);
}

function open_modal(type_pk)
{
    $('#modal_container').addClass(type_pk);
    $("form.add_comment").slideUp();
    $('#modal_container article').animate({scrollTop: 0}, 200);
    $("form .success-message").hide();
    // Hide the nav
    $('nav').hide();
    // Hide the location and volunteer lists
    $('aside.listcontainer').hide();
}

function open_geological_modal(pk) {

    // If the modal is already open, close_popup (and modal)
    if ( $("#modal_container").hasClass("active") ) {
        close_popup();
        return false;
    }
    // Show the modal
    $( "#modal_container" ).addClass( "active", 2000 );
    $('nav').hide();
    select_geological_site(pk);
    map.panBy([675,0]);
    map_markers[pk].closePopup();
    disable_map_interactivity();
    return false;
}

function open_volunteer_modal(pk) {

    // If the modal is already open, close_popup (and modal)
    if ( $("#modal_container").hasClass("active") ) {
        close_popup();
        return false;
    }
    // Show the modal
    $( "#modal_container" ).addClass( "active", 2000 );
    $('nav').hide();
    select_volunteer_opportunity(pk);
    map.panBy([500,0]);
    map_markers[pk].closePopup();
    disable_map_interactivity();
    return false;
}

function feature_tooltip_content(feature)
{
    var content = '<div class="map-popup">';
    // For geological sites, which have multiple photos
    if (feature.properties.photos && feature.properties.photos.length > 0) {
        content += '<img class="oneup" src="'+feature.properties.photos[0].url+'" onclick="open_geological_modal('+feature.properties.pk+');"/>';
    }
    // For volunteer opportunities, which have an optional photo
    if (feature.properties.photo) {
        content += '<img class="oneup" src="'+feature.properties.photo+'" onclick="open_volunteer_modal('+feature.properties.pk+');"/>';
    }
    if (feature.properties.type == "geological") {
        content += '<div class="name ' + feature.properties.type + '" onclick="open_geological_modal('+feature.properties.pk+');">'+feature.properties.title+'</div>';
    } else if (feature.properties.type == "volunteer") {
        content += '<div class="name ' + feature.properties.type + '" onclick="open_volunteer_modal('+feature.properties.pk+');">'+feature.properties.title+'</div>';
    } else {
        content += '<div class="name">'+feature.properties.title+'</div>';
    }

    var dist = great_circle_distance_in_mi(window.session_handle.location[0], window.session_handle.location[1],
                                feature.geometry.coordinates[1], feature.geometry.coordinates[0]);
    var dist = Math.round(dist);
    var dist_units = "miles";
    if (dist == 1) {
        dist_units = "mile";
    }

    content += '<p>'

    if ('venue' in feature.properties) {
        content += '<span class="venue">'+feature.properties.venue+'</span> '
    }

    content += '(<span class="distance" data-lat="'+feature.geometry.coordinates[1]+'" data-lng="'+feature.geometry.coordinates[0]+'">'+dist+'</span> ' + dist_units + ' away)';

    content += '</p>';


    content += '</div>';
    return content;
}
