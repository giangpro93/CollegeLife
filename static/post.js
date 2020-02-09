function handleBtnClick(event) {
  var pressed = (event.target.getAttribute("aria-pressed") === "true");
  // Change aria-pressed to the opposite state
  var eventID = event.target.getAttribute("id");
  $.ajax({
      type: "POST",
      url: '/updateGoingStatus',
      data: {
        json_string: JSON.stringify({eventID: eventID, going: !pressed})
      },
      success: function(response){
          if(response=="Failed")
          {
              window.alert("Failed to update going status")
              return "Failed"
          }
          else{
              event.target.setAttribute("aria-pressed", !pressed);
          }
      }
  })
}
