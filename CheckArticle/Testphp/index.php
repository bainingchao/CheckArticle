<!DOCTYPE>
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <title>项目查重检测系统</title>
    <style type="text/css">
        html{font-size:16px;}
        fieldset{width:1080px; margin: 0 auto;}
        legend{font-weight:bold; font-size:14px;}
        label{float:left; width:120px; margin-left:10px;}
        .left{margin-left:120px;}
        .input{width:150px;}
        span{color: #666666;}
    </style>
    <script language=JavaScript>
    <!--

    function InputCheck(CheckForm)
    {
      if (CheckForm.projectname.value == "" )
      {
        alert("请输入项目名称!");
        CheckForm.projectname.focus();
        return (false);
      }
      if (document.getElementById("projectsumb").value== "" )
      {
        alert("请输入项目简介!");
        CheckForm.projectname.focus();
        return (false);
      }
  }
    </script>
</head>
<body>
<div>
<fieldset>
<legend>项目查重检测系统</legend>
<form name="CheckForm" method="post" action="index.php" onSubmit="return InputCheck(this)">
    <div>
    <br/>
    <label for="projectname" class="label">项目名称:</label>
    <input id="projectname" name="projectname" type="text" style="width: 400px"     class="input" />
    <divp/>

    <div>
    <br/>
    <label for="projectsumb" class="label">项目简介:</label>
    <textarea name="projectsumb"  id="projectsumb" style="height:400px;width:800px;"></textarea>
    <div/>

    <div>
    <br/>
    <br/>
    <input type="submit" name="submit" value="  检 测  " class="left" />
    </div>
        <div>
    <br/>
    <label name="result" class="label">检测结果:</label>
    <label name="outresult" class="label"></label>
    <br/>
    <div/>

</form>
<br/>
<br/>

</div>
</body>
</html>
<?php
    $name=mb_convert_encoding($_POST['projectname'], "GBK","UTF-8");
    $sumb=mb_convert_encoding($_POST['projectsumb'], "GBK","UTF-8");
    $program="D:/Users/Administrator/Anaconda3/python E:/pythonSource/CheckArticle/CheckRepeat/checkIndex.py ".$name." ".$sumb.""; #注意使用绝对路径.$name."".$sumb
    $output = nl2br(shell_exec($program));
    // $program1="D:/Users/Administrator/Anaconda3/python ../CheckRepeat/test.py ".$name." ".$sumb.""; #注意使用绝对路径.$name."".$sumb
    // $result1 = shell_exec($program1);
    echo mb_convert_encoding ($output,"UTF-8", "GBK");
    // if ($output!=null){
    //     print_r(nl2br(file_get_contents('../CheckRepeat/database/DealCorpus/checkout.txt')));
    // }
?>

