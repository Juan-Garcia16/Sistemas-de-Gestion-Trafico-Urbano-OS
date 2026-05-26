

Procesos II
Planificación, Sincronización y comunicación,
Semáforos, monitores, mensajes
## Ing. Juan Andrés García Moreno

Objetivos de la Planificación de Procesos
Maximizar la
utilización de la
CPU: Mantener la
CPU ocupada el
mayor tiempo
posible.
## 01
Maximizar el
rendimiento:
Aumentar el número
de procesos que se
completan en un
tiempo dado.
## 02
Minimizar el tiempo
de espera: Reducir
el tiempo que los
procesos pasan en la
cola de procesos
listos.
## 03
Minimizar el tiempo
de respuesta:
Reducir el tiempo
que tarda el sistema
en responder a una
solicitud.
## 04
## Equidad: Asegurar
que todos los
procesos reciban
una porción justa de
tiempo de CPU.
## 05

Conceptos Clave en la
Planificación de Procesos
•Proceso: Programa en ejecución que
necesita recursos (CPU, memoria, E/S)
para completar su tarea.
•Cola de procesos listos: Lista de
procesos en estado Listo, esperando
para ser ejecutados por la CPU.
•Cambio de contexto: Proceso en el cual
el sistema operativo guarda el estado de
un proceso y carga el estado de otro.

Planificación de Procesos
+La planificación de procesoses el
mecanismo mediante el cual un sistema
operativo decide cuál de los procesos
en estado Listodebe ejecutarse en un
momento dado.
+El objetivo es optimizar el uso del
procesador, mejorar el rendimiento
general del sistema y cumplir con ciertos
criterios, como el tiempo de respuesta,
rendimientoy equidad.

Planificación de Procesos
+En un sistema de un único procesador, sólo puede ejecutarse un
proceso cada vez; cualquier otro proceso tendrá que esperar hasta
que el CPU quede libre y pueda volver a planificarse. El objetivo de la
multiprogramación es tener siempre varios procesos en espera en la
memoria del sistema para maximizar el uso de la CPU.
+Con la multiprogramación, se intenta usar ese tiempo de forma
productiva. En este caso, se mantienen varios procesos en memoria y
cuando uno está esperando por E/S, otro puede estar utilizando el
procesador o estar listo para hacerlo

Ciclo de Ráfagas de CPU y E/S
+Cuando un proceso tiene que esperar, el sistema operativo retira ese
proceso del procesador y le cede el turno al siguiente en espera que esté
listo para continuar su ejecución en ese momento. Esto se repite
continuamente y cada vez que un proceso espera otro proceso puede
hacer uso de la CPU.
+El ciclo de ráfagas de CPU y E/Ses un modelo que describe
cómo los procesos alternan entre el uso de la CPUy la
entrada/salida (E/S)durante su ejecución.
+Los procesos no pasan todo su tiempo ejecutándose en la CPU; en
su lugar, realizan operaciones de E/S (como leer archivos, escribir
en disco, o esperar datos de red) y, entre estas operaciones,
ejecutan instrucciones en la CPU.

Clases de Ráfaga
+Ráfaga de CPU: Es un período de tiempo durante el cual un
proceso utiliza intensivamente la CPU para ejecutar
instrucciones sin realizar operaciones de E/S. En este tiempo,
el proceso realiza cálculos, manipula datos en la memoria,
etc.
+Ráfaga de E/S: Es un período de tiempo durante el cual el
proceso espera la finalización de una operación de E/S.
Durante este tiempo, el proceso está bloqueado y no puede
continuar hasta que la operación de E/S se complete.
## +

Ciclo de Ejecución
+Un proceso típico alterna entre ráfagas de CPU y ráfagas de E/S de
la siguiente manera:
1.Ráfaga de CPU: El proceso utiliza la CPU para realizar cálculos o ejecutar instrucciones.
2.Ráfaga de E/S:El proceso necesita realizar una operación de entrada/salida, como leer un
archivo o esperar datos de la red. Durante esta etapa, el proceso está en estado de espera,
esperando que se complete la operación de E/S.
3.Ráfaga de CPU:Una vez que se completa la operación de E/S, el proceso vuelve a utilizar la
CPU para continuar su ejecución.
+Este ciclo se repite hasta que el proceso termina.

Características del Ciclo de Ráfagas de
CPU y E/S
1.Procesos con ráfagas de CPU largas:Son aquellos que pasan la mayor
parte de su tiempo realizando cálculos en la CPU. Ejemplos incluyen
simulaciones científicas o procesamiento de imágenes.
2.Procesos con ráfagas de E/S largas:Son aquellos que dependen
principalmente de las operaciones de E/S y pasan mucho tiempo esperando
que estas operaciones se completen. Ejemplos incluyen aplicaciones que
dependen de la lectura/escritura en disco o la recepción de datos de una red.

Ejemplo de Ciclo de Ráfagas
+Se tiene que un proceso que realiza los
siguientes pasos:
1.El proceso comienza a ejecutar en la
CPU y realiza cálculos (ráfaga de CPU).
2.Luego, necesita leer datos de un
archivo, por lo que solicita una
operación de lectura (ráfaga de E/S).
3.Mientras espera los datos, el proceso no
puede continuar y la CPU se asigna a
otro proceso.
4.Una vez que los datos son leídos, el
proceso vuelve a la CPU para procesar
los datos leídos (otra ráfaga de CPU).

Algoritmos de
## Planificación

Implicaciones en la Planificación de
## Procesos
+El ciclo de ráfagas de CPU y E/S afecta la planificación de
procesos de varias maneras:
Procesos dependientes de la CPU:Los algoritmos de planificación
deben garantizar que estos procesos, que pasan mucho tiempo en
ráfagas de CPU, no monopolicen la CPU.
Procesos dependientes de E/S:Estos procesos pasan mucho tiempo en
espera de operaciones de E/S, por lo que es crucial que, cuando estén
listos, se les asigne rápidamente la CPU para minimizar los tiempos de
espera.

Tipos de Planificación de Procesos
+Existen dos tipos principales de planificación de procesos:
1.Planificación no expropiativa(Non-PreemptiveScheduling):
1.Una vez que un proceso obtiene la CPU, la retiene hasta que termine su ejecución o pase a estado de espera.
2.Ventaja: Simple de implementar y predecible.
3.Desventaja: Puede causar problemas como la inanicióno el bloqueodel sistema si un proceso de larga
duración monopoliza la CPU.
2.Planificación expropiativa(PreemptiveScheduling):
1.La CPU puede ser retirada de un proceso en ejecución si llega un proceso con mayor prioridad o si el tiempo
asignado ha expirado (cuota de tiempo).
2.Ventaja: Mejora la interactividaddel sistema y reduce el tiempo de respuesta.
3.Desventaja: Introduce una mayor sobrecarga debido a los cambios de contexto.

## Despachador
+El despachador es el módulo que implica el control del ciclo de la
CPU al proceso seleccionado por el planificador a corto plazo. Esta
función implica lo siguiente:
•Cambio de contexto.
•Cambio al modo usuario.
•Salto a la posición correcta dentro del programa de usuario para reiniciar dicho programa.
+El despachador debe ser lo más rápido posible, ya que se invoca en
cada cambio de proceso. El tiempo que tarda el despachador en
detener un proceso e iniciar la ejecución de otro se conoce como
latencia de despacho.

Criterios de
## Planificación
+Los diferentes algoritmos
de planificación de la
CPU tienen distintas
propiedades, y la
elección de un algoritmo
de planificación debe
cumplir ciertos criterios

Colas de Planificación
+Cuando los procesos ingresan al sistema, se añaden a una cola de
trabajosque incluye todos los procesos del sistema. Aquellos
procesos que se encuentran en la memoria principal y están listos y
esperando para ejecutarse se mantienen en una lista llamada cola de
procesos preparados.
+LaCola de Planificaciónse almacena en forma de lista enlazada La
cabecera de la cola de procesos preparados contiene punteros al
primer y último bloques de control de procesos (PCB) de la lista.

Gestión de Colas en el Sistema
•Colas del Sistema: Además de la cola de procesos en espera, el sistema
maneja varias otras colas.
•Asignación de CPU: Cuando un proceso recibe la CPU, puede:
•Ejecutarse
•Ser interrumpido
•Esperar un evento (como la finalización de una solicitud de E/S)
•Solicitudes de E/S:
•Si un proceso solicita E/S a un dispositivo compartido (por ejemplo, un disco) y este está
ocupado, el proceso debe esperar.
•La lista de procesos esperando por un dispositivo específico de E/S se llamacola del
dispositivo.
•Cada dispositivo tiene su propia cola.

Cola de procesos
preparados y diversas
colas de dispositivos
de E/S

Diagrama de
colas para la
planificación de
procesos

## Planificadores
+Planificador a largo plazo: Selecciona procesos de una cola de almacenamiento masivo (como
un disco) y los carga en memoria para su ejecución. Controla el grado de multiprogramación,
asegurando un equilibrio entre procesos limitados por la CPU y procesos limitados por la E/S. Su
ejecución es poco frecuente y busca optimizar la mezcla de procesos.
+Planificador a corto plazo: Selecciona los procesos que están listos para ejecutarse en la CPU.
Se ejecuta frecuentemente, ya que un proceso puede usar la CPU por solo unos milisegundos
antes de esperar por E/S. Debe ser muy rápido para no desperdiciar demasiado tiempo en la
planificación.
+Planificador a medio plazo: Realiza el intercambio(swap) de procesos, es decir, puede sacar
procesos de la memoria temporalmente para reducir la competencia por la CPU y volver a
cargarlos más tarde. Esto ayuda a manejar la memoria disponible y mantener un equilibrio en el
sistema.

Cambio de Contexto
+El cambio de contexto ocurre cuando la CPU interrumpe su tarea
actual para ejecutar una rutina del kernel. Durante este proceso, el
sistema operativo guarda el contexto del proceso en ejecución
(registros, estado del proceso y gestión de memoria) en el PCB
(ProcessControl Block). Luego, restaura el contexto del nuevo
proceso a ejecutar. Aunque necesario para gestionar múltiples
procesos, este cambio no produce trabajo útil. Su velocidad
depende del hardwarey de la complejidad del sistema operativo.

Cambio de Contexto
+El cambio de contexto ocurre cuando la CPU interrumpe su tarea
actual para ejecutar una rutina del kernel. Durante este proceso, el
sistema operativo guarda el contexto del proceso en ejecución
(registros, estado del proceso y gestión de memoria) en el PCB
(ProcessControl Block). Luego, restaura el contexto del nuevo
proceso a ejecutar. Aunque necesario para gestionar múltiples
procesos, este cambio no produce trabajo útil. Su velocidad
depende del hardwarey de la complejidad del sistema operativo.

Mecanismos de
## Planificación
1.Entrada del Intercambio: Indica el inicio del proceso de
cambio de contexto.
2.Procesos Intercambiados Parcialmente Ejecutados:
Representa los procesos que han sido interrumpidos y
están en espera de ser reanudados.
3.Salida del Intercambio: Marca el final del proceso de
cambio de contexto.
4.Cola de Preparadas: Lista de procesos que están listos
para ejecutarse.
5.Colas de Espera de E/S: Procesos que están esperando
la finalización de operaciones de entrada/salida.

Comunicación en Interprocesos
+La comunicación interprocesos (IPC)es el mecanismo que permite a los
procesos en un sistema operativo compartir datos e interactuar entre
ellos. Este mecanismo es fundamental cuando los procesos son
cooperativos, es decir, cuando pueden verse afectados o afectar a otros
procesos mediante la cooperación. Existen dos principales modelos de
comunicación interprocesos:
1.Memoria compartida
2.Paso de mensajes

## 1. Memoria Compartida
+En este modelo, se asigna una región de la memoria que puede
ser accedida por varios procesos. Los procesos cooperativos
pueden leer y escribir datos en esta zona de memoria para
intercambiar información de manera eficiente.
•Ventajas:
•Alta velocidad, ya que la comunicación ocurre directamente en la memoria, sin
intervención constante del sistema operativo.
•Menos consumo de recursos del sistema, pues una vez establecida la memoria
compartida, los accesos se tratan como accesos normales a la memoria.
•Desventajas:
•Requiere mecanismos de sincronización para evitar conflictos de acceso
concurrente a los mismos datos (por ejemplo, mediante semáforos o mutex).

## Ejemplo Memoria Compartida
+Un ejemplo de uso de memoria compartidaen un
sistema operativo sería en una aplicación de
procesamiento paralelo, donde múltiples procesos
necesitan acceder y modificar los mismos datos al
mismo tiempo.

- Paso de mensajes
+En este modelo, los procesos se comunican enviando y recibiendo mensajes a
través del sistema operativo. Los mensajes pueden ser de diferentes tamaños y
estructuras, y se envían a través de canales de comunicación que el sistema
operativo gestiona.
•Ventajas:
•Es más sencillo de implementar, especialmente en sistemas distribuidos o cuando los procesos no
comparten la misma memoria.
•No requiere mecanismos complejos de sincronización, ya que los procesos no acceden
simultáneamente a la misma zona de memoria.
•Desventajas:
•Menor rendimiento en comparación con la memoria compartida, ya que el envío y recepción de
mensajes requiere intervención del kernel.
•Más adecuado para pequeñas cantidades de datos o comunicaciones en sistemas distribuidos.

Sincronización de Procesos
+La comunicación entre procesos (IPC) se realiza mediante las
primitivas send() y receive(). Estas primitivas pueden
implementarse de diferentes maneras, utilizando mecanismos de
bloqueo (síncrono) o sin bloqueo (asíncrono):
+Envío con bloqueo: El proceso que envía se bloquea hasta que el receptor o el
buzón de correo reciben el mensaje.
+Envío sin bloqueo: El proceso que envía continúa operando después de enviar el
mensaje.
+Recepción con bloqueo: El receptor se bloquea hasta que hay un mensaje
disponible.
+Recepción sin bloqueo: El receptor extrae un mensaje válido o un mensaje nulo si
no hay mensajes disponibles.

Problemas sin sincronización
adecuada
+Condiciones de carrera (RaceCondition): Ocurre cuando varios procesos o hilos acceden
y modifican datos compartidos de manera concurrente, y el resultado depende del orden de
ejecución.
+Ejemplo: Dos procesos intentan incrementar el valor de una variable compartida al mismo
tiempo. Si uno de ellos lee el valor y lo incrementa antes de que el otro lo modifique, el valor
final será incorrecto.
+Inconsistencia de datos: Si los procesos acceden a recursos compartidos sin un control
adecuado, pueden generar datos inconsistentes o inválidos.
+Interbloqueo (Deadlock): Ocurre cuando dos o más procesos esperan indefinidamente por
un recurso que está siendo utilizado por otro proceso, y ninguno puede continuar.

Mecanismos comunes de
sincronización
1.Semáforos
2.Mutex(Mutual Exclusion)
3.Monitores
4.Variables de condición
5.Barriers(Barreras)

El Problema de la Sección Crítica
+El problema de la sección crítica se refiere a
la necesidad de diseñar un protocolo que
permita a los procesos cooperar de manera
que solo un proceso pueda ejecutar su
sección crítica a la vez.
+Una sección crítica es un segmento de
código donde un proceso puede modificar
variables comunes, actualizar tablas, escribir
en archivos, etc.
+La clave es que, mientras un proceso está
en su sección crítica, ningún otro proceso
puede estar en la suya.
Estructura de un Proceso
Un proceso típico tiene la siguiente estructura:
1.Sección de Entrada: Código que solicita
permiso para entrar en la sección crítica.
2.Sección Crítica: Código donde se
realizan operaciones que no deben ser
interrumpidas.
3.Sección de Salida: Código que se
ejecuta al salir de la sección crítica.
4.Sección Restante: Código que no
pertenece a las secciones anteriores.

Requisitos para Solucionar el Problema
+Cualquier solución al problema de la sección crítica debe cumplir con
los siguientes tres requisitos:
1.Exclusión Mutua: Si un proceso está en su sección crítica, ningún otro proceso puede
estar en la suya.
2.Progreso: Si ningún proceso está en su sección crítica y algunos desean entrar, solo
los procesos que no están en sus secciones restantes pueden participar en la
decisión de quién entra a la sección crítica. Esta decisión no debe posponerse
indefinidamente.
3.Espera Limitada: Existe un límite en el número de veces que otros procesos pueden
entrar en sus secciones críticas después de que un proceso haya solicitado entrar en
la suya y antes de que se le conceda el acceso

Condiciones de Carrera
+Las condiciones de carrera ocurren cuando múltiples procesos
acceden y modifican datos compartidos simultáneamente, lo
que puede llevar a resultados inconsistentes. Por ejemplo, si
dos procesos abren archivos simultáneamente, las
actualizaciones a la lista de archivos abiertos pueden causar
errores.

Solución al problema de la sección
Critica: Algoritmos de Peterson
+Lasolución de Petersones un algoritmo de programación
concurrente diseñado para resolver el problema de la exclusión
mutua, permitiendo que dos o más procesos compartan un recurso
sin conflictos.
+Funcionamiento del Algoritmo de Peterson
+El algoritmo utiliza dos variables compartidas:
•bandera: Un array de booleanos que indica si un proceso desea entrar
en la sección crítica.
•turno: Una variable que indica cuál proceso tiene el turno para entrar
en la sección crítica.

Propiedades del Algoritmo de Peterson
1.Exclusión Mutua: Garantiza que solo un proceso puede estar en la
sección crítica a la vez.
2.Progreso: Si ningún proceso está en la sección crítica, el proceso que
desea entrar puede hacerlo sin esperar indefinidamente.
3.Espera Limitada: Un proceso no puede ser bloqueado
indefinidamente si desea entrar en la sección crítica.
+Ventajas y Limitaciones
•Ventajas: Es simple y no requiere hardware especial.
•Limitaciones: Funciona eficientemente solo para dos procesos.

## SEMÁFOROS
+Los semáforos son mecanismos utilizados en sistemas
operativos y lenguajes de programación para gestionar la
concurrencia. Fueron introducidos por Edsger Dijkstra en 1965
como una solución para la cooperación entre procesos
secuenciales. Los semáforos permiten que dos o más procesos
cooperen mediante señales, deteniendo un proceso hasta que
reciba una señal específica.

Funcionamiento de los Semáforos
+Los semáforos son variables especiales que permiten la
señalización entre procesos. Existen dos primitivas principales
para trabajar con semáforos:
•signal(s): Transmite una señal.
•wait(s): Recibe una señal. Si la señal no ha sido transmitida, el proceso se
suspende hasta que la señal esté disponible.

Operaciones Básicas de los Semáforos
+Los semáforos se pueden considerar como variables enteras con
tres operaciones principales:
1.Inicialización: Un semáforo puede inicializarse con un valor no negativo.
2.wait(): Decrementa el valor del semáforo. Si el valor se vuelve negativo, el
proceso se bloquea.
3.signal(): Incrementa el valor del semáforo. Si el valor no es positivo, se
desbloquea un proceso bloqueado por una operación wait().
+Estas operaciones son atómicas, es decir, no pueden ser
interrumpidas y se consideran indivisibles.

Tipos Principales de Semáforos
+Existen dos tipos principales:
•Semáforos binarios (también conocidos como mutex): Solo pueden
tomar los valores 0 o 1, y se usan para permitir o denegar el acceso a
un recurso.
•Semáforos contadores: Pueden tener cualquier valor entero, y
permiten la gestión de acceso a múltiples recursos del mismo tipo.