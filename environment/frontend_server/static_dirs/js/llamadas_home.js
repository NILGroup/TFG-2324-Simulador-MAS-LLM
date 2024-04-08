// Código JQuery para la gestión de las llamadas al backend en relación con la gestión de una simulación
// (play, pase, guardar para ver, guardar para continuar y salir sin guardar)

$(document).ready(function() {
    $('#boton_play').click(function() {
        // get the value from the input number field
        let values = {};
        let steps = $('#step-select').val();
        values['steps'] = steps;
        console.log(steps)
        console.log("Iniciando la simulación")
        sendAjaxCall('play', values);
    });

    $('#pause_button').click(function() {
        console.log("Pausando la simulación")
        sendAjaxCall('pause');
    });

    $('#boton_guardar_ver').click(function() {
        console.log("Guardando la simulación para ver después")
        sendAjaxCall('guardar_ver');
    });
    
    $('#boton_guardar_y_salir').click(function() {
        console.log("Guardando la simulación para continuar después")
        sendAjaxCall('guardar_salir');
    });

    $('#boton_salir').click(function() {
        console.log("Saliendo de la simulación")
        sendAjaxCall('salir');
    });

    $('#boton_chat').click(function() {
        // TODO: En este caso, hay que coger también el id o nombre del personaje con el que se quiere chatear
        console.log("Chateando con un personaje")
        sendAjaxCall('chat');
    });

    $('#boton_susurro').click(function() {
        // TODO: En este caso, hay que coger también el id o nombre del personaje al que susurrar
        console.log("Susurrando a un personaje")
        sendAjaxCall('susurro');
    });

    function sendAjaxCall(action, values = {}) {
        const dataToSend = {
            action: action,
            values: values
        };

        $.ajax({
            url: '/manejador-acciones-simulacion/', 
            type: 'POST',
            data: dataToSend,
            dataType: 'json',
            success: function(response) {
                console.log("La acción del botón fue enviada correctamente:", response);
            },
            error: function(error) {
                console.error("Error enviando la acción del botón:", error);
            }
        });
    }
});
