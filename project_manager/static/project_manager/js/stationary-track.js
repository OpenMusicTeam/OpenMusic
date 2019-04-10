var playlist = WaveformPlaylist.init({
  samplesPerPixel: 3000,
  zoomLevels: [500, 1000, 3000, 5000],
  mono: true,
  waveHeight: 100,
  container: document.getElementById("playlist"),
  state: 'shift',
  waveOutlineColor: '#E0EFF1',
  colors: {
      waveOutlineColor: '#E0EFF1',
      timeColor: 'grey',
      fadeColor: 'black'
  },
  controls: {
    show: true, //whether or not to include the track controls
    width: 200 //width of controls in pixels
  }
});

/*playlist.load([
  {
    //"src": "media/audio/Vocals30.mp3",
    //"src": "../../../../../static/project_manager/media/audio/Vocals30.mp3", 
    //"src":"../../../../../../user_projects/psm2001/Third project/gtr-nylon22.mp3",
    //"src": "D:/OpenMusicOfficial/OpenMusic_current/user_projects/psm2001/Third project/gtr-nylon22.mp3",
    //"src": "../../../../../user_projects/psm2001/Third project/gtr-nylon22.mp3",
    "src": "../../../../../static/user_projects/psm2001/alien.mp3",
    //"src": "<% = Url.Content('~/user_projects/psm2001/Third project/gtr-nylon22.mp3') %>",
    "name": "Vocals",
    "states": {
      "shift": false
    }
  },
  {
    //"src": "media/audio/BassDrums30.mp3",
    "src": "../../../../../static/project_manager/media/audio/BassDrums30.mp3", 
    "name": "Drums",
    "start": 30
  }
]).then(function() {
  //can do stuff with the playlist.
});*/


/*playlist.load([
  {
    "src": "../../../../../static/user_projects/psm2001/alien.mp3",
  }
]);
playlist.load([
  {
    "src": "../../../../../static/project_manager/media/audio/BassDrums30.mp3", 
  }
]);*/

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
    }
  ]);
}