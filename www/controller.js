$(document).ready(function () {

  eel.expose(DisplayMessage);
  function DisplayMessage(message) {
      $(".siri-message").text(message);   // fix selector, remove 'li:first'
      $('.siri-message').textillate({
        in: { effect: 'fadeInUp' },
        loop: false
      });
      $('.siri-message').text(message).textillate('start');
      
  }

  eel.expose(Showhood);
  function Showhood() {
      $('#Oval').attr("hidden", false);
      $('#siriwave').attr("hidden", true);
  }

  eel.expose(go_back);
  function go_back() {
      window.location.href = "index.html";  // Or your desired page
  }
  
});











