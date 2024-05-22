// Código JQuery para la gestión de las llamadas al backend en relación con la gestión de una simulación
// (play, pase, guardar para ver, guardar para continuar y salir sin guardar)

function gestionarVisibilidad(simulacionCorriendo, problemaBack) {
    const boton_run = $('#boton_run');
    const input_steps = $('#num_steps'); 
    const boton_guardar_ver = $('#boton_guardar_ver');
    const boton_guardar_y_salir = $('#boton_guardar_y_salir');
    const boton_salir = $('#boton_salir');
    const boton_abrir_chat = $('.abrir_chat');
    const boton_abrir_susurro = $('.abrir_susurro');

    let disableButtons = simulacionCorriendo | problemaBack;

    boton_run.prop('disabled', disableButtons);
    input_steps.prop('disabled', disableButtons);
    boton_guardar_ver.prop('disabled', disableButtons);

    boton_guardar_y_salir.prop('disabled', simulacionCorriendo);
    
    boton_salir.prop('disabled', disableButtons);
    boton_abrir_chat.prop('disabled', disableButtons);
    boton_abrir_susurro.prop('disabled', disableButtons);
}

function actualizarTextoSimulacion(simulacionCorriendo, steps, problemaBack) {
    const simulationStateText = $('#textoEstadoSimulacion');
    if (problemaBack) {
        const message = "Hubo un problema con el LLM reinicie la simulación";
        const color = 'red';
        simulationStateText.text(message).css('color', color);
    } else {
        const message = simulacionCorriendo ? "Quedan "+steps+" steps por ejecutar" : "";
        const color = simulacionCorriendo ? 'red' : 'green';
        simulationStateText.text(message).css('color', color);
    }
}

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
        },
        error: function(error) {
            console.error("Error enviando la acción del botón:", error);
        }
    });
}

$(document).ready(function() {
    let simulacionCorriendo = true;

    const sim_code = $('#simulacion_en_ejecucion').val();
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

    // Se desactivan por que són para la interacción con la demo
    boton_play.css('display', 'none');
    boton_pause.css('display', 'none');

    boton_run.click(function() {
        // Obtener el valor del select de pasos
        let values = {};
        let steps = $('#num_steps').val();
        values['steps'] = steps;
        console.log("Estamos en ", step, steps);
        desired_step = step + parseInt(steps);
        console.log("Queremos", desired_step);
        sendAjaxCall('run', values);
    });

    boton_guardar_ver.click(function() {
        console.log(step, sim_code)
        console.log("Guardando la simulación para ver después")
        sendAjaxCall('guardar_ver', {sim_code: sim_code, step: step});
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

});
