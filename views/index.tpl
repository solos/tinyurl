<!Doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>台泥缩-网址缩短</title>
    <link href="static/base.css" media="screen" rel="stylesheet" type="text/css" />
    <link href="static/main.css" media="screen" rel="stylesheet" type="text/css" />
    <script src="static/jquery-1.8.1.min.js"></script>
</head>
<body>
<br/>
<br/>
<h1 align="center">台泥缩-网址缩短</h1>
<br/>
<div align="center">
<br/>
<div name="form">
    <form>
    <div name="inputbox">
        <input name="url" type="text" id="url" placeholder="请输入要缩短的网址"/>
    </div>
    <div name="inputbutton">
        <input type="submit" id="tinyurl" value="网址缩短" />
    </div>
    </form>
</div>
<div style="clear:both;"></div>
<div name="custom">
    <div name="custom_title">自定义:</div>
    <div name="baseurl">http://{{domain}}{{port}}/</div><div name="custom_id"><input name="custom_id" type="text" placeholder="请输入要用的短址"/></div></div>
</div>
</div>
<div id="result" align="center"></div>
<script>
    $("#tinyurl").click(function(e){
        e.preventDefault();
        var url = $("input[name='url']").val();
        var custom_id = $("input[name='custom_id']").val();
        if (! valid_url(url)) {
            alert('亲，url仅支持 http/https/ftp/mailto/dataurl/ed2k等协议');
            return ''
        }
        if (!valid_custom_id(custom_id) && custom_id != "") {
            alert('亲，自定义短址仅支持5-32位数字、大小写字母');
            return ''
        }
        var apiurl = '/api';
        $.ajax({
            type: 'POST',
            url: apiurl,
            data: "url="+encodeURIComponent(url)+"&custom_id="+custom_id,
            dataType: "json",
            success: function(data){
                $("#result").html("<a href='" + data.tinyurl + "'>" + data.tinyurl + "</a>");
            }
        });

    function valid_url(url) {
        var patten = new RegExp(/^(https?:\/\/|ftp:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}(:\d{1,4})?(\/[\w ./?%&=!-]*)?|mailto:[^@]+@([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}|data:.+|ed2k:.+$/);
        return patten.test(url);
    }

    function valid_custom_id(custom_id) {
        var patten = new RegExp(/^[a-zA-Z0-9]{5,32}$/);
        return patten.test(custom_id);
    }

    });
</script>

 <div id="footer" align="center">
    <a href="https://github.com/solos/tinyurl" target="_blank" title="关于台泥缩">关于台泥缩</a>&nbsp;&nbsp;By <a target="_blank" href="http://linuxfan.me">solos</a>&nbsp;&nbsp;</div>

</body>
</html>
