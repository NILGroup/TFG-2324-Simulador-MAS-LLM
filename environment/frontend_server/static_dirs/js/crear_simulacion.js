// Código JQUERY para la creación de una simulación, añadiendo de forma dinámica los personajes

$(document).ready(function() {
    // Por ahora, tenemos nombres predeterminados de la simulación. En el futuro podrán añadir los suyos los usuarios
    const names = ["Abigail Chen", "Adam Smith", "Arthur Burton", "Ayesha Khan", "Carlos Gomez", "Carmen Ortiz",
                    "Eddy Lin", "Francisco Lopez", "Giorgio Rossi", "Hailey Johnson", "Isabella Rodriguez", "Jane Moreno",
                "Jennifer Moore", "John Linn", "Klaus Mueller", "Latoya Williams", "Maria Lopez", "Mei Lin",  "Rajiv Patel", 
            "Ryan Park", "Sam Moore", "Tamara Taylor", "Tom Moreno", "Wolfgang Schulz", "Yuriko Yamamoto"];
  
    $('#numCharacters').on('change', function() {
       updateCharacterForms();
    });
  
    function updateCharacterForms() {
      let numCharacters = parseInt($('#numCharacters').val());
      $('#characterContainer').empty(); 
  
      for (let i = 1; i <= numCharacters; i++) { 
        $('#characterContainer').append(`
          <div class="character-form">
            <h3>Personaje ${i}</h3>
            <select id="nameSelect${i}" required>
                <option value="" disabled selected>Selecciona un nombre</option>
              ${names.map(name => `<option value="${name}">${name}</option>`)}
            </select>
            <textarea required></textarea>
          </div>
        `);
      }
    }
  
    updateCharacterForms();
  });
  