function bindEmailCaptchaClick() {
  $("#captcha-btn").click(function (event) {//#表示id click若点击了就执行函数function(event)
      // $this: 代表当前按钮的 jQuery 对象
      var $this = $(this);
      // 阻止默认的事件
      event.preventDefault();

      var email = $("input[name='email']").val();//.val()获取到输入框里面的值
      // 单独一个$表示jQuery库 $()表示函数
      $.ajax({//与服务器进行异步通信
          url: "/auth/captcha/email?email=" + email,//默认当前js所在域名
          method: "GET",
          success: function (result) {
              //这个result就是后端返回的数据---> return jsonify({"code": 200,"message":"","data": None})#返回json格式--- 状态码、信息、数据
              var code = result['code'];
              if (code == 200) {
                  var countdown = 60;
                  // 开始倒计时之前，取消按钮的点击事件
                  $this.off("click");//off就是取消事件
                  var timer = setInterval(function () {
                      $this.text(countdown);
                      countdown -= 1;
                      // 倒计时结束时执行
                      if (countdown <= 0) {
                          // 清除定时器
                          clearInterval(timer);
                          // 按钮文本恢复原样
                          $this.text("获取验证码");
                          // 重新绑定点击事件
                          bindEmailCaptchaClick();//递归
                      }
                  }, 1000);//setInterval()每隔多少毫秒执行函数--->定时器
                   $("#success-message").text("邮箱验证码发送成功!").show();
                    setTimeout(function () {
                        $("#success-message").hide(); // 3秒后隐藏消息
                    }, 3000);
              } else {
                  alert(result['message']);
              }
          },
          error: function (error) {
              console.log(error);
          }
      });
  });
}

// 整个网页加载完成后再执行
$(function () {
  bindEmailCaptchaClick();
});
// $(fun()):表示在整个网页元素都加载好了再执行func()
//function abc(){};表示一个函数

// $.ajax 函数是 jQuery 中用于执行异步 HTTP 请求的函数。它允许你与服务器进行交互，而无需重新加载整个页面。
//
// $.ajax 的主要用途包括：
//
// **获取数据：**从服务器获取 JSON、HTML 或其他格式的数据。
// **提交数据：**将数据提交到服务器，例如用于创建、更新或删除记录。
// **更新页面部分：**只更新页面的特定部分，而无需重新加载整个页面。
// **执行后台任务：**在不阻塞用户交互的情况下执行后台任务。
// $.ajax 使你能够与服务器进行异步通信，这意味着请求在后台发送和处理，而不会中断用户与页面的交互。这对于创建响应迅速且用户友好的 web 应用程序至关重要。