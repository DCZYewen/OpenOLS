//Statics declaration
API_URL = "https://o2ls.basicws.net/"
PAGE_URL = "https://o2ls.basicws.net/"

function login() {
    var username = document.getElementById("username");
    var pass = document.getElementById("password");
    if (username.value == "") {
        alert("请输入用户名");
    } else if (pass.value  == "") {
        alert("请输入密码");
    } else {
        var myDate = new Date();
        var Sec = myDate.getSeconds(); 
        var encrypt_passwd = window.btoa(Sec + pass.value + Sec);
        var url = API_URL + '/login/?username=' + username.value + '&password=' + encrypt_passwd + '&time=' + Sec;

        $.get(url,function callback(data){
            console.log(data);
            if (data.status == 'OK' && data.AUTH == 'STUDENT'){
                $.cookie('token', data.token , {path:'/web/Student/'});
                $.cookie('auth', data.AUTH , {path:'/web/Student/'});
                $.cookie('user_id', data.user_id , {path:'/web/Student/'});
                window.location.replace(data.redirect_url);
            }
            else if (data.status == 'OK' && data.AUTH == 'TEACHER'){
                $.cookie('token', data.token , {path:'/web/Teacher/'});
                $.cookie('auth', data.AUTH , {path:'/web/Teacher/'});
                $.cookie('user_id', data.user_id , {path:'/web/Teacher/'});
                window.location.replace(data.redirect_url);
            }
            else{
                alert("用户名或密码错误！");
            }
        });

    }
    
}
