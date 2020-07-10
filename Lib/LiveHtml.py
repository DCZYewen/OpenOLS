#http://10.0.10.51:8080/live/jiangxu.flv?user_id=99999998&token=2f49ccee30a915239cfb7942062f347f
html = ['''<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta http-equiv="x-ua-compatible" content="IE=edge" >
<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no"/>
<title>Aliplayer Online Settings</title>
<link rel="stylesheet" href="https://g.alicdn.com/de/prismplayer/2.8.8/skins/default/aliplayer-min.css" />
<script type="text/javascript" charset="utf-8" src="https://g.alicdn.com/de/prismplayer/2.8.8/aliplayer-min.js"></script>
</head>
<body>
<div class="prism-player" id="player-con"></div>
<script>
var player = new Aliplayer({
  "id": "player-con",
  "source": "''' , '''",
  "width": "100%",
  "height": "500px",
  "autoplay": true,
  "isLive": true,
  "rePlay": false,
  "playsinline": true,
  "preload": true,
  "enableStashBufferForFlv": true,
  "stashInitialSizeForFlv": 32,
  "controlBarVisibility": "hover",
  "useH5Prism": true
}, function (player) {
    console.log("The player is created");
  }
);
</script>
</body>''']