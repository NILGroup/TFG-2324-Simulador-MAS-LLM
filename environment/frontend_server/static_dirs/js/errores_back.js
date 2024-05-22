// Funciones que se encarguen de gestionar los posibles errores que se dén en elback
// En concreto nos encargaremos de hacer las peticiones necesarias al back para que se adviertan los posibles errores

function hayErrores(url, callback) {
  var update_xobj = new XMLHttpRequest();
  update_xobj.overrideMimeType("application/json");
  update_xobj.open('POST', url, true);
  update_xobj.addEventListener("load", function() {
    if (this.readyState === 4) {
      if (update_xobj.status === 200) {
        if (JSON.parse(update_xobj.responseText)["<error>"] == true) {
          callback(true);
        } else {
          callback(false);
        }
      }
    }
  });
  update_xobj.send(JSON.stringify({}));
}