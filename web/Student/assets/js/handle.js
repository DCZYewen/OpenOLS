//to mzWyt This is a lib for dealing with the token etc.
pageUrl = 'http://dev.sunboy.site'
loginPanel = pageUrl + '/login'

function flushToken(token , user_id){
    var url = API_URL + '/get_new_token/?user_id=' + user_id + '&token=' + token;
    $.get( url , function callback(data){
        if (data.status == 'OK'){
            $.cookie('token',data.token);
            $.cookie('user_id',data.user_id);
            return 0;
        }
        else{
            goHome();
        }
    })
}

function logOut(token , user_id){
    var url = API_URL + '/logout/?user_id=' + user_id + '&token=' + token;
    $.get( url , function callback(data){
        if (data.status == 'OK'){
            alert("登出成功");
            $.cookie('auth',data.auth);
            $.cookie('token','');//清除token和user_id
            $.cookie('user_id','');
            return 0;
        }
        else{
            goHome();
        }
    })
}

function goToLogin(){
    window.location.replace(loginPanel);
}

function checkToken(token , user_id){
    var url = API_URL + '/check_valid/?user_id=' + user_id + '&token=' + token;
    $.get( url , function callback(data){
        if (data.status == 'OK'){
            return 'Valid';
        }
        else{
            goHome();
        }
    })
}

function goHome(){
    alert("您的登陆状态出现问题或者服务器故障，请联系管理员。");
    goToLogin();
}