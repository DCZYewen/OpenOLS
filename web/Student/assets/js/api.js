API_URL = "https://oolsapi.basicws.net"

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name)==0) return c.substring(name.length,c.length);
    }
    return "";
}

function setCourceName(token, userid, courseid) { // This func works but shitty. - mzWyt
    
    var url = API_URL + '/fetch_course_by_id/?user_id=' + userid + '&token=' + token + '&course_id=' + courseid;

    $.get(url,function callback(data){
        if (data.status == 'OK'){
			init = API_URL + '/live?user_id=' + userid + '&token=' + token + '&course_id=' + courseid;
			html = '<a href="' + init + '">' + data.title + '</a>
            document.getElementById("last_class").innerHTML = html
        }
        else{
            alert("获取课程信息失败！");
        }
    });
}

function formatFileSize(fileSize) { //Format capacity func
    if (fileSize < 1024) {
        return fileSize + 'B';
    } else if (fileSize < (1024*1024)) {
        var temp = fileSize / 1024;
        temp = temp.toFixed(2);
        return temp + 'KB';
    } else if (fileSize < (1024*1024*1024)) {
        var temp = fileSize / (1024*1024);
        temp = temp.toFixed(2);
        return temp + 'MB';
    } else {
        var temp = fileSize / (1024*1024*1024);
        temp = temp.toFixed(2);
        return temp + 'GB';
    }
}

function load_mainpage_info() {

    var Token = getCookie("token")
    var User_Id = getCookie("user_id")

    if(!Token || !User_Id){
        goHome()
        return
    }

    var url = API_URL + '/mainpage/?user_id=' + User_Id + '&token=' + Token;

    $.get(url,function callback(data){
        if (data.status == 'OK'){
            document.getElementById("stu_name").innerHTML = data.information.name;
            document.getElementById("grade_n_sex").innerHTML = data.information.grade + '级学生 | ' + data.information.gender;

            document.getElementById("intro").innerHTML = data.information.intro
            document.getElementById("motto").innerHTML = data.information.motto;
            
            setCourceName(Token, User_Id, data.information.last_course)            
            document.getElementById("exit_time").innerHTML = data.information.exit_time

            var CPU_Usage = data.statistics.Total_Usage.toFixed(1) + "%"
            var MEM_Total = formatFileSize(data.statistics.Total_Mem)
            var MEM_Usage = (data.statistics.Total_Mem - data.statistics.Free_Mem )/ data.statistics.Total_Mem * 100
            MEM_Usage = MEM_Usage.toFixed(1) + "%" //Gemini : Fixed display issue #
        
            document.getElementById("pb_CPU_usage").style = "width: " + CPU_Usage + ";"
            document.getElementById("pb_CPU_usage").innerHTML = CPU_Usage

            document.getElementById("pb_MEM_total").innerHTML = MEM_Total

            document.getElementById("pb_MEM_usage").style = "width: " + MEM_Usage + ";"
            document.getElementById("pb_MEM_usage").innerHTML = MEM_Usage

        }
        else{
            alert("连接服务器失败！")
        }
    });

}
