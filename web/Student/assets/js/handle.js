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

function checkToken(token , user_id ){
    return new Promise((resolve , reject) => {
        var url = API_URL + '/check_valid/?user_id=' + user_id + '&token=' + token ;
        $.get( url , function callback(data){
            if (data.status == 'OK'){
                var res = 'Valid'
                return resolve(res);
            }
            else{
                var err = 'Invalid'
                return reject(err);
            }
        })
    })
        .then((state) => {
            return state;
        }).catch((err) => {
            return err;
        });
}

function goHome(){
    alert("您的登陆状态出现问题或者服务器故障，请联系管理员。");
    goToLogin();
}

function formatTime(time_entity){
    var yr = time_entity.substr(0,3);
    var mon = time_entity.substr(4,5);
    var day = time_entity.substr(5,6);
    var hr = time_entity.substr(7,8);
    var min = time_entity.substr(9,10);
    var sec = time_entity.substr(11,12);
    var para = time_entity.substr(13,14);

    var fullTimeString = yr + '年' + mon + '月' + day +'日' + hour + '点' + min + '分' + sec + '秒' ;
    var semiTimeString = mon + '月' + day +'日' + hour + '点' + min + '分';
    var returnItem = [fullTimeString,semiTimeString,yr,mon,day,hr,min,src,para];
    return returnItem;
}