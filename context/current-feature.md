# Construir una herramienta en el entorno de OpenCode

Se desea una pequeña aplicación de línea de comandos inspirada en Unix `wc`.

La herramienta se llamará `wordcount`.

### 1. Diseña la aplicación

El diseño debe contemplar:

- Una CLI basada en **Typer** o una biblioteca equivalente.

- Opciones para contar líneas, palabras y caracteres.

- Una semántica de opciones inspirada en `wc`.

- Un comportamiento definido para el caso en que no se especifique ninguna opción.


### 2. Implementa y prueba

Implementa la aplicación con ayuda del agente.

Pídele que:

- escriba las pruebas necesarias;

- analice la cobertura;

- aumente la cobertura hasta alcanzar **al menos el 90 %**.

No es necesario reproducir todas las funcionalidades de `wc`.

### 3. Documenta la ejecución

Incluye un fichero `loremipsum.txt` en el proyecto y pide al agente que prepare unas instrucciones breves de ejecución.

El `README` debe mostrar ejemplos para contar:

- líneas;

- palabras;

- caracteres;

- varias métricas simultáneamente.

