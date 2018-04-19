
$(function (){
    var $planets = $('#planets');
    var $pagecount = 1;
    loadPage();

    function residentHandler(resident) {
        if (resident.length === 0) {
            return 'No known resident'
        } else {
            return '<button type="button" class="btn btn-secondary residentbutton" data-residents="' + resident + '" >' + resident.length + ' resident(s)</button>'
        }
    }

    function loadPage() {
        $planets.html('');
        $.ajax({
            type: 'GET',
            url: 'https://swapi.co/api/planets/?page=' + $pagecount,
            success: function(data) {
                $.each(data.results , function(i, planet) {
                    $planets.append('<tr><td>' + planet.name +
                                    '</td><td>' + planet.diameter +
                                    '</td><td>' + planet.climate +
                                    '</td><td>' + planet.terrain +
                                    '</td><td>' + planet.surface_water + "%" +
                                    '</td><td>' + planet.population +
                                    '</td><td>' + residentHandler(planet.residents) +
                                    '</td></tr>');
                });
                $('.residentbutton').click(function() {
                    openResidentModal(this);
                })
            },
            error: function(){
                alert('error loading planets');
            }
        });
    }

    function openResidentModal(residentButton) {
        let data = $(residentButton).attr('data-residents');
        let linkArray = data.split(",")
        $('#modaltable').html("");

        $.each(linkArray, function(i, link) {
            $.ajax({
                type: 'GET',
                url: link,
                success: function(data) {
                    $('#modaltable').append('<tr><td>' + data.name +
                                            '</td><td>' + data.height +
                                            '</td><td>' + data.mass +
                                            '</td><td>' + data.hair_color +
                                            '</td><td>' + data.skin_color +
                                            '</td><td>' + data.eye_color +
                                            '</td><td>' + data.birth_year +
                                            '</td><td>' + data.gender +
                                            '</td><tr>');
                },
                error: function() {
                    alert('Error, loading data!')
                }
            });
        });
        $("#residentmodal").modal("show");
    }

    $("#next, #previous").click(function() {
        $pagecount = ($(this).attr('id')=='next') ? $pagecount + 1 : $pagecount - 1;
        if ($pagecount === 0) {
            $pagecount = 1;
        } else if ($pagecount === 8){
            $pagecount = 7;
        } else {
            loadPage();
        }
    });
});