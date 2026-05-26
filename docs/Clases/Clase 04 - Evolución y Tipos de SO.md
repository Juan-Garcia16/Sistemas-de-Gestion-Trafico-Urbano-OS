

Evolución y
Tipos de SO
## Ing. Juan Andrés García Moreno

Gestión de Recursos
Un computador es un conjunto de recursos que se utilizan para el transporte,
almacenamiento y procesamiento de los datos, así como para llevar a cabo el
control de estas funciones. El sistema operativo se encarga de gestionar estos
recursos.

Proceso de Gestión
1.El sistema operativo dirige al procesador en el uso de los otros recursos del sistema y en
la temporización de la ejecución de otros programas.
2.El sistema operativo deja el control para que el procesador pueda realizar trabajo «útil» y
de nuevo retoma el control para permitir al procesador que realice la siguiente pieza de
trabajo.
3.La asignación de este recurso (memoria principal) es controlada de forma conjunta por
el sistema operativo y el hardware de gestión de memoria del procesador.
4.El sistema operativo decide cuándo un programa en ejecución puede utilizar un
dispositivo de E/S y controla el acceso y uso de los ficheros.
5.El procesador es también un recurso, y el sistema operativo debe determinar cuánto
tiempo de procesador debe asignarse a la ejecución de un programa de usuario
particular.

Importancia de la Evolución de un SO
1.Actualizaciones de hardware más nuevos tipos de hardware: Permite
gestionar de manera eficiente la memoria.
2.Nuevos servicios: Nuevas herramientas de medida y control.
3.Resolución de fallos: Cualquier sistema falla, esto se descubre con el tiempo
se soluciona e introduce nuevos fallos.

La Evolución de los Sistemas Operativos
Los Sistemas Operativos se deben adaptar a medida que el tiempo pasa.
¿Esto sucede por qué razón?

Línea del Tiempo de la Evolución de un SO
-Procesamiento en Serie.
-Sistemas en Lotes Sencillos.
-Sistemas en Lotes Multiprogramados.
-Sistemas de Tiempos Compartidos.

- Procesamiento en Serie
•Finales de los años 40 hasta mediados de los
años 50.
•No existía ningún sistema operativo.
•Estas máquinas eran utilizadas desde una
consola que contenía luces, interruptores,
algún dispositivo de entrada y una impresora.
•Si un error provocaba la parada del programa,
las luces indicaban la condición de error.
•Si el programa terminaba de manera normal,
la salida aparecía en la impresora.

Características del Procesamiento en Serie
En este modelo, las tareas o trabajos se ejecutaban uno tras otro, sin ninguna forma
de paralelismo o multitarea.
Características del Procesamiento en Serie:
1.Ejecuta un Trabajo a la Vez: No se permite la ejecución simultánea de múltiples
tareas, por lo que cada programa debe esperar hasta que el trabajo anterior se haya
completado.
2.Secuencia Fija: Los trabajos se procesan en el orden en que llegan o en un orden
predefinido.
3.Baja Utilización de Recursos: Si un trabajo necesita esperar (por ejemplo, esperando
una operación de E/S), la CPU queda inactiva durante ese tiempo.
4.Falta de Interactividad:Una vez que un trabajo se ponía en la cola para su
procesamiento, no había forma de detenerlo, no había interrupciones.

Funcionamiento Básico del Procesamiento en
## Serie
Carga del Trabajo: El operador de la computadora cargaba un trabajo en la memoria del
sistema desde un dispositivo de entrada, como una cinta o tarjetas perforadas.
Ejecución del Trabajo:La CPU comenzaba a ejecutar las instrucciones del programa
cargado. El trabajo se ejecutaba en su totalidad antes de que cualquier otro programa
pudiera comenzar.
Salida de Resultados:Una vez finalizado el trabajo, los resultados se enviaban a un
dispositivo de salida, como una impresora o una cinta magnética.
Carga del Siguiente Trabajo: Después de completar un trabajo, el sistema se preparaba
para cargar y ejecutar el siguiente trabajo en la cola. Este proceso continuaba hasta que se
procesaban todos los trabajos en la lista.

## Problemas Principales
Planificación: un usuario podía solicitar un bloque de tiempo en múltiplos de
media hora aproximadamente. Si el proceso terminaba en 45 minutos, el resto del
tiempo se perdía.
Tiempo de configuración: Si ocurría un error, el usuario tenía que volver al
comienzo de la secuencia de configuración.

Transición a Modelos Más Avanzados
El procesamiento en serie fue eventualmente reemplazado por sistemas de
procesamiento en batch(lotes), multitareay multiprogramación,que permitieron
que varios trabajos se ejecutaran concurrentemente, mejorando así la utilización de
los recursos del sistema y reduciendo los tiempos de espera para los usuarios.

- Sistemas en Lotes Sencillos
(Batchsencillo)
Las primeras máquinas eran muy caras, era importante maximizar su utilización. El
tiempo malgastado en la planificación y configuración de los trabajos era
inaceptable.
En los años 50 se desarrolló el concepto de sistema operativo en lotes, fue el primer
SO y se desarrolló por General Motors para el uso de la IBM 701 y mejorado para la
IBM 704 por otros clientes de IBM.
Idea central Monitor, el usuario enviaba el trabajo a través de una cinta o tarjeta
perforada creando las tareas por lotes, Noaccedía directamente a la máquina.
Cuando la máquina finalizaba devolvía el control al Monitor.
Su funcionamiento se puede analizar desde dos enfoques: Monitor y Procesador.

## Monitor
Se ejecuta en modo núcleo y controla la secuencia de eventos, gran parte del
monitor debe estar cargada en la memoria principal y disponible para ejecución.
Esta parte se denomina Monitor Residente. El resto del monitor está formado por
un conjunto de utilidades y funciones comunes que se cargan como subrutinas en
el programa de usuario, al comienzo de cualquier trabajo que las requiera.

Punto de vista del Monitor
1.Lee uno por uno la cola de trabajos desde el
dispositivo de entrada.
2.Luego, el trabajo se coloca en el área del
usuario y se pasa el control.
3.Al terminar, el control vuelve al Monitor, y lee
el siguiente trabajo.
4.Envía los resultados a un dispositivo de salida.
El monitor realiza una función de planificación: en
una cola se sitúa un lote de trabajos, y los trabajos
se ejecutan lo más rápidamente posible, sin
ninguna clase de tiempo ocioso entre medias.

Punto de vista del Procesador
Ejecuta instrucciones de la zona de memoria principal que contiene el monitor.
1.Estas instrucciones provocan que se lea el siguiente trabajo y se almacene en otra
zona de memoria principal.
2.El procesador encontrará una instrucción de salto en el monitor que le indica al
procesador que continúe la ejecución al inicio del programa de usuario.
3.Se ejecuta hasta que encuentre condición de parada o error.

## Job Control Language
Con cada uno de los trabajos, se incluye un conjunto de
instrucciones en algún formato primitivo de lenguaje de
control de trabajos (Job Control Language, JCL).
Se trata de un tipo especial de lenguaje de programación
utilizado para dotar de instrucciones al monitor.

Características adicionales del Hardware
El monitor, o sistema operativo en lotes, confía en la habilidad del procesador para cargar
instrucciones de diferentes porciones de la memoria principal que de forma alternativa le
permiten tomar y abandonar el control.
•Protección de memoria: Durante la ejecución del programa de usuario, éste no debe
alterar el área de memoria que contiene el monitor. Si esto ocurriera, el hardware del
procesador debe detectar un error y transferir el control al monitor.
•Temporizador: Se utiliza un temporizador para evitar que un único trabajo monopolice el
sistema. Se activa el temporizador al comienzo de cada trabajo. Si el temporizador expira,
se para el programa de usuario, y se devuelve el control al monitor.
•Instrucciones privilegiadas: Ciertas instrucciones a nivel de máquina se denominan
privilegiadas y sólo las puede ejecutar el monitor. Si el procesador encuentra estas
instrucciones mientras ejecuta un programa de usuario, se produce un error provocando
que el control se transfiera al monitor.

Implicaciones de un SO en Lotes
Con un sistema operativo en lotes, el tiempo de máquina alterna la ejecución
de programas de usuario y la ejecución del monitor. Esto implica dos
sacrificios:
1.El monitor utiliza parte de la memoria principal.
2.Consume parte del tiempo de máquina.
Ambas situaciones implican una sobrecarga. A pesar de esta sobrecarga, el
sistema en lotes simple mejora la utilización del computador.

Sistemas en Lotes Multiprogramados
El procesador se encuentra frecuentemente ocioso, incluso con el
orden secuencial de trabajos automático que proporciona un
sistema operativo en lotes simple. El problema consiste en que
los dispositivos de E/S son lentos comparados con el procesador.

Ejemplo del Funcionamiento de un Sistema
## Multiprogramado
En este ejemplo, el computador malgasta
aproximadamente el 96% de su tiempo esperando a que los
dispositivos de E/S terminen de transferir datos a y desde el
fichero.
Cálculo representativo de
este hecho, que corresponde
a un programa que procesa
un fichero con registros y
realiza de media 100
instrucciones máquina por
registro.

Ejemplo del Funcionamiento de un Sistema Multiprogramado
En monoprogramación el procesador ejecuta durante cierto tiempo hasta
que alcanza una instrucción de E/S. Entonces debe esperar que la
instrucción de E/S concluya antes de continuar.
Expansión de memoria

Atributos de
ejecución de
ejemplos de
programas.
Para tener varios trabajos listos para ejecutar, éstos deben guardarse en memoria principal,
requiriendo alguna forma de gestión de memoria.
Adicionalmente, si varios trabajos están listos para su ejecución, el procesador debe decidir cuál
de ellos ejecutar; esta decisión requiere un algoritmo para planificación.

## Sistemas De Tiempo Compartido
Cuando se presenta muchos trabajos en un procesamiento en lote, se genera la
necesidad de que el usuario tenga interacción con el computador como lo es
actualmente, esto surge después de los años 60.
En un sistema de tiempo compartido, la CPU se comparte entre varios usuarios al
asignar pequeños intervalos de tiempo llamados time slices o quantums a cada
tarea o proceso. Aunque cada usuario interactúa con el sistema como si tuviera el
control exclusivo de la máquina, en realidad, la CPU alterna rápidamente entre los
procesos de todos los usuarios, proporcionando la ilusión de que todos los
procesos se ejecutan simultáneamente.

Comparativa entre Multiprogramación y
## Tiempo Compartido
Ambos tipos de procesamiento, en lotes y tiempo compartido, utilizan multiprogramación, Del
mismo modo que la multiprogramación permite al procesador gestionar múltiples trabajos en
lotes en un determinado tiempo, la multiprogramación también se puede utilizar para gestionar
múltiples trabajos interactivos. En este último caso, la técnica se denomina tiempo compartido,
porque se comparte el tiempo de procesador entre múltiples usuarios.

## Características Principales
Multiprogramación y Multitarea: Múltiples programas o procesos están en memoria al mismo
tiempo. El sistema operativo alterna la ejecución de estos procesos, lo que permite que varios
usuarios interactúen con la computadora simultáneamente.
Interactividad: A diferencia de los sistemas en lotes, los sistemas de tiempo compartido permiten la
interacción directa y en tiempo real entre el usuario y el sistema. Los usuarios pueden enviar
comandos, recibir respuestas, y modificar el estado de sus procesos mientras están en ejecución.
Planificación de CPU: El sistema operativo utiliza un algoritmo de planificación para decidir qué
proceso debe ejecutarse en un momento dado.
Memoria Virtual: La introducción de la memoria virtual fue fundamental para los sistemas de tiempo
compartido, permitiendo que cada proceso tenga su propio espacio de direcciones virtuales, lo que
facilita la protección de los procesos entre sí y el uso eficiente de la memoria física.
Tiempo de Respuesta Rápido: Aunque cada proceso solo recibe una pequeña fracción del tiempo de
CPU, los sistemas de tiempo compartido están diseñados para minimizar el tiempo de espera entre
interacciones del usuario y la respuesta del sistema, dando la impresión de ejecución continua.

Funcionamiento de un SO de un Tiempo Compartido
Del mismo modo que la multiprogramación permite al procesador gestionar múltiples trabajos en lotes en un determinado
tiempo, la multiprogramación también se puede utilizar para gestionar múltiples trabajos interactivos. En este último caso,
la técnica se denomina tiempo compartido, porque se comparte el tiempo de procesador entre múltiples usuarios.
1.Multiprogramación:
Los programas de varios usuarios se cargan en la memoria principal. Cada usuario interactúa con el sistema a través
de terminales o consolas conectadas al sistema central.
2.Planificación de Procesos:
El sistema operativo divide el tiempo de CPU en intervalos cortos y los asigna a cada proceso de usuario en turnos
rotativos. Un proceso puede ejecutarse durante su intervalo de tiempo (quantum) y luego cede la CPU al siguiente
proceso en la cola.
3.Cambio de Contexto:
Cuando el tiempo asignado a un proceso termina o el proceso necesita esperar (por ejemplo, por una operación de
E/S), el sistema operativo guarda el estado del proceso (cambio de contexto) y carga el estado del siguiente proceso en
la cola para que continúe la ejecución.
4.Memoria Virtual y Protección:
La memoria virtual asegura que cada proceso tiene su propio espacio de direcciones, protegiendo los datos de cada
usuario de interferencias accidentales por parte de otros procesos.
5.Interacción en Tiempo Real:
Los usuarios pueden enviar comandos y recibir respuestas inmediatamente, lo que permite la edición de textos, la
ejecución de cálculos y otras tareas interactivas en tiempo real.

Ventajas de los Sistemas de Tiempo
## Compartido
1.Uso Eficiente de la CPU:
La CPU se utiliza de manera más eficiente, ya que siempre está ocupada ejecutando algún
proceso, reduciendo el tiempo de inactividad.
2.Interactividad:
Los usuarios pueden interactuar con el sistema en tiempo real, lo que es crucial para tareas
como la programación, la edición de texto, y el análisis de datos.
3.Accesibilidad Multipropósito:
Varios usuarios pueden usar la misma computadora central para diferentes tareas, lo que era
particularmente importante cuando el hardware era caro y escaso.
4.Protección entre Usuarios:
La memoria virtual y la planificación de procesos garantizan que los procesos de diferentes
usuarios no interfieran entre sí, aumentando la seguridad y la estabilidad del sistema.

Desventajas de los Sistemas de Tiempo
## Compartido
1.Sobrecarga del Sistema:
El constante cambio de contexto y la gestión de múltiples procesos pueden generar una
sobrecarga significativa en el sistema operativo, lo que puede ralentizar el rendimiento
general si no se gestiona correctamente.
2.Fragmentación de la Memoria:
La gestión de la memoria virtual puede llevar a la fragmentación, lo que puede degradar el
rendimiento si la memoria física se llena de pequeñas porciones no contiguas de espacio
libre.
3.Problemas de Escalabilidad:
A medida que aumenta el número de usuarios y procesos, el sistema puede volverse menos
eficiente si no está bien optimizado, ya que cada proceso recibe una fracción menor de
tiempo de CPU.

Principales Logros de lo SO
## • Procesos.
- Gestión de memoria.
- Protección y seguridad de la información.
- Planificación y gestión de los recursos.
- Estructura del sistema.