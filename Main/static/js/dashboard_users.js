function getUsersNo(){

  var req = new XMLHttpRequest();
  var url ='/getusersno'
  req.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
     alert(req.responseText);
    }
  };
  req.open("GET", "ajax_info.txt", true);
  req.send();

}