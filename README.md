[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/xB5owuT7)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23014341&assignment_repo_type=AssignmentRepo)
# Lab03: Visualización interactiva de datos en Raspberry Pi usando Python y Matplotlib

## Integrantes

[Juan Camilo Yepes](https://github.com/JuanCY99)
[Cristian Romero]()
[Kevin Mejia]()


## Documentación


## Preguntas

1. ¿Qué función cumple ```plt.fignum_exists(self.fig.number)``` en el ciclo principal?

La instrucción plt.fignum_exists(self.fig.number) actúa como la condición de control principal para el ciclo while responsable de la actualización continua de los datos.

cumple con los siguientes propósitos:

Verifica el estado de la interfaz gráfica: Su función específica es comprobar en cada iteración si la ventana de la figura generada por la biblioteca Matplotlib permanece abierta y activa en el sistema. Mientras la ventana exista, la instrucción evalúa como verdadero (True), permitiendo que el proceso de muestreo y graficación continúe.

Interrupción del programa: En el momento en que el usuario cierra la ventana manualmente la figura se destruye en la memoria. Consecuentemente, la función retorna falso (False), lo que provoca la finalización del ciclo while.

Prevención de errores de ejecución: Gracias a esta validación, se garantiza que el programa termine su ejecución de manera controlada (pasando al bloque finally). 

2. ¿Por qué se usa ```time.sleep(self.intervalo)``` y qué pasa si se quita?

tiene como propósito principal establecer una pausa controlada dentro de la ejecución del ciclo principal del programa. Este tiempo de espera establece la frecuencia de muestreo de los datos, definiendo los segundos exactos que el sistema debe aguardar entre una lectura de temperatura y la siguiente. Al implementar esta pausa, se regula el ritmo de actualización de la interfaz.

Si se elimina esta línea del código, el ciclo repetitivo se ejecutaría a la velocidad máxima que permita el hardware del dispositivo.

3. ¿Qué ventaja tiene usar ```__init__``` para inicializar listas y variables?

Garantiza la encapsulación y la independencia de los datos. Al definir variables como las listas de temperatura o los tiempos dentro de este método constructor, se convierten en atributos de instancia. Cada objeto generado a partir de la clase poseerá su propia copia aislada de dichos datos. Si el sistema requiriese ejecutar dos monitores de forma simultánea, cada uno registraría sus valores de manera completamente independiente. Por el contrario, si estas listas se declararan por fuera del constructor, operarían como variables de clase, lo que causaría que todos los monitores mezclaran sus lecturas en un mismo espacio de memoria compartida.

Centraliza la configuración en este bloque asegura un estado inicial limpio y predecible. Al momento de instanciar el objeto, el sistema asigna automáticamente los valores por defecto requeridos para el correcto funcionamiento del ciclo de monitoreo.

4. ¿Qué se está midiendo con ```self.inicio = time.time()```?

La instrucción self.inicio = time.time() captura el momento exacto en el que se inicia la ejecución del monitor de temperatura. Su función principal es establecer un punto de referencia temporal o tiempo cero para el sistema.

En lugar de medir una duración en ese instante específico, la línea guarda la hora actual del sistema operativo representada en segundos.

5. ¿Qué hace exactamente ```subprocess.check_output(...)```?

La instrucción subprocess.check_output tiene la función de establecer una comunicación directa e interna entre el script de Python y el sistema operativo de la Raspberry Pi.

Permite ejecutar instrucciones nativas de la consola de comandos directamente desde el código. En este caso específico, se encarga de lanzar la orden vcgencmd measure_temp, que es una herramienta nativa del hardware de la Raspberry Pi, diseñada para consultar la temperatura física actual del procesador central.

La función captura la respuesta textual que normalmente el sistema imprimiría en la pantalla de una terminal. Acto seguido, entrega esa información de vuelta al programa de Python. De esa forma, el script puede tomar esa respuesta cruda, limpiarla y extraer únicamente el valor numérico necesario para construir la gráfica.

6. ¿Por qué se almacena ```ahora = time.time() - self.inicio``` en lugar del tiempo absoluto?

El comando de tiempo del sistema entrega por defecto un número extremadamente grande, el cual representa todos los segundos que han pasado desde una fecha base en el pasado. Si este número gigante se colocara directamente en la parte inferior de la gráfica, los valores serían muy largos y confusos a simple vista.

Al realizar esta resta matemática, el programa logra que el contador de tiempo empiece exactamente en cero justo en el instante en que arranca la medición. De esta manera, el eje horizontal de la gráfica muestra únicamente los segundos que han transcurrido desde que se inició el monitoreo, haciendo que los datos sean claros y directos.

7. ¿Por qué se usa ```self.ax.clear()``` antes de graficar?


La instrucción self.ax.clear cumple la de limpiar el área de dibujo justo antes de trazar una nueva actualización visual.

Durante un monitoreo en tiempo real, el programa genera un nuevo conjunto de puntos cada vez que transcurre el intervalo de tiempo establecido. Si se omite esta instrucción de limpieza, la biblioteca gráfica dibujaría la nueva línea directamente sobre las líneas generadas en los segundos anteriores.

La pantalla se saturaría con múltiples trazos superpuestos. De igual manera, forzar al sistema a recordar y dibujar miles de líneas antiguas de forma simultánea agotaría rápidamente la memoria del equipo y provocaría un bloqueo o una caída severa en el rendimiento del programa.

8. ¿Qué captura el bloque ```try...except``` dentro de ```leer_temperatura()```?

El bloque de código mencionado actúa como un mecanismo de seguridad y prevención de fallosdel programa. Su propósito principal es anticipar y gestionar cualquier error que pueda surgir durante la comunicación con el hardware de la placa.

Al depender de una instrucción enviada directamente al sistema operativo, existen diversos factores que podrían interrumpir el proceso. Por ejemplo, la ejecución podría fallar si el script se corre en un PC convencional en lugar de una Raspberry Pi, o la respuesta del procesador podría contener caracteres inesperados que impidan transformar el texto extraído en un valor numérico decimal.

Si ocurre alguna de estas anomalías, la estructura de control captura el error inmediatamente e impide que el sistema colapse o se cierre . Como medida de contingencia, imprime un mensaje explicativo en la consola y entrega un valor nulo. De esta manera, el programa principal detecta que la lectura falló, descarta ese dato defectuoso y continúa funcionando ininterrumpidamente hasta el siguiente intento de medición.

9. ¿Cómo podría modificar el script para guardar las temperaturas en un archivo .```csv```?
Inicialmente se debe importar CSV
Dentro del método de inicialización __init__, se debe definir el nombre del archivo y configurar su estructura inicial.
se puede añadir al codigo el siguiente bloque 
self.nombre_archivo = "registro_temperaturas.csv"
        
        with open(self.nombre_archivo, mode='w', newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["Tiempo_Transcurrido_s", "Temperatura_C"])

Por último, se requiere modificar el método actualizar_datos para que cada nueva lectura se escriba inmediatamente en el registro. Justo después de la línea donde se añaden los datos a las listas, se debe incluir la orden para abrir el documento en modo de adición y guardar la nueva fila:

if temp is not None:
            self.tiempos.append(ahora)
            self.temperaturas.append(temp)

            
            with open(self.nombre_archivo, mode='a', newline='') as archivo:
                escritor = csv.writer(archivo)
                escritor.writerow([round(ahora, 2), temp])

