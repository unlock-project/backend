alert_iterator = 0;

function createAlert(text, color = "success")
{
  var alert = document.createElement("div")
  alert.innerHTML = text +`
  <button type="button" class="close" data-dismiss="alert" aria-label="Close">
    <span aria-hidden="true">&times;</span>
  </button>`
  alert.className = "alert alert-"+ color +" alert-dismissible fade show";
  alert.role = "alert";
  alert.id = "alert" + alert_iterator;
  var alert_block = document.getElementById("alert_block")
  alert_block.appendChild(alert)
  alert_iterator++;
  setTimeout((alertId) => $("#" + alertId).alert("close"), 5000, alert.id)
}