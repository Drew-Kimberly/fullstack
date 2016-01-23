import webbrowser
import os
import re

# Styles and scripting for the page
main_page_head = '''
<head>
    <meta charset="utf-8">
    <title>Fresh Tomatoes!</title>

    <!-- Bootstrap 3 -->
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/css/bootstrap-theme.min.css">
    <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
    <script src="https://netdna.bootstrapcdn.com/bootstrap/3.1.0/js/bootstrap.min.js"></script>
    <style type="text/css" media="screen">
        body {
            padding-top: 80px;
        }
        #trailer .modal-dialog {
            margin-top: 200px;
            width: 640px;
            height: 480px;
        }
        .hanging-close {
            position: absolute;
            top: -12px;
            right: -12px;
            z-index: 9001;
        }
        #trailer-video {
            width: 100%;
            height: 100%;
        }
        .movie-tile {
            margin-bottom: 20px;
            padding-top: 20px;
        }
        .movie-tile:hover {
            background-color: #EEE;
            cursor: pointer;
        }
        .scale-media {
            padding-bottom: 56.25%;
            position: relative;
        }
        .scale-media iframe {
            border: none;
            height: 100%;
            position: absolute;
            width: 100%;
            left: 0;
            top: 0;
            background-color: white;
        }
        #toolbar {
            padding-bottom: 50px;
        }
        .requiredInput:after {
            content:" *";
        }
        .tooltip-inner {
            white-space:pre-wrap;
        }
        #durationAlert {
            padding-bottom: 5px;
            padding-top: 5px;
            margin-top: 8px;
            margin-bottom: 0px;
        }
    </style>
    <script type="text/javascript" charset="utf-8">

        // Filter movies by title using user search input
        // Reference: http://stackoverflow.com/questions/16829761/how-to-implement-search-functionality-in-javascript-for-phonegap
        $(document).ready(function () {
            $("#searchBox").keyup(function () {
                var userInput = $(this).val();
                $("#moviesDisplay div").map(function (index, value) {
                    $(value).toggle($(value).text().toLowerCase().indexOf(userInput) >= 0);
                });
            });
        });

        //Prevent postback from occurring if user hits enter key while search input in focus
        //Reference: http://stackoverflow.com/questions/21579724/how-to-prevent-postback-while-pressing-enter-key-from-inside-html-input-textbox
        $(document).ready(function () {
            $("#searchBox").keydown(function (event) {
                if (event.keyCode == 13) {
                    event.preventDefault();
                    return false;
                }
            });
        });

        //Display input error for duration if user-input is not an integer
        $(document).ready(function() {
            $('#inputDuration').keyup(function() {
                if (!isValidDurationInput()) {
                    $('#durationAlert').show();
                }
                else {
                    $('#durationAlert').hide();
                }
            });
        });

        //Disable 'Add Movie' button until required form fields are filled out
        //Reference: http://stackoverflow.com/questions/5614399/disabling-submit-button-until-all-fields-have-values
        $(document).ready(function () {
            $('.form-control').keyup(function() {
                if (isValidAddMovieForm()) {
                    $('#submitMovieBtn').removeAttr('disabled');
                }
                else {
                    $('#submitMovieBtn').attr('disabled', 'disabled');
                }
            });
        });

        //On submit of modal form, append new movie tile to existing container
        $(document).ready(function () {
            $('#submitMovieBtn').click(function () {
                var movieTileContent = createMovieTile($('#inputTitle').val(),
                                                       $('#inputDuration').val(),
                                                       $('#inputYear').val(),
                                                       $('#inputStoryline').val(),
                                                       $('#inputImage').val(),
                                                       $('#inputTrailer').val());
                $('#moviesDisplay').append(movieTileContent);

                //Re-initialize movie information tooltips
                $('[data-toggle="tooltip"]').tooltip();
             });
        });

        //Initialize movie information tooltips
        $(document).ready(function() {
            $('[data-toggle="tooltip"]').tooltip();
        });

        //Create new movie tile html
        function createMovieTile(title, duration, year, storyline, imageUrl, trailerUrl) {
            var movieTile = "";
            movieTile += "<div class='col-md-6 col-lg-4 movie-tile text-center' data-trailer-youtube-id='";
            movieTile += getTrailerId(trailerUrl);
            movieTile += "' data-toggle='modal' data-target='#trailer'>";
            movieTile += "<img src='" + imageUrl + "' data-toggle='tooltip' data-html='true' title='Year Released: " + year + "&lt;br&gt;Duration: " + formatDuration(duration) + "&lt;br&gt;&lt;br&gt;" + storyline + "' width='220' height='342'>";
            movieTile += "<h2>" + title + "</h2></div>";
            return movieTile;
        };

        //Grabs the YouTube trailer ID from a YouTube url
        //Reference: http://stackoverflow.com/questions/18268233/get-youtube-video-id-from-link-with-javascript
        function getTrailerId(trailerUrl) {
            var re = /^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
            return (trailerUrl.match(re)) ? RegExp.$1 : false;
        };

        //Formats duration in minutes to user-friendly view {hours}h {minutes}m
        //Makes one appreciate MVC for dynamic functionality as this function exists in model
        function formatDuration(duration) {
            var hours = Math.floor(duration / 60);
            var minutes = duration % 60;
            return String(hours + "h " + minutes + "m");
        };

        //Validates Duration input field - can only be an integer
        //Reference: http://stackoverflow.com/questions/2405880/jquery-validate-that-text-field-is-numeric
        function isValidDurationInput() {
            inputDuration = $('#inputDuration').val();
            if ((isNaN(inputDuration / 1) == true &&  inputDuration != "") || String(inputDuration).indexOf(".") != -1) {
                return false;
            }
            else {
                return true;
            }
        };

        //Validates if required add movie form fields are filled out
        function isValidAddMovieForm() {
            var isValid;
            var inputTitle = $('#inputTitle').val();
            var inputImage = $('#inputImage').val();
            var inputTrailer = $('#inputTrailer').val();

            isValid = (inputTitle !== "" && inputImage !== "" && inputTrailer !== "" && isValidDurationInput()) ? true : false;

            return isValid;
        };

        // Pause the video when the modal is closed
        $(document).on('click', '.hanging-close, .modal-backdrop, .modal', function (event) {
            // Remove the src so the player itself gets removed, as this is the only
            // reliable way to ensure the video stops playing in IE
            $("#trailer-video-container").empty();
        });
        // Start playing the video whenever the trailer modal is opened
        $(document).on('click', '.movie-tile', function (event) {
            var trailerYouTubeId = $(this).attr('data-trailer-youtube-id')
            var sourceUrl = 'http://www.youtube.com/embed/' + trailerYouTubeId + '?autoplay=1&html5=1';
            $("#trailer-video-container").empty().append($("<iframe></iframe>", {
              'id': 'trailer-video',
              'type': 'text-html',
              'src': sourceUrl,
              'frameborder': 0
            }));
        });
        // Animate in the movies when the page loads
        $(document).ready(function () {
          $('.movie-tile').hide().first().show("fast", function showNext() {
            $(this).next("div").show("fast", showNext);
          });
        });
    </script>
</head>
'''

# The main page layout and title bar
main_page_content = '''
<!DOCTYPE html>
<html lang="en">
  <body>
    <!-- Trailer Video Modal -->
    <div class="modal" id="trailer">
      <div class="modal-dialog">
        <div class="modal-content">
          <a href="#" class="hanging-close" data-dismiss="modal" aria-hidden="true">
            <img src="https://lh5.ggpht.com/v4-628SilF0HtHuHdu5EzxD7WRqOrrTIDi_MhEG6_qkNtUK5Wg7KPkofp_VJoF7RS2LhxwEFCO1ICHZlc-o_=s0#w=24&h=24"/>
          </a>
          <div class="scale-media" id="trailer-video-container">
          </div>
        </div>
      </div>
    </div>

    <!--Add New Movie Modal -->
    <!--Reference: http://getbootstrap.com/javascript/ -->
    <div class="modal fade" role="dialog" id="addMovieModal">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
             <button type="button" class="close" data-dismiss="modal" aria-label="Close">
               <span aria-hidden="true">&times;</span>
             </button>
             <h4 class="modal-title">Add New Movie</h4>
          </div>
          <div class="modal-body">
            <form class="form-horizontal" id="addMovieForm">
              <div class="form-group">
                <label for="inputTitle" class="col-sm-3 control-label requiredInput">Title</label>
                <div class="col-sm-9">
                  <input type="text" class="form-control" id="inputTitle" placeholder="Movie Title">
                </div>
              </div>
              <div class="form-group">
                <label for="inputDuration" class="col-sm-3 control-label">Duration</label>
                <div class="col-sm-9">
                  <input type="text" class="form-control" id="inputDuration" placeholder="Duration in Minutes (optional)">
                  <div id="durationAlert" class="alert alert-danger collapse" role="alert">Please enter an integer</div>
                </div>
              </div>
              <div class="form-group">
                <label for="inputYear" class="col-sm-3 control-label">Year</label>
                <div class="col-sm-9">
                  <input type="text" class="form-control" id="inputYear" placeholder="Year Released (optional)">
                </div>
              </div>
              <div class="form-group">
                <label for="inputStoryline" class="col-sm-3 control-label">Storyline</label>
                <div class="col-sm-9">
                  <input type="text" class="form-control" id="inputStoryline" placeholder="Storyline (optional)">
                </div>
              </div>
              <div class="form-group">
                <label for="inputImage" class="col-sm-3 control-label requiredInput">Image Url</label>
                <div class="col-sm-9">
                  <input type="text" class="form-control" id="inputImage" placeholder="Poster Image Url">
                </div>
              </div>
              <div class="form-group">
                <label for="inputTrailer" class="col-sm-3 control-label requiredInput">Trailer Url</label>
                <div class="col-sm-9">
                  <input type="text" class="form-control" id="inputTrailer" placeholder="Trailer Url">
                </div>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            <button type="submit" id="submitMovieBtn" class="btn btn-primary" data-dismiss="modal" disabled="disabled">Add Movie</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Main Page Content -->
    <div class="container">
      <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
        <div class="container">
          <div class="navbar-header">
            <a class="navbar-brand" href="#">Fresh Tomatoes Movie Trailers</a>
          </div>
        </div>
      </div>
    </div>
    <div class="container" id="toolbar">
      <ul class="nav navbar-nav navbar-right">
        <li>
          <button id="addMovieBtn" class="btn btn-primary navbar-btn" data-toggle="modal" data-target="#addMovieModal"><b>Add Movie</b></button>
        </li>
      </ul>
      <form class="navbar-form navbar-left" role="search">
        <div class="form-group has-feedback">
          <input type="text" class="form-control" id="searchBox" placeholder="Search" />
          <i class="glyphicon glyphicon-search form-control-feedback"></i>
        </div>
      </form>
    </div>
    <div class="container" id="moviesDisplay">
      {movie_tiles}
    </div>
  </body>
</html>
'''

# A single movie entry html template
movie_tile_content = '''
<div class="col-md-6 col-lg-4 movie-tile text-center" data-trailer-youtube-id="{trailer_youtube_id}" data-toggle="modal" data-target="#trailer">
    <img src="{poster_image_url}" data-toggle="tooltip" data-html="true" title="Year Released: {year_released}<br>Duration: {duration}<br><br>{storyline}" width="220" height="342">
    <h2>{movie_title}</h2>
</div>
'''

def create_movie_tiles_content(movies):
    # The HTML content for this section of the page
    content = ''
    for movie in movies:
        # Extract the youtube ID from the url
        youtube_id_match = re.search(r'(?<=v=)[^&#]+', movie.youtube_url)
        youtube_id_match = youtube_id_match or re.search(r'(?<=be/)[^&#]+', movie.youtube_url)
        trailer_youtube_id = youtube_id_match.group(0) if youtube_id_match else None

        # Append the tile for the movie with its content filled in
        content += movie_tile_content.format(
            movie_title=movie.title,
            poster_image_url=movie.poster_img_url,
            trailer_youtube_id=trailer_youtube_id,
            year_released=movie.year_released,
            duration=movie.format_duration(),
            storyline=movie.storyline
        )
    return content

def open_movies_page(movies):
  # Create or overwrite the output file
  output_file = open('fresh_tomatoes.html', 'w')

  # Replace the placeholder for the movie tiles with the actual dynamically generated content
  rendered_content = main_page_content.format(movie_tiles=create_movie_tiles_content(movies))

  # Output the file
  output_file.write(main_page_head + rendered_content)
  output_file.close()

  # open the output file in the browser
  url = os.path.abspath(output_file.name)
  webbrowser.open('file://' + url, new=2) # open in a new tab, if possible