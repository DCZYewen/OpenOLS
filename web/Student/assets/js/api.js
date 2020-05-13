API_URL = "http://api.sunboy.site"

function mainpage_info() {
    // var username = document.getElementById("username");
    // var pass = document.getElementById("password");
    // if (username.value == "") {
    //     alert("请输入用户名");
    // } else if (pass.value  == "") {
    //     alert("请输入密码");
    // } else {
    //     var myDate = new Date();
    //     var Sec = myDate.getSeconds(); 
    //     var Back_Json;
    //     var encrypt_passwd = window.btoa(Sec + pass.value + Sec);
    //     var url = API_URL + '/login/?username=' + username.value + '&password=' + encrypt_passwd + '&time=' + Sec;
    //     $.get(url,function callback(data){
    //         console.log(data);
    //         if (data.status == 'OK'){
    //             document.cookie = 'user_id = ' + data.user_id;
    //             document.cookie = 'token = ' + data.token;
    //             document.cookie = 'auth = ' + data.auth;
    //             window.location.href=data.redirect_url;
    //         }
    //         else{
    //             alert("用户名或密码错误！")
    //         }
    //     });

    // }

    document.getElementById("name").innerHTML = "许";
}