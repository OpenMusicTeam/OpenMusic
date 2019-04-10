var playlist = WaveformPlaylist.init({
  samplesPerPixel: 3000,
  waveHeight: 100,
  mono: true,
  container: document.getElementById("playlist"),
  state: 'cursor',
  colors: {
    waveOutlineColor: '#E0EFF1',
    timeColor: 'grey',
    fadeColor: 'black'
  },
  timescale: true,
  controls: {
    show: true, //whether or not to include the track controls
    width: 200 //width of controls in pixels
  },
  seekStyle : 'line',
  zoomLevels: [250,500, 1000, 3000, 5000]
});

/*playlist.load([
  {
    //"src": "media/audio/Vocals30.mp3",
    "src": "../../../../../static/project_manager/media/audio/Vocals30.mp3",
    "name": "Vocals",
    "fadeIn": {
      "duration": 0.5
    },
    "fadeOut": {
      "duration": 0.5
    },
    "cuein": 5.918,
    "cueout": 14.5,
    "customClass": "vocals",
    "waveOutlineColor": '#c0dce0'
  },
  {
    //"src": "media/audio/BassDrums30.mp3",
    "src": "../../../../../static/project_manager/media/audio/BassDrums30.mp3",
    "name": "Drums",
    "start": 8.5,
    "fadeIn": {
      "shape": "logarithmic",
      "duration": 0.5
    },
    "fadeOut": {
      "shape": "logarithmic",
      "duration": 0.5
    }
  },
  {
    //"src": "media/audio/Guitar30.mp3",
    "src": "../../../../../static/project_manager/media/audio/Guitar30.mp3",
    "name": "Guitar",
    "start": 23.5,
    "fadeOut": {
      "shape": "linear",
      "duration": 0.5
    },
    "cuein": 15
  }
]).then(function() {
  //can do stuff with the playlist.

  //initialize the WAV exporter.
  playlist.initExporter();
});*/

var audio_paths = document.getElementById("myVar").value;
audio_paths = audio_paths.split('\'').join('\"');
//alert(audio_paths);
audio_paths = JSON.parse(audio_paths);
for (var song_name in audio_paths) {
  var song_path = audio_paths[song_name];
  song_path = '../../../../../' + song_path;
  //alert("song_name = " + song_name);
  //alert("song_path = " + song_path);
  playlist.load([
    {
      "src": song_path,
      "name": song_name,
      "customClass": "vocals"
    }
  ])
  .then(function() {
    //can do stuff with the playlist.
  
    //initialize the WAV exporter.
    playlist.initExporter();
  });
}







