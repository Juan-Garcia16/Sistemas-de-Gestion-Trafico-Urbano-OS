# INTERRUPCIONES
Ing. Juan Andrés García Moreno
Necesidad de las interrupciones
Debido a la falta de una estandarización de técnicas para el manejo de los dispositivos E/S
y otros procesos, las interrupciones surgen de la necesidad que tienen los dispositivos
periféricos de enviar información al procesador principal de un sistema informático.
Técnica antecesora
La primera técnica que se empleó para esto fue el polling, que consistía en que el propio
procesador se encargara de sondear los dispositivos periféricos cada cierto tiempo para
averiguar si tenía pendiente alguna comunicación para él. Este método presentaba el
inconveniente de ser muy ineficiente, ya que el procesador consumía constantemente
tiempo y recursos en realizar estas instrucciones de sondeo.
¿Qué es una interrupción?
```
Es un mecanismo mediante el cual otros módulos (E/S, memoria) pueden interrumpir
```
```
(temporalmente) la ejecución normal del procesador y pasar a ejecutar una subrutina de
```
servicio de interrupción.
Permiten la gestión eficiente de las operaciones entre el hardware y el software. Una
interrupción es una señal enviada a la CPU que indica que un evento necesita atención
inmediata, interrumpiendo el flujo normal de ejecución del programa actual para atender
ese evento.
Clases de Interrupciones
De programa
Generadas por alguna condición que se produce como resultado de la ejecución de una instrucción,
como el desbordamiento aritmético, la división por cero, el intento de ejecutar una instrucción ilegal de
la máquina o una referencia a una zona de memoria fuera del espacio permitido al usuario.
De reloj
Generadas por un reloj interno del procesador. Esto permite al sistema operativo llevar a cabo ciertas
funciones con determinada regularidad.
De E/S
Generadas por un controlador de E/S, para indicar que una operación ha terminado normalmente o
para indicar diversas condiciones de error.
Por fallo del hardware
Generadas por fallos tales como un corte de energía o un error de paridad de la memoria.
Ejemplo de Interrupción
La mayoría de los dispositivos externos son mucho más lentos que el procesador. Supóngase que el procesador está
transfiriendo datos hacia una impresora, utilizando un esquema para el ciclo de instrucción como en la figura:
Después de cada operación ESCRIBIR, el procesador hará una pausa y permanecerá desocupado hasta que la
impresora se ponga al corriente. La duración de esta pausa puede ser del orden de varios cientos o incluso
miles de ciclos de instrucción en los que la memoria no está implicada.
¿Qué tanta eficiencia se tiene frente a la utilización del procesador?
Interrupciones de hardware
Descripción: Generadas por dispositivos de hardware como teclados, ratones, discos duros, y
otros periféricos cuando necesitan la atención de la CPU.
```
Ejemplos:
```
Pulsación de una tecla en el teclado.
Finalización de una operación de lectura/escritura en un disco duro.
```
Funcionamiento: Un controlador de dispositivo envía una señal de interrupción a la CPU a través del
```
```
controlador de interrupciones (PIC o APIC), solicitando atención.
```
Interrupciones de Software:
Descripción: Generadas por instrucciones de software para solicitar servicios del sistema operativo. También
```
conocidas como llamadas al sistema (system calls).
```
```
Ejemplos:
```
Un programa solicita acceso a un archivo mediante una llamada al sistema.
Un proceso solicita más memoria.
Desbordamiento aritmético.
División por cero.
Ejecución de instrucción ilegal.
Referencia fuera del espacio de la memoria permitido para el usuario
```
Funcionamiento: El software ejecuta una instrucción especial que genera una interrupción de software,
```
haciendo que la CPU transfiera el control al sistema operativo.
Flujo de control con y sin interrupciones
Las interrupciones y el ciclo de instrucción
Programa de usuario:
Muestra las etapas del programa de usuario, numeradas del 1 al
m.
En el punto i, se produce una interrupción, lo que detiene
temporalmente la ejecución del programa de usuario.
Manejador de interrupción:
Representa el código que maneja la interrupción.
Cuando se produce la interrupción en el punto i del programa de
usuario, el control se transfiere al manejador de interrupción.
Después de que el manejador de interrupción completa su tarea,
el control regresa al punto i+1 del programa de usuario,
continuando la ejecución normal.
Flujo del Diagrama
Interrupción en el punto i: Indica el momento en que se produce
la interrupción durante la ejecución del programa de usuario.
Manejador de interrupción: Ejecuta el código necesario para
manejar la interrupción.
Retorno al programa de usuario: Una vez que se maneja la
interrupción, el control regresa al programa de usuario en el
punto i+1, permitiendo que la ejecución continúe.
Ciclo de instrucción con interrupciones
```
Hay cierta sobrecarga en este proceso. Se deben ejecutar instrucciones extra (en
```
```
la rutina de tratamiento de la interrupción) para determinar la naturaleza de la
```
interrupción y decidir la acción apropiada. Sin embargo, por la cantidad de tiempo
que se desperdicia esperando en una operación de E/S, puede aprovecharse el
procesador de una manera mucho más eficaz con el uso de interrupciones.
Pasos del Diagrama
```
INICIO: El proceso comienza aquí.
```
Leer la instrucción siguiente: El sistema lee la próxima instrucción que
debe ejecutar.
Ejecutar la instrucción: La instrucción leída se ejecuta.
Interrupciones inhabilitadas: Si las interrupciones están deshabilitadas, el
sistema vuelve a ejecutar la instrucción.
Interrupciones habilitadas: Si las interrupciones están habilitadas, el
sistema verifica si hay una interrupción.
Comprobación de interrupción del proceso: El sistema comprueba si se
ha producido una interrupción.
Interrupción: Si hay una interrupción, el sistema entra en el “Ciclo de
interrupción” para manejarla.
No hay interrupción: Si no hay interrupción, el sistema vuelve al “Ciclo de
lectura” para leer la siguiente instrucción.
```
FIN: El proceso termina aquí.
```
Ciclos del Diagrama
Ciclo de lectura: El sistema lee y ejecuta instrucciones de manera continua.
Ciclo de ejecución: El sistema ejecuta las instrucciones leídas.
Ciclo de interrupción: El sistema maneja las interrupciones cuando se producen.
Tiempos de Tiempos: Espera corta
```
Diagrama (a): Sin interrupciones
```
Espera del procesador: El procesador está en espera hasta que se complete la
operación de E/S.
Operación de E/S: Se realiza la operación de entrada/salida.
Espera del procesador: El procesador vuelve a esperar hasta que se complete la
siguiente operación de E/S.
En este escenario, el procesador pasa mucho tiempo esperando, lo que no es eficiente.
```
Diagrama (b): Con interrupciones
```
Espera del procesador: El procesador espera inicialmente.
Operación de E/S: Se inicia la operación de entrada/salida.
Interrupción: Con la operación de E/S está en curso, el procesador puede realizar
otras tareas. Si ocurre una interrupción, el procesador maneja la interrupción.
2a: El procesador maneja la interrupción y luego vuelve a la operación de E/S.
2b: El procesador continúa con otras tareas mientras espera la finalización de la
operación de E/S.
Operación de E/S: Se completa la operación de entrada/salida.
Espera del procesador: El procesador vuelve a esperar si no hay más tareas
pendientes.
Comparación
•Sin interrupciones: El procesador está inactivo durante la
operación de E/S, lo que resulta en una baja eficiencia.
•Con interrupciones: El procesador puede realizar otras tareas
mientras espera la finalización de la operación de E/S, mejorando
la eficiencia general del sistema
Ejercicio en clase
Describir el comportamiento de las
interrupciones del diagrama
¿Qué es el PSW?
```
El PSW (Program Status Word) es un registro en los sistemas informáticos que desempeña varias
```
funciones críticas, es un componente crucial que ayuda a mantener el control y la eficiencia en la
ejecución de programas y la gestión de interrupciones en un sistema operativo.
Funciones del PSW
Registro de Estado: Almacena información sobre el estado actual del procesador, como los indicadores de
```
condición (flags) que muestran el resultado de la última operación aritmética o lógica.
```
```
Contador de Programa (PC): Contiene la dirección de la siguiente instrucción que debe ejecutarse. Esto
```
permite al procesador saber qué instrucción ejecutar a continuación.
Control de Interrupciones: Incluye bits que habilitan o deshabilitan las interrupciones, permitiendo al
sistema manejar eventos externos de manera eficiente.
Modo de Operación: Indica el modo en el que está operando el procesador, como el modo usuario o el
modo kernel.
Importancia del PSW
El PSW es esencial para la gestión del flujo de ejecución en un sistema operativo. Permite
al procesador:
Guardar y Restaurar Estados: Durante una interrupción, el PSW se guarda para que el
procesador pueda retomar la ejecución correcta después de manejar la interrupción.
Controlar el Flujo de Ejecución: Almacena la dirección de la siguiente instrucción, asegurando que
el procesador sigue la secuencia correcta de instrucciones.
Manejar Interrupciones: Facilita la habilitación y deshabilitación de interrupciones, permitiendo
una respuesta rápida a eventos externos.
```
Program Counter (PC)
```
Es un registro para la ejecución ordenada y eficiente de las instrucciones en un programa,
asegurando que el procesador siempre sepa cuál es la siguiente instrucción a ejecuta.
Función del PC:
Almacenar la Dirección de la Siguiente Instrucción: El PC contiene la dirección de memoria de la
próxima instrucción que el procesador debe ejecutar. Esto permite que el procesador sepa qué
instrucción ejecutar a continuación.
Secuenciación de Instrucciones: Después de ejecutar una instrucción, el PC se incrementa
automáticamente para apuntar a la siguiente instrucción en la secuencia del programa.
Control de Flujo: En caso de instrucciones de salto, llamadas a subrutinas o interrupciones, el PC
se actualiza para reflejar la nueva dirección de la instrucción que debe ejecutarse, permitiendo
cambios en el flujo de control del programa.
```
Importancia del Program Counter (PC)
```
Ejecución Secuencial: El PC asegura que las instrucciones se ejecuten en el orden correcto,
a menos que una instrucción de control de flujo indique lo contrario.
Manejo de Interrupciones: Durante una interrupción, el valor del PC se guarda para que el
procesador pueda retomar la ejecución correcta después de manejar la interrupción.
```
Eficiencia: Al mantener la dirección de la siguiente instrucción, el PC permite una ejecución
```
eficiente y continua del programa.
```
Ejemplo:
```
Cuando la CPU comienza a ejecutar un programa, el PC apunta a la primera instrucción.
A medida que se ejecuta esa instrucción, el PC se incrementa para apuntar a la siguiente.
Si el programa encuentra una instrucción de salto, el PC se actualiza para apuntar a la nueva
dirección donde se encuentra la instrucción de destino.
Tratamiento de interrupciones
Hardware
El controlador del dispositivo avisa de
una interrupción: Un dispositivo de
hardware genera una señal de
interrupción.
El procesador finaliza la ejecución de
la instrucción en curso: El procesador
termina la instrucción que está
ejecutando antes de atender la
interrupción.
El procesador acusa el recibo de la
interrupción: El procesador reconoce
la señal de interrupción.
Tratamiento de interrupciones
Software
Salvar el resto de la información de estado del proceso:
El sistema operativo guarda el estado actual del
```
proceso interrumpido (por ejemplo, registros y
```
```
variables).
```
Interrupción del proceso: El sistema operativo maneja la
interrupción, ejecutando el código necesario para
atenderla.
Restaurar la información de estado del proceso: Una vez
manejada la interrupción, el sistema operativo restaura
el estado del proceso interrumpido.
Restaurar los valores anteriores de PSW y PC: El
procesador recupera los valores anteriores del Program
```
Status Word (PSW) y el Program Counter (PC).
```
El procesador carga el nuevo valor del PC dependiendo
de la interrupción: El procesador ajusta el PC para
continuar la ejecución del proceso interrumpido.