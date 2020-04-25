//Statics declaration
API_URL = "http://api.sunboy.site"
PAGE_URL = "http://dev.sunboy.site"

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
        fetch(url)
        .then(function(response) {
            return response.json();
          })
        .then(function(myJson) {
            console.log(myJson);
        });
    }
    
}