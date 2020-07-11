#http://10.0.10.51:8080/live/jiangxu.flv?user_id=99999998&token=2f49ccee30a915239cfb7942062f347f
html = ['''<!DOCTYPE HTML>
<html>
    <head>
		<head>    
		<meta charset="UTF-8">
		<title>Bootstrap引入</title>
	
    <!-- 新 Bootstrap4 核心 CSS 文件 -->
    <link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/4.3.1/css/bootstrap.min.css">
    
    <!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
    <script src="https://cdn.staticfile.org/jquery/3.2.1/jquery.min.js"></script>
    
    <!-- bootstrap.bundle.min.js 用于弹窗、提示、下拉菜单，包含了 popper.min.js -->
    <script src="https://cdn.staticfile.org/popper.js/1.15.0/umd/popper.min.js"></script>
    
    <!-- 最新的 Bootstrap4 核心 JavaScript 文件 -->
    <script src="https://cdn.staticfile.org/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>
		
		<meta http-equiv="x-ua-compatible" content="IE=edge" >
		<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no"/>
		<link rel="stylesheet" href="https://g.alicdn.com/de/prismplayer/2.8.8/skins/default/aliplayer-min.css" />
		<script type="text/javascript" charset="utf-8" src="https://g.alicdn.com/de/prismplayer/2.8.8/aliplayer-min.js"></script>
		
		</head>
    </head>
    <body>
<div class="container-fluid">
	<div class="row">
		<div class="col-md-12">
			<div class="row">
				<div class="col-md-11">
					<h2>测试直播间</h2>
				</div>
				<div class="col-md-1">
					<button type="button" class="btn btn-success" onclick="gotoMain();">
						返回主页
					</button>
				</div>
			</div>
			<div class="row">
				<div class="col-md-12">
					<div class="prism-player" id="player-con"></div>
					<script>
					var player = new Aliplayer({
					  "id": "player-con",
					  "source": "''' , '''",
					  "width": "80%",
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
					<script>
						function gotoMain(){
							window.location.replace("https://openols.basicws.net/web/Student/");
                                                        }
					</script>
				</div>
			</div>
		</div>
	</div>
</div>
    </body>
</html>

<div class="container-fluid">
	<div class="row">
		<div class="col-md-12">
			<div class="row">
				<div class="col-md-11">
				</div>
				<div class="col-md-1">
				</div>
			</div>
			<div class="row">
				<div class="col-md-12">
				</div>
			</div>
		</div>
	</div>
</div>''']

mobileHTML= ['''<!DOCTYPE HTML>
<html>
    <head>
		<head>    
		<meta charset="UTF-8">
		<title>移动端直播间测试</title>

		<!-- 新 Bootstrap4 核心 CSS 文件 -->
		<link rel="stylesheet" href="https://cdn.staticfile.org/twitter-bootstrap/4.3.1/css/bootstrap.min.css">
		
		<!-- jQuery文件。务必在bootstrap.min.js 之前引入 -->
		<script src="https://cdn.staticfile.org/jquery/3.2.1/jquery.min.js"></script>
		
		<!-- bootstrap.bundle.min.js 用于弹窗、提示、下拉菜单，包含了 popper.min.js -->
		<script src="https://cdn.staticfile.org/popper.js/1.15.0/umd/popper.min.js"></script>
		
		<!-- 最新的 Bootstrap4 核心 JavaScript 文件 -->
		<script src="https://cdn.staticfile.org/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>
		
		<meta http-equiv="x-ua-compatible" content="IE=edge" >
		<meta name="viewport" content="width=device-width, height=device-height, initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no"/>

        <script src="https://boyinthesun.cn/others/flvplayer.js"></script>
        <script src="https://boyinthesun.cn/others/flvplayer-control.js"></script>
        
		</head>
    </head>
    <body>
<div class="container-fluid">
	<div class="row">
		<div class="col-md-12">
			<div class="row">
				<div class="col-md-11">
					<h2>移动端测试直播间</h2>
				</div>
				<div class="col-md-1">
					<button type="button" class="btn btn-success" onclick="gotoMain();">
						返回主页
					</button>
				</div>
			</div>
			<div class="row">
				<div class="col-md-12">
                    <div class="flvplayer-app"></div>

                    <script>
                    var flv = new FlvPlayer({
                        container: '.flvplayer-app',
                        poster: './assets/img/weathering-with-you-poster.jpg',
                        url: ' ''' , ''' ',
                        decoder: 'https://boyinthesun.cn/others/flvplayer-decoder-baseline.js',
                        // decoder: './uncompiled/flvplayer-decoder-multiple.js',
                        debug: true,
                        live: true,
                        loop: true,
                        autoPlay: true,
                        hasAudio: true,
                        control: true,
                        muted: false,
                        volume: 0.7,
                        frameRate: 30,
                        maxTimeDiff: 200,
                        videoChunk: 1024 * 1024,
                        audioChunk: 64 * 1024,
                        width:1280,
                        height:720,
                    });</script>
                    
					<script>
						function gotoMain(){
							window.location.replace("https://openols.basicws.net/web/Student/");
                        }
					</script>
				</div>
			</div>
		</div>
	</div>
</div>
    </body>
</html>

'''
]
