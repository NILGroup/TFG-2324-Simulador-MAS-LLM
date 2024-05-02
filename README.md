
# TFG-2324-Simulador-MAS-LLM
Repositorio para el TFG de Kevin Arce y Alberto Ramos sobre un simulador multiagente dirigido por LLMs.

<p align="center" width="100%">
<img src="cover.png" alt="Smallville" style="width: 80%; min-width: 300px; display: block; margin: auto;">
</p>

El objetivo principal de este Trabajo de Fin de Grado es democratizar el uso del estudio realizado en el siguiente paper: "[Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442)", así como extender algunas de las funcionalidades existentes en el mismo y modificar la manera de ejecutar de la aplicación completamente.

Por ello, hemos realizado esta documentación, la cual era algo complicada en el programa inicial, para que cualquier persona pueda ejecutar la aplicación sin problemas. Además, la hemos escrito en castellano para mayor facilidad.

## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Isabella_Rodriguez.png" alt="Generative Isabella">   Configurando el entorno 

Ahora, configurar el entorno será mucho más sencillo que antes. A continuación, se detallan los pasos a seguir para poder ejecutar la aplicación sin problemas.

### Paso 1. Crear un entorno virtual

Primero, es necesario crear un entorno virtual para instalar las dependencias necesarias. Para ello, se puede utilizar el siguiente comando:

    python3 -m venv env

### Paso 2. Activar el entorno virtual

Una vez creado el entorno virtual, es necesario activarlo. Para ello, se puede utilizar el siguiente comando:

    source env/bin/activate

### Paso 3. Instalar las dependencias

Una vez activado el entorno virtual, es necesario instalar las dependencias necesarias. Para ello, se puede utilizar el siguiente comando:

    pip install -r requirements.txt

### Paso 4. Declarar la clave de la API como variable de entorno

Para poder ejecutar la aplicación, es necesario declarar la clave de la API de OpenAI como variable de entorno. Para ello, simplemente abriremos la terminal en la que tengamos activado el entorno virtual y ejecutaremos el siguiente comando:

    OPENAI_API_KEY=<Tu clave de la API de OpenAI>


## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Klaus_Mueller.png" alt="Generative Klaus">   Ejecutar la simulación 

Para ejecutar una nueva simulación, será necesario iniciar dos servidores simultáneamente: el servidor de entorno y el servidor de simulación de agentes.

### Paso 1. Iniciar el servidor de entorno

El entorno se implementa como un proyecto de Django, y como tal, deberá iniciar el servidor de Django. Para ello, primero navegue hasta `environment/frontend_server` (aquí es donde se encuentra `manage.py`) en su línea de comandos. Luego, ejecute el siguiente comando:

    python manage.py runserver

A continuación, en su navegador favorito, vaya a [http://localhost:8000/](http://localhost:8000/). Aquí ya podremos ver la página de landing, pero no será posible ejecutar simulaciones hasta que no se inicie el segundo servidor. Asegúrese de que el servidor de entorno siga funcionando mientras ejecuta la simulación, ¡así que mantenga esta pestaña de línea de comandos abierta! (Nota: Se recomienda usar Chrome o Safari. Firefox podría producir algunos errores en el frontend, aunque no debería interferir con la simulación en sí).

### Paso 2. Iniciar el servidor de simulación

Abra otra línea de comandos (la que utilizó en el Paso 1 debería seguir ejecutando el servidor de entorno, así que déjela como está). Navegue hasta `reverie/backend_server` y ejecute `reverie.py`.

    python reverie.py

Esto iniciará el servidor de la simulación. Aparecerá un prompt de línea de comandos pero podemos ignorarlo ya que toda la interacción con la simulación se realizará mediante la interfaz gráfica.


## <img src="https://joonsungpark.s3.amazonaws.com:443/static/assets/characters/profile/Isabella_Rodriguez.png" alt="Generative Isabella">   Interactuar con la simulación

Con todo esto, ya estamos listos para interactuar con la simulación. Para ello, simplemente abra su navegador favorito y vaya a [http://localhost:8000/](http://localhost:8000/). Aquí podrá ver la página de landing, donde podrá acceder a la guía de usuario, para informarse de todo lo que puede hacer y ver ejemplos o ir directamente a la creación, ejecución y visualización de simulaciones.


