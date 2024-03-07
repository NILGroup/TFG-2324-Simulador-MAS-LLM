// Código JQUERY para la creación de una simulación, añadiendo de forma dinámica los personajes

$(document).ready(function() {
    // Por ahora, tenemos nombres predeterminados de la simulación. En el futuro podrán añadir los suyos los usuarios
    const nombres = ["Abigail Chen", "Adam Smith", "Arthur Burton", "Ayesha Khan", "Carlos Gomez", "Carmen Ortiz",
                    "Eddy Lin", "Francisco Lopez", "Giorgio Rossi", "Hailey Johnson", "Isabella Rodriguez", "Jane Moreno",
                "Jennifer Moore", "John Linn", "Klaus Mueller", "Latoya Williams", "Maria Lopez", "Mei Lin",  "Rajiv Patel", 
            "Ryan Park", "Sam Moore", "Tamara Taylor", "Tom Moreno", "Wolfgang Schulz", "Yuriko Yamamoto"];
  
    $('#numPersonajes').on('change', function() {
       updateCharacterForms();
    });
  
    function updateCharacterForms() {
      let numPersonajes = parseInt($('#numPersonajes').val());
      $('#contenedorPersonaje').empty(); 
  
      for (let i = 1; i <= numPersonajes; i++) { 
        $('#contenedorPersonaje').append(`
          <div class="container character-form">
            <h3 class="fw-bold">Personaje ${i}</h3>
            <select name="nombre${i}" id="nombre${i}" required>
                <option value="" disabled selected>Selecciona un nombre</option>
              ${nombres.map(nombre => `<option value="${nombre}">${nombre}</option>`)}
            </select>
            <div class="row">
              <div class="col-md-6">
                <label for="innate${i}" class="fw-bold">Personalidad innata:</label>
                <select multiple name="innate${i}" id="innate${i}" class="mb-0" required> 
                    <option value="friendly">Amigable</option>
                    <option value="outgoing">Extrovertido</option>
                    <option value="hospitable">Hospitalario</option>
                    <option value="passionate">Apasionado</option>
                    <option value="kind">Amable</option>
                    <option value="energetic">Energético</option>
                    <option value="enthusiastic">Entusiasta</option>
                </select>
                <small class="text-muted">Selecciona con Ctrl o Cmd hasta un máximo de 3 personalidades</small>
              </div>
              <div class="col-md-6">
                <label for="lifestyle${i}" class="fw-bold">Estilo de vida:</label>
                <textarea name="lifestyle${i}" id="lifestyle${i}" placeholder="Breve texto sobre el estilo de vida del agente" required></textarea>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6">
                <label for="learned${i}" class="fw-bold">Conocimiento aprendido:</label>
                <textarea name="learned${i}" id="learned${i}" placeholder="Breve texto sobre los recuerdos iniciales del personaje" required></textarea>
              </div>
              <div class="col-md-6">
                <label for="currently${i}" class="fw-bold">Estado actual:</label>
                <textarea name="currently${i}" id="currently${i}" placeholder="Breve texto sobre las pretensiones e inquietudes actuales" required></textarea>
              </div>
            </div>
          </div>
        `);
      }
    }
  
    updateCharacterForms();
  });
  