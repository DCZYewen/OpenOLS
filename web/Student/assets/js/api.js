API_URL = "http://api.sunboy.site"

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i<ca.length; i++) {
        var c = ca[i].trim();
        if (c.indexOf(name)==0) return c.substring(name.length,c.length);
    }
    return "";
}

function formatFileSize(fileSize) {
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

    var Token = getCookie(token)
    var User_Id = getCookie(user_id)

    // var Token = "rSPnzG6Cf%2FHayX2pbsjoxoAn4ZwK6Ui7oz6bA%2FC1p2Y%3D";
    // var User_Id = 99999998;

    var url = API_URL + '/mainpage/?user_id=' + User_Id + '&token=' + Token;
    
    // alert(url)

    $.get(url,function callback(data){
        console.log(data);
        if (data.status == 'OK'){
            document.getElementById("stu_name").innerHTML = data.information.name;
            document.getElementById("grade_n_sex").innerHTML = data.information.grade + '级学生 | ' + data.information.gender;

            document.getElementById("intro").innerHTML = data.information.intro
            document.getElementById("motto").innerHTML = data.information.motto;

            document.getElementById("last_class").innerHTML = data.information.last_course
            document.getElementById("exit_time").innerHTML = data.information.exit_time

            var CPU_Usage = data.statistics.Total_Usage + "%"
            var MEM_Total = formatFileSize(data.statistics.Total_Mem)
            var MEM_Usage = data.statistics.Free_Mem / data.statistics.Total_Mem * 100
            MEM_Usage = MEM_Usage.toFixed(1) + "%"
        
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