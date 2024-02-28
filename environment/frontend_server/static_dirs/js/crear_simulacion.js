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
          <div class="character-form">
            <h3>Personaje ${i}</h3>
            <select id="nombre${i}" required>
                <option value="" disabled selected>Selecciona un nombre</option>
              ${nombres.map(nombre => `<option value="${nombre}">${nombre}</option>`)}
            </select>
            <textarea id="contexto${i}" required></textarea>
          </div>
        `);
      }
    }
  
    updateCharacterForms();
  });
  