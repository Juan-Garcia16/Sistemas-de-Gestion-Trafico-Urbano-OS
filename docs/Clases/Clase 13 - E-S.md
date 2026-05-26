

Sistemas de E/S
## Ing. Juan Andrés García Moreno

¿Qué son los Sistemas de Entrada/Salida (E/S)?
•Los sistemas de Entrada/Salida (E/S)son un conjunto de
mecanismos y estructuras que permiten la comunicación entre el
sistema operativoy los dispositivos periféricosexternos, como
discos duros, impresoras, teclados, y dispositivos de red. Los
sistemas de E/S se encargan de transferir datos desde y hacia el
sistema, garantizando que los dispositivos funcionen de manera
coordinada y eficiente sin interferir entre sí.

Importancia de los Sistemas de E/S en un
## Sistema Operativo
1.Interacción con Dispositivos Periféricos: Los sistemas de E/S permiten que el sistema
operativo se comunique con dispositivos periféricos de todo tipo, gestionando las diferencias de
velocidad, tamaño de datos y métodos de comunicación entre el CPU y los dispositivos.
2.Gestión de Recursos y Rendimiento: La E/S afecta directamente al rendimiento del sistema. Un
sistema operativo optimiza el uso de la CPU mediante técnicas de E/S, evitando que el
procesador quede inactivo mientras espera que se completen operaciones de entrada o salida.
3.Multiprogramación: En sistemas multitarea, varios programas pueden requerir E/S
simultáneamente. Los sistemas de E/S permiten que múltiples aplicaciones usen dispositivos sin
interferencias, mediante mecanismos de cola y planificación que optimizan el uso de cada
dispositivo.

Componentes del Sistema de E/S
1.Controladores de Dispositivos: Los controladores son programas específicos que actúan como
intermediarios entre el sistema operativo y los dispositivos de hardware. Cada dispositivo tiene
su propio controlador, que traduce las solicitudes del sistema operativo en instrucciones
específicas que el dispositivo entiende.
2.Módulos del Kernel: En el núcleo del sistema operativo, los módulos de E/S del kernelmanejan
la planificación, el almacenamiento en búfer y la protección de los dispositivos. Estos módulos
también supervisan los errores y gestionan las colas de solicitudes de E/S.
3.Interfaces de Usuario y Aplicaciones: Las aplicaciones utilizan la E/S para interactuar con el
sistema operativo a través de llamadas al sistema, solicitando datos de dispositivos o enviando
datos hacia ellos. Estas interfaces permiten que las aplicaciones se comuniquen con la E/S sin
conocer los detalles técnicos de los dispositivos.

Hardware de E/S
•Los dispositivos se comunican con los sistemas informáticos
enviando señales a través de un “cable o incluso a través del
aire. Cada dispositivo se comunica con la máquina a través de
un punto de conexión (o puerto), como por ejemplo un
puerto serie. Si los dispositivos utilizan un conjunto común de
hilos, dicha conexión se denomina bus.



¿Cómo puede proporcionar comandos y datos el
procesador a una controladora para llevar a
cabo una transferencia de E/S?
•El procesador puede proporcionar comandos y datos a una
controladora de E/S para llevar a cabo una transferencia de
E/S mediante varios métodos, cada uno diseñado para
maximizar la eficiencia y el rendimiento de los sistemas
operativos. Los métodos principales para esto son:
1.Sondeo o Programmed I/O (P-I/O)
2.Interrupciones
3.Acceso Directo a Memoria (DMA)
4.MapeodeE/SenMemoria(Memory-mappedI/O)

1.Sondeo o Programmed I/O (P-I/O)
•En el método de sondeo, el procesador controla y verifica directamente
el estado del dispositivo de E/S mediante la consulta periódica
(sondeo) de sus registros de estado. Una vez que el dispositivo está listo,
el procesador puede enviarle comandos y datos.
•Proceso: El CPU ejecuta un ciclo continuo de lectura de los registros de la
controladora de E/S hasta que detecta que el dispositivo está listo. Luego, envía el
comando y/o los datos necesarios.
•Desventajas: Este método consume muchos recursos de CPU, ya que el
procesador debe esperar activamente hasta que el dispositivo esté disponible.
Ejemplo: Es común en dispositivos de E/S antiguos o simples, como
teclados y algunos controladores de impresoras básicos.

2.Interrupciones
•En el método basado en interrupciones, la controladora de E/S notifica al
procesador cuando está lista para recibir o enviar datos. Este método permite
que el procesador ejecute otras tareas mientras espera que el dispositivo esté
listo.
•Proceso:
•El CPU envía un comando a la controladora para iniciar una operación de E/S.
•La controladora lleva a cabo la operación y, cuando está lista o ha terminado, genera una interrupción.
•El procesador pausa su ejecución actual y responde a la interrupción, enviando los datos o comandos
necesarios.
•Ventajas: El CPU puede realizar otras tareas mientras espera la interrupción,
mejorando la eficiencia.
Ejemplo: Las impresoras y los discos duros modernos suelen utilizar
interrupciones para notificar al CPU que han terminado una operación de E/S y
que están listas para otra.

3.Acceso Directo a Memoria (DMA)
•El DMA permite que un dispositivo de E/S transfiera datos directamente
a la memoria principal sin la intervención constante del procesador, lo
que ahorra tiempo y recursos de CPU.
•Proceso:
•El CPU envía un comando a la controladora de DMA con las direcciones de memoria y los
datos a transferir.
•La controladora de DMA gestiona la transferencia de datos entre el dispositivo de E/S y la
memoria, mientras que el procesador realiza otras tareas.
•Al finalizar la transferencia, la controladora de DMA envía una interrupción al procesador
para notificar que la operación ha concluido.
•Ventajas: Ideal para grandes cantidades de datos, ya que permite que
el CPU se libere del proceso de transferencia, mejorando el rendimiento
general del sistema.
•Ejemplo: Las tarjetas de red y las tarjetas gráficas usan DMA para
transferir datos masivos, como videos y datos de red, directamente a la
memoria.

4.Mapeode E/S enMemoria (Memory-mappedI/O)
•En el mapeo de E/S en memoria, los registros de control y datos del dispositivo se
asignan a direcciones específicas en el espacio de memoria del procesador. Esto
permite que el CPU acceda a los dispositivos de E/S utilizando las mismas
instrucciones que usa para acceder a la memoria.
•Proceso:
•Se asignan direcciones de memoria específicas a los registros de control y datos
de los dispositivos de E/S.
•El CPU lee y escribe en estas direcciones para enviar comandos o recibir datos de
los dispositivos.
•Ventajas: Simplifica la comunicación entre CPU y dispositivos, permitiendo que el CPU
use el mismo conjunto de instrucciones para E/S y memoria.
•Ejemplo: Es utilizado en muchas arquitecturas de procesadores modernos, donde
dispositivos como tarjetas de sonido y de red están mapeados en el espacio de
direcciones de memoria.

Interfaz de E/S de las Aplicaciones
•La Interfaz de E/S de las aplicaciones es el conjunto de
mecanismos y funciones que el sistema operativo proporciona
a las aplicaciones para interactuar con dispositivos de
entrada/salida (E/S), como discos duros, impresoras, teclados,
pantallas y dispositivos de red.
•Este sistema permite a las aplicaciones acceder a los recursos
de E/S sin necesidad de conocer los detalles técnicos de cada
dispositivo, proporcionando una abstracción que facilita la
programación y mejora la seguridad del sistema.

Componentes Clave de la Interfaz de E/S
1.Tipos de Dispositivos de E/S
2.Modos de Operación de E/S
3.Llamadas del Sistema para E/S
4.Almacenamiento en Búfer y Almacenamiento en Caché
5.Control de Acceso y Seguridad en E/S

1.Tipos de Dispositivos de E/S
•Los dispositivos de E/S se clasifican en función de la forma en
que manejan los datos y en cómo permiten el acceso a estos:
a.Dispositivos de Bloques
b.Dispositivos de Caracteres
c.Dispositivos de Red
d.Relojes y Temporizadores

a.Dispositivos de Bloques
•Estos dispositivos manejan datos en bloques de tamaño fijo, lo
que permite un acceso aleatorio (es decir, los datos pueden leerse
o escribirse en cualquier orden).
•Ejemplos: Discos duros, SSDs y unidades USB.
•Uso en sistemas modernos: En sistemas de archivos y bases de
datos, los dispositivos de bloques se acceden mediante
instrucciones que permiten leer y escribir datos en bloques
específicos, mejorando el rendimiento en aplicaciones que
requieren acceso aleatorio.

b.Dispositivos de Caracteres
•Estos dispositivos manejan datos en un flujo continuo de
caracteres (bytes) y solo permiten acceso secuencial.
•Ejemplos: Teclados, ratones y ciertos dispositivos de comunicación
serie.
•Uso en sistemas modernos: Estos dispositivos son ideales
para aplicaciones que procesan flujos de datos secuenciales,
como la lectura de un teclado o la salida de texto en una
impresora.

c.Dispositivos de Red
•Los dispositivos de red manejan datos en paquetes y requieren
una interfaz de E/S especializada para gestionar el tráfico de red.
•Ejemplos: Tarjetas de red Ethernet, Wi-Fi y dispositivos de comunicación
en redes.
•Uso en sistemas modernos: Estos dispositivos son cruciales en
aplicaciones cliente-servidor, servicios web y entornos de alta
concurrencia, donde se utilizan técnicas avanzadas como el
buffering y el manejo de interrupciones para gestionar múltiples
conexiones simultáneamente.

d.Relojes y Temporizadores
•Relojes y temporizadores son dispositivos especiales que
permiten a las aplicaciones medir y gestionar el tiempo.
•Ejemplos: Relojes del sistema y temporizadores de software.
•Uso en sistemas modernos: Son esenciales para tareas
programadas, eventos de tiempo real, y en sistemas de
control en los que es fundamental la precisión del tiempo.

2.Modos de Operación de E/S
•La E/S bloqueante y no bloqueante son dos modos de
operación que determinan cómo se comporta un proceso
cuando realiza una operación de entrada/salida.
a.E/S Bloqueante
b.E/S No Bloqueante
c.E/S Asincrónica

a.E/S Bloqueante
•En el modo de E/S bloqueante, una aplicación que realiza una
operación de E/S se detiene (bloquea) hasta que la operación de
entrada/salida se complete. Esto asegura que los datos estén
disponibles antes de que la aplicación continúe ejecutándose.
•Ejemplo: La lectura de un archivo desde el disco en modo bloqueante
garantiza que el archivo completo esté disponible antes de que el
programa prosiga.
•Ventaja: Simplicidad en la programación.
•Desventaja: Puede reducir la eficiencia en aplicaciones que
requieren alta velocidad, ya que el proceso queda inactivo
esperando el resultado de la operación.

b.E/S No Bloqueante
•En la E/S no bloqueante, la aplicación puede continuar
ejecutándose mientras espera que se complete la operación
de entrada/salida. Esto es ideal para aplicaciones multitarea y
en sistemas de alto rendimiento.
•Ejemplo: En servidores web, el manejo de solicitudes de red se
realiza de forma no bloqueante, lo cual permite gestionar múltiples
conexiones sin detener el flujo de ejecución.
•Ventaja: Mejora la eficiencia en sistemas multitarea.
•Desventaja: La programación puede ser más compleja, ya
que el sistema debe manejar los eventos asincrónicos para
saber cuándo la E/S está lista.

c.E/S Asincrónica
•En la E/S asincrónica, la aplicación envía una solicitud de E/S y
el sistema operativo notifica al proceso cuando la operación
ha finalizado, sin necesidad de que la aplicación esté
pendiente de su estado.
•Ejemplo: Una aplicación de reproducción de video puede solicitar
datos de E/S asincrónicos para cargar las siguientes partes del video
sin detener la reproducción.
•Uso en sistemas modernos: La E/S asincrónica es
ampliamente usada en aplicaciones que requieren gran
rendimiento, como videojuegos, aplicaciones de
procesamiento en tiempo real y sistemas de bases de datos.

3.Llamadas del Sistema para E/S
•Las llamadas del sistema para E/S son funciones que el sistema
operativo proporciona a las aplicaciones para interactuar con los
dispositivos de entrada y salida de manera controlada y segura.
•Estas llamadas permiten que las aplicaciones realicen operaciones
de E/S (como leer o escribir en un archivo, o comunicarse con un
dispositivo de red) sin necesidad de acceder directamente al
hardware, protegiendo así el sistema de errores y fallos de
seguridad.
•Las llamadas de sistema para E/S actúan como un puente entre el
software y el hardware, proporcionando una interfaz estándar
que permite a las aplicaciones manipular archivos, dispositivos y
otros recursos de E/S mediante comandos de alto nivel.

3a. Principales Llamadas del Sistema para E/S
1.open(): Abre un archivo o dispositivo
oLa llamada open() permite a una aplicación abrir un archivo o dispositivo específico para comenzar
a interactuar con él. Este comando recibe como parámetros la ruta del archivo o dispositivo y el
modo en el que se desea abrir (lectura, escritura o ambos).
oEjemplo: En un sistema Unix/Linux, open("/home/usuario/documento.txt", O_RDONLY) abre el
archivo en modo de solo lectura.
2.read(): Lee datos de un archivo o dispositivo
oLa llamada read() permite a una aplicación leer datos de un archivo o dispositivo que previamente
se abrió. El sistema operativo lee los datos desde el archivo o dispositivo en un búfer y luego los
transfiere a la aplicación.
oEjemplo: read(fd, buffer, size) lee una cantidad específica de datos desde un archivo o dispositivo
identificado por fd (file descriptor) y los almacena en el buffer.

3b. Principales Llamadas del Sistema para E/S
3.write(): Escribe datos en un archivo o dispositivo
oLa llamada write() permite a una aplicación escribir datos en un archivo o dispositivo. Es
comúnmente usada para enviar datos a una impresora, escribir en un archivo de texto o
enviar datos a una red.
oEjemplo: write(fd, buffer, size) toma los datos de buffer y los escribe en el archivo o
dispositivo asociado a fd.
4.close(): Cierra un archivo o dispositivo
oLa llamada close() permite a una aplicación cerrar un archivo o dispositivo que ya no
necesita. Esto libera el descriptor de archivo y permite que otros procesos puedan
acceder a él.
oEjemplo: close(fd) cierra el archivo o dispositivo identificado por fd.

3c. Principales Llamadas del Sistema para E/S
5.ioctl(): Control de dispositivo de E/S
oLa llamada ioctl() es una función especial que se utiliza para enviar comandos específicos
a dispositivos, permitiendo el control de hardware mediante instrucciones
personalizadas.
oEjemplo: ioctl(fd, command, argument) permite enviar comandos de bajo nivel a un
dispositivo como una tarjeta de red, ajustando configuraciones específicas o controlando
funcionalidades avanzadas.
6.lseek(): Mueve el puntero de un archivo
oLa llamada lseek() ajusta la posición del puntero en un archivo abierto, permitiendo el
acceso aleatorio en archivos de dispositivos de bloques.
oEjemplo: lseek(fd, offset, SEEK_SET) mueve el puntero de archivo fd al desplazamiento
offset desde el inicio del archivo (usando SEEK_SET), lo cual es útil para trabajar con
archivos grandes.

Funcionalidad de las Llamadas de Sistema
para E/S
•Las llamadas de sistema para E/S encapsulan la complejidad de interactuar
directamente con el hardware de E/S, proporcionando a las aplicaciones una
interfaz uniforme y sencilla. Estas llamadas funcionan de la siguiente
manera:
1.Control de Acceso y Seguridad
2.Aislamiento de Errores
3.Eficiencia y Almacenamiento en Búfer
4.Compatibilidad y Portabilidad

1.Control de Acceso y Seguridad
1.El sistema operativo asegura que las aplicaciones solo puedan acceder a los
archivos y dispositivos para los que tienen permisos, evitando accesos no
autorizados a recursos del sistema.
•Por ejemplo, si una aplicación intenta abrir un archivo sin permisos de lectura, la
llamada open() fallará, y el sistema operativo devolverá un error.
2.Aislamiento de Errores:
•Las llamadas de sistema para E/S manejan los errores de hardware o software que
ocurren durante las operaciones de E/S, notificando a la aplicación sin interrumpir
el funcionamiento general del sistema.
•Ejemplo: Si una llamada read() falla porque el dispositivo de almacenamiento no
responde, el sistema operativo devuelve un código de error, permitiendo que la
aplicación gestione el fallo sin afectar el sistema.

2b.  Control de Acceso y Seguridad
1.El sistema operativo asegura que las aplicaciones solo puedan acceder a los
archivos y dispositivos para los que tienen permisos, evitando accesos no
autorizados a recursos del sistema.
•Por ejemplo, si una aplicación intenta abrir un archivo sin permisos de lectura, la
llamada open() fallará, y el sistema operativo devolverá un error.
2.Aislamiento de Errores:
•Las llamadas de sistema para E/S manejan los errores de hardware o software que
ocurren durante las operaciones de E/S, notificando a la aplicación sin interrumpir
el funcionamiento general del sistema.
•Ejemplo: Si una llamada read() falla porque el dispositivo de almacenamiento no
responde, el sistema operativo devuelve un código de error, permitiendo que la
aplicación gestione el fallo sin afectar el sistema.

2c.  Control de Acceso y Seguridad
3.Eficiencia y Almacenamiento en Búfer:
•Las llamadas de sistema para E/S utilizan almacenamiento en búfer para
optimizar las operaciones de entrada y salida. El sistema operativo puede
acumular datos en un búfer y enviarlos al hardware en lotes, lo cual es más
eficiente que realizar múltiples llamadas directas al hardware.
•Ejemplo: Al escribir en un archivo grande, el sistema operativo puede
acumular varios fragmentos de datos en un búfer y escribirlos todos a la vez
en el disco, reduciendo así el número de operaciones de escritura física.
4.Compatibilidad y Portabilidad:
•Las llamadas de sistema estandarizan las operaciones de E/S en diferentes
sistemas operativos y arquitecturas de hardware, permitiendo que las
aplicaciones sean portátiles y funcionen en diversos entornos sin necesidad
de modificar el código.

Ejemplos de Uso de Llamadas de Sistema para E/S en
## Aplicaciones
1.Aplicaciones de Archivos:
oUn editor de texto usa open() para acceder a un archivo, read() para cargar su
contenido, write() para guardar cambios, y close() para liberar el archivo cuando el
usuario termina de editar.
2.Aplicaciones de Red:
oEn un servidor web, open() se utiliza para iniciar una conexión, read() y write() para
enviar y recibir datos de los clientes, y close() para terminar la conexión cuando finaliza
la sesión del cliente.
3.Gestión de Dispositivos de E/S Especializados:
oAplicaciones que interactúan con hardware especializado (como impresoras o
escáneres) utilizan ioctl() para enviar comandos específicos de control y configuración
al dispositivo, permitiendo, por ejemplo, ajustar la resolución de un escáner o
configurar una impresora en un modo específico.

Ventajas de las Llamadas de Sistema para E/S
1.Abstracción del Hardware: Las llamadas de sistema para E/S
ocultan los detalles de hardware de las aplicaciones,
permitiendo que los desarrolladores trabajen con una interfaz
estandarizada sin preocuparse por las complejidades de cada
dispositivo.
2.Seguridad y Control de Acceso: El sistema operativo controla el
acceso a los dispositivos, protegiendo la integridad de los datos
y la estabilidad del sistema al restringir las operaciones de E/S a
procesos autorizados.
3.Manejo de Errores: Las llamadas de sistema para E/S
proporcionan mecanismos integrados para gestionar errores de
dispositivos o de permisos, permitiendo que las aplicaciones
respondan de manera controlada y evitando fallos críticos en el
sistema.
4.Portabilidad del Software: Gracias a estas llamadas, el código
de E/S de una aplicación puede funcionar en distintos sistemas
operativos y arquitecturas, facilitando la migración y reutilización
de software.

4.Almacenamiento en Búfer y Almacenamiento en
## Caché
•El almacenamiento en búfer y el almacenamiento en caché
son dos técnicas fundamentales utilizadas en sistemas
operativos para mejorar la eficiencia de las operaciones de
entrada/salida (E/S). Aunque ambos términos suelen usarse
de forma similar, tienen diferencias significativas en cuanto a
su propósito y funcionamiento.

a.Almacenamiento en Búfer
•El almacenamiento en búfer (buffering) se refiere a una técnica donde los datos se
almacenan temporalmente en una región de memoria intermedia llamada búfer. El
propósito principal del búfer es sincronizar la velocidad de transferencia entre
dispositivos que operan a diferentes velocidades y reducir la latencia de E/S.
•Características del Almacenamiento en Búfer
I.Sincronización de Velocidad: Los dispositivos de E/S, como discos duros y
dispositivos de red, suelen operar a velocidades diferentes al CPU. Un búfer permite
almacenar los datos temporalmente mientras se ajusta la velocidad de transferencia
entre el dispositivo y el sistema.
II.Reducción de Latencia: Al almacenar datos en un búfer, el sistema puede continuar
procesando la siguiente operación sin esperar a que la transferencia de datos se
complete, reduciendo el tiempo de inactividad.
III.Evita Bloqueos de E/S: Si un proceso necesita enviar o recibir grandes cantidades
de datos, un búfer puede acumular estos datos en fragmentos, permitiendo que el
proceso avance sin esperar a que los datos se escriban o lean completamente.

a.Almacenamiento en Búfer (II)
•Tipos de Almacenamiento en Búfer
•Búfer de Entrada: Almacena temporalmente los datos recibidos de un dispositivo
hasta que el proceso esté listo para procesarlos. Por ejemplo, al descargar un
archivo, el sistema operativo utiliza un búfer de entrada para almacenar los datos
recibidos de la red.
•Búfer de Salida: Acumula datos que un proceso desea enviar a un dispositivo de
salida, como una impresora o un archivo de disco. Los datos se envían en lotes al
dispositivo, lo que reduce la cantidad de transferencias y mejora la eficiencia.
•Doble Búfer (Double Buffering): Consiste en usar dos búferes en paralelo para
que, mientras se escribe en uno, el sistema puede leer el otro. Esto es ideal en
sistemas de alto rendimiento y multimedia, donde los datos necesitan procesarse y
transferirse rápidamente.
•Ejemplo de Almacenamiento en Búfer
•En una operación de impresión, los datos de un documento se envían primero a un
búfer de impresión. El sistema operativo escribe en este búfer mientras la
impresora, que opera a una velocidad diferente, lee los datos desde el mismo. Esto
permite que la aplicación de usuario continúe trabajando mientras la impresora
procesa el contenido de manera gradual.

2.Almacenamiento en Caché
•El almacenamiento en caché es una técnica que guarda temporalmente datos de
acceso frecuente o reciente en una memoria de acceso rápido, conocida como
caché, para acelerar futuras solicitudes. A diferencia del búfer, el objetivo principal de
la caché es mejorar el rendimiento de acceso a datos que ya han sido solicitados
previamente, reduciendo así el tiempo de acceso y evitando operaciones de E/S
repetitivas.
•Características del Almacenamiento en Caché
1.Minimización de Operaciones de E/S: Al almacenar datos de acceso frecuente, el sistema puede
reducir la cantidad de veces que necesita acceder al dispositivo de almacenamiento principal, como
un disco duro o una base de datos.
2.Memoria de Alta Velocidad: La caché suele estar ubicada en una memoria de acceso rápido, como
la memoria RAM o la memoria interna del procesador (caché L1, L2 o L3), lo que permite un acceso
más rápido a los datos en comparación con los dispositivos de almacenamiento de mayor latencia.
3.Estrategias de Reemplazo: La caché tiene un espacio limitado, por lo que utiliza algoritmos de
reemplazo (como LRU, FIFO) para decidir qué datos eliminar cuando se necesita espacio para
almacenar nuevos datos.

2b. Tipos de Almacenamiento en Caché
•Caché de Disco: Almacena datos de acceso frecuente de un disco duro o
SSD. Los sistemas operativos utilizan la caché de disco para almacenar
sectores o bloques que se han leído recientemente, optimizando la carga
de archivos.
•Caché de Páginas: Utilizada en sistemas de memoria virtual, la caché de
páginas almacena las páginas de memoria que se utilizan con mayor
frecuencia, lo que mejora el rendimiento de los procesos al reducir los fallos
de página.
•Caché de Red: En sistemas de red, los datos recibidos desde el servidor se
almacenan en una caché para mejorar el rendimiento y reducir el tráfico de
red. Los navegadores web, por ejemplo, almacenan imágenes y contenido
en caché para que las páginas se carguen más rápido en visitas posteriores.

Diferencias entre Almacenamiento en Búfer y
Almacenamiento en Caché

Beneficios del Almacenamiento en Búfer y
Almacenamiento en Caché

Ejemplos de Uso Combinado de Búfer y
Caché en Sistemas Operativos Modernos