$(function () {
    //根据类型显示或隐藏一些部件
    if(showType == "view"){

    }
    else if (showType == "review"){

    }
})
$(function(){
    // 隐藏例句
    $("shcut-blk").css("display", "none")

    //隐藏例句
    $("def").nextAll().css("display", "none")

    //点击定义显示/隐藏例句
    $("def").click(function(){
        if ($(this).next().css("display") == "none"){
            $(this).nextAll().css("display", "block")
        }
        else{
            $(this).nextAll().css("display", "none")
        }
    })

    //show HTML button
    $("#editHtmlButton").click(function(){
        if ($("#editHtmlForm").css("display") == "block"){
            $("#editHtmlForm").css("display", "none")
        }else{
            $("#editHtmlForm").css("display", "block")
        }
    })

    //submit HTML button
    $("#editHtmlSubmit").click(function(){
        if ($("#editHtmlForm").css("display") == "block"){
            $("#editHtmlForm").css("display", "none")
        }else{
            $("#editHtmlForm").css("display", "block")
        }
        $.post(
            "/edithtml",
            {
                entry: $("#entry").attr("value"),
                raw: $("#editHtmlContent").val()
            },
            function (data, status) {
                location.reload()
            }
        );
    })

    //record button
    $("#testButton").click(function () {
        $.post(
            "/recordtest",
            {
                entry: $("#entry").attr("value"),
                score: $("#testScore").val(),
            },
            function (data, status) {

            }
        );
    })
});
