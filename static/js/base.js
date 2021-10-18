var time = 5;

$(document).ready(function () {
  if ($("#time").length > 0) {
    var timer = setInterval(() => {
      time--;
      if (time === 0) {
        $("#time").fadeOut("slow");
        clearInterval(timer);
      }
    }, 1000);
  }
});
