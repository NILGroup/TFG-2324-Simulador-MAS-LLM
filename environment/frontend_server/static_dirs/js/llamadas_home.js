// Código JQuery para la gestión de las llamadas al backend en relación con la gestión de una simulación
// (play, pase, guardar para ver, guardar para continuar y salir sin guardar)

$(document).ready(function() {
    let simulacionCorriendo = true;

    const simulationStateText = $('#textoEstadoSimulacion');
    const boton_play = $('#play_button');
    const boton_pause = $('#pause_button');
    const boton_run = $('#boton_run');
    const input_steps = $('#num_steps');    
    const boton_guardar_ver = $('#boton_guardar_ver');
    const boton_guardar_y_salir = $('#boton_guardar_y_salir');
    const boton_salir = $('#boton_salir');
    const boton_chat = $('.boton_chat');
    const boton_susurro = $('.boton_susurro');
    const boton_abrir_chat = $('.abrir_chat');
    const boton_abrir_susurro = $('.abrir_susurro');

    function gestionarVisibilidad() {
        boton_run.prop('disabled', !simulacionCorriendo);
        input_steps.prop('disabled', !simulacionCorriendo);
        boton_guardar_ver.prop('disabled', simulacionCorriendo);
        boton_guardar_y_salir.prop('disabled', simulacionCorriendo);
        boton_salir.prop('disabled', simulacionCorriendo);
        boton_abrir_chat.prop('disabled', simulacionCorriendo);
        boton_abrir_susurro.prop('disabled', simulacionCorriendo);
    }

    function actualizarTextoSimulacion() {
        const message = simulacionCorriendo ? "La simulación se está ejecutando..." : "La simulación está parada";
        const color = simulacionCorriendo ? 'green' : 'red';
        simulationStateText.text(message).css('color', color);
    }

    gestionarVisibilidad();
    actualizarTextoSimulacion();

    boton_play.click(function() {
        simulacionCorriendo = true; // Estado de la simulación corriendo (se realizan llamadas a process environment)
        gestionarVisibilidad();
        actualizarTextoSimulacion();
        console.log("Iniciando la simulación " + simulacionCorriendo)
    });

    boton_pause.click(function() {
        simulacionCorriendo = false; // Estado de la simulación pausada (no se realizan llamadas a process environment)
        gestionarVisibilidad();
        actualizarTextoSimulacion();

        console.log("Pausando la simulación " + simulacionCorriendo)
        // sendAjaxCall('pause');
    });

    boton_run.click(function() {
        // Obtener el valor del select de pasos
        let values = {};
        let steps = $('#step-select').val();
        values['steps'] = steps;

        console.log(steps);
        sendAjaxCall('run', values);
    });

    boton_guardar_ver.click(function() {
        console.log("Guardando la simulación para ver después")
        sendAjaxCall('guardar_ver');
    });
    
    boton_guardar_y_salir.click(function() {
        console.log("Guardando la simulación para continuar después")
        sendAjaxCall('guardar_salir');
    });

    boton_salir.click(function() {
        console.log("Saliendo de la simulación")
        sendAjaxCall('salir');
    });

    boton_chat.click(function() {
        const chat = $(this).closest('.modal').find('textarea').val(); 
        const personaName = $(this).closest('.modal').find('input').val();

        console.log("chateando");

        let values = {};
        values['persona_name'] = personaName;
        values['chat'] = chat;
        console.log(values);

        sendAjaxCall('chat', values);
    });

    boton_susurro.click(function() {
        const susurro = $(this).closest('.modal').find('textarea').val(); 
        const personaName = $(this).closest('.modal').find('input').val();

        let values = {};
        values['persona_name'] = personaName;
        values['susurro'] = susurro;
        console.log(values);

        sendAjaxCall('susurro', values);
    });

    function sendAjaxCall(action, values = {}) {
        const dataToSend = {
            action: action,
            values: values
        };

        $.ajax({
            url: '/manejador-acciones-simulacion/', 
            type: 'POST',
            data: JSON.stringify(dataToSend),
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
