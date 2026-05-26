

Gestióndel sistema
## Operativo
## ING. JUAN ANDRÉS GARCÍA MORENO

Principales Logros de lo SO
Procesos.
Gestión de memoria.
Protección y seguridad de la información.
Planificación y gestión de los recursos.
Estructura del sistema.

## Procesos
El concepto de proceso surgió como una necesidad para gestionar de
manera eficiente la ejecución de programas en los sistemas operativos
Se le da muchas interpretaciones:
Un programa en ejecución.
Una instancia de un programa ejecutándose en un computador.
La entidad que se puede asignar o ejecutar en un procesador.
Una unidad de actividad caracterizada por un solo hilo secuencial de
ejecución, un estado actual, y un conjunto de recursos del sistema asociados.

Necesidades de los Procesos
En las primeras etapas del desarrollo de los sistemas operativos, no existían
métodos estandarizados o formalizados para coordinar y gestionar las
actividades y recursos dentro del sistema.
En lugar de utilizar un enfoque sistemático o estructurado, los
programadores recurrían a soluciones "ad hoc“.
No existía una teoría o metodología bien establecida sobre cómo
gestionar los procesos, la memoria, o los dispositivos de entrada/salida de
manera eficiente.

Errores de la Falta de Estandarización
Inapropiada sincronización: Es frecuente el hecho de que una rutina se
suspenda esperando por algún evento en el sistema.
Violación de la exclusión mutua: Frecuentemente, más de un programa o
usuario intentan hacer uso de recursos compartidos simultáneamente. Si estos
accesos no se controlan, podría ocurrir un error.
Operación no determinista de un programa: cuando los programas
comparten memoria, y sus ejecuciones son entrelazadas por el procesador,
podrían interferir entre ellos, sobrescribiendo zonas de memoria comunes de
una forma impredecible.
Interbloqueos: dos programas podrían requerir dos dispositivos de E/S para
llevar a cabo una determinada operación. Cada uno de ellos está esperando
a que el otro programa libere el recurso que no poseen. Dicho interbloqueo
puede depender de la temporización de la asignación y liberación de
recursos.

¿Qué es un proceso?
Un proceso es:
Un programa en ejecución
Una actividad
Una tarea del sistema
Envío de datos

Gestión de memoria
La memoria principal es una
matriz de palabras o bytes.
Cada palabra o byte tiene su
propia dirección.
El SO asigna los archivos a los
soportes físicos y accede a dichos
archivos a través de los
dispositivos de almacenamiento.
Tarea: investigar sobre el ciclo
de extracción de instrucciones
de VonNewmann

Jerarquía de memoria
Para un sistema práctico, el
coste de la memoria debe ser
razonable en relación con los
otros componentes.
se cumplen las siguientes
relaciones:
✓A menor tiempo de acceso,
mayor coste por bit
✓A mayor capacidad, menor
coste por bit
✓A mayor capacidad, mayor
tiempo de acceso

## Gestióndelalmacenamientomasivo
El sistema operativo es responsable de las siguientes
actividades en lo que se refiere a la gestión de disco:
➢Gestión del espacio libre.
➢Asignación del espacio de almacenamiento.
➢Planificación del disco.

Gestión del espacio libre
La gestión del espacio libre implica mantener un registro de
las áreas no utilizadas del disco para que puedan ser
asignadas a nuevos archivos o datos. Esto se puede hacer
mediante varias técnicas:
Listas de espacios libres: Mantener una lista de bloques de
disco libres.
Mapas de bits: Utilizar un mapa de bits donde cada bit
representa un bloque del disco; un bit en 0 indica que el
bloque está libre.
Grupos de bloques libres: Agrupar bloques libres en
conjuntos para facilitar la asignación.

Asignación del Espacio de Almacenamiento
La asignación del espacio de almacenamiento se refiere a cómo se asignan los
bloques de disco a los archivos. Existen varios métodos para esto:
•Asignación contigua:Los archivos se almacenan en bloques contiguos. Es simple y
rápida, pero puede llevar a fragmentación externa.
•Asignación enlazada:Cada archivo es una lista de bloques de disco, donde cada
bloque contiene un puntero al siguiente. Esto elimina la fragmentación externa, pero
puede ser más lento.
•Asignación indexada: Utiliza una estructura de índice para mantener todos los
punteros a los bloques de un archivo. Es eficiente y flexible, pero puede requerir más
espacio para los índices.

Planificación del Disco
La planificación del disco se refiere a la forma en que el sistema operativo decide el
orden en que se atienden las solicitudes de lectura y escritura en el disco. Los algoritmos
de planificación del disco incluyen:
•FCFS (First-Come, First-Served):Las solicitudes se atienden en el orden en que llegan.
•SSTF (ShortestSeekTime First):Se atiende la solicitud más cercana a la posición actual del
cabezal.
•SCAN (ElevatorAlgorithm):El cabezal se mueve en una dirección atendiendo todas las
solicitudes hasta llegar al final, luego invierte la dirección.
•C-SCAN (Circular SCAN):Similar a SCAN, pero al llegar al final, el cabezal vuelve al inicio sin
atender solicitudes en el camino de regreso.

Nota: Fragmentación externa
La fragmentación externa ocurre cuando hay espacios libres dispersos entre bloques de memoria asignados, pero
estos espacios son demasiado pequeños para ser utilizados por nuevos procesos o datos.
Esto sucede cuando los bloques de memoria se asignan y liberan de manera continua, dejando huecos entre ellos
que no pueden ser aprovechados eficientemente.
Soluciones para la Fragmentación Externa:
Compactación: Reorganizar los bloques de memoria para juntar los espacios libres en un solo bloque
grande.
Paginación: Dividir la memoria en páginas de tamaño fijo, permitiendo que los procesos se asignen en
páginas no contiguas.
Segmentación: Dividir la memoria en segmentos de tamaño variable según las necesidades del
proceso, permitiendo una asignación más flexible.

Gestión de Memoria en HDD (Hard
## Disk Drive)
1.Estructura Física:
1.Los HDD utilizan platos giratorios cubiertos con material magnético para almacenar datos.
2.Un cabezal de lectura/escritura se mueve físicamente sobre los platos para acceder a los datos.
2.Asignación de Espacio:
1.Sectores y Clústeres:Los datos se dividen en sectores (512 bytes o 4 KB) y se agrupan en clústeres.
2.Fragmentación:La fragmentación externa puede ocurrir cuando los archivos se dividen en múltiples
clústeres no contiguos, lo que ralentiza el acceso a los datos.
3.Planificación del Disco:
1.Algoritmos de Planificación:Se utilizan algoritmos como FCFS, SSTF, SCAN y C-SCAN para optimizar el
movimiento del cabezal y reducir el tiempo de búsqueda.

Gestión de Memoria en SSD (Solid
StateDrive)
1.Estructura Física:
1.Los SSD utilizan memoria flash NAND para almacenar datos, sin partes móviles.
2.Los datos se almacenan en celdas de memoria que pueden ser de un solo nivel (SLC), multinivel (MLC) o triple nivel
## (TLC).
2.Asignación de Espacio:
1.Bloques y Páginas:Los datos se organizan en bloques (varios megabytes) y páginas (varios kilobytes).
2.WearLeveling:Técnica que distribuye uniformemente las escrituras y borrados para prolongar la vida útil del SSD.
3.Planificación del Disco:
1.Controlador SSD:Gestiona la lectura/escritura de datos, optimizando el rendimiento y la durabilidad.
2.TRIM:Comando que permite al sistema operativo informar al SSD qué bloques de datos ya no son necesarios,
mejorando la eficiencia de las escrituras futuras.
Ver video: https://www.youtube.com/watch?v=tut4twg9nAo&t=14s

Almacenamiento en Caché
Es una técnica que consiste en almacenar temporalmente datos en una
memoria de acceso rápido (caché) para mejorar el tiempo de acceso a
esos datos. En lugar de acceder a la memoria principal o al disco duro, los
sistemas pueden recuperar los datos desde la caché, lo que resulta en un
rendimiento mucho más rápido.

Tipos de Caché
Caché de CPU
Caché de Disco
Caché de Navegador

Caché de CPU
L1 Cache: Es la memoria caché más cercana al núcleo del procesador y, por lo tanto,
la más rápida, pero también la más pequeña (generalmente entre 32 KB y 128 KB).
❖Uso: Almacena datos e instrucciones que la CPU está utilizando actualmente o
utilizará inmediatamente.
L2 Cache: Un poco más grande y más lenta que la L1, pero todavía muy rápida
(tamaño típico entre 256 KB y 1 MB).
❖Uso: Almacena datos e instrucciones que se espera que la CPU necesite pronto.
L3 Cache: La más grande (a menudo varios MB), pero también la más lenta de las
cachés del procesador. Generalmente es compartida por todos los núcleos de la
## CPU.
❖Uso: Almacena datos que podrían ser útiles para cualquier núcleo del procesador.

Ejemplo Caché CPU
Cuando la CPU necesita realizar una operación
matemática compleja, primero busca en la L1 Cache.
Si no encuentra los datos, sigue a L2, y finalmente a L3
antes de acceder a la memoria RAM más lenta.

Caché de Memoria (RAM)
Buffer Caché:
Almacena datos que están en proceso de ser escritos
en o leídos desde el disco. Esto mejora el rendimiento
de las operaciones de entrada/salida.
Ejemplo:Cuando un archivo es leído del disco duro, se
almacena en el buffer caché para que, si se necesita
de nuevo, no sea necesario acceder al disco otra vez.

Caché de Disco
Definición:
Utilizada por discos duros y SSDspara
almacenar datos frecuentemente accedidos.
Ejemplo:Un disco SSD almacena en caché
bloques de datos que se acceden con
frecuencia para reducir el tiempo de lectura.

## Caché Web
•Definición:
Utilizado por navegadores web para
almacenar archivos descargados de sitios web,
como imágenes y hojas de estilo CSS.
•Ejemplo:Cuando visitas un sitio web por
segunda vez, el navegador carga elementos
desde la caché en lugar de descargarlos
nuevamente.

Funcionamiento del Almacenamiento
en Caché
Principio de Localidad
Algoritmos de Caché

Principio de Localidad
## Localidad Temporal:
Los datos a los que se ha accedido recientemente es probable que se accedan de
nuevo en un futuro cercano.
•Ejemplo:En un bucle de programación, las mismas instrucciones se ejecutan
repetidamente, y es eficiente almacenarlas en caché.
## Localidad Espacial:
Los datos cercanos a los datos que se han accedido recientemente también es
probable que se accedan pronto.
•Ejemplo:Al leer un archivo grande, es probable que se necesiten los bloques
de datos que están próximos al bloque actual.

Algoritmos de Caché
LRU (LeastRecentlyUsed):
Elimina el bloque de caché que no ha sido utilizado durante más tiempo.
FIFO (FirstIn, FirstOut):
Elimina el bloque de caché que fue almacenado primero, independientemente de si se ha usado
recientemente.
LFU (LeastFrequentlyUsed):
Elimina el bloque de caché que ha sido accedido con menor frecuencia.
MRU (MostRecentlyUsed)
Elimina el dato que ha sido utilizado más recientemente.
## Ejemplo:
En un sistema de caché web, el navegador puede eliminar los archivos que no se han utilizado en las
últimas semanas (LRU) para liberar espacio para nuevos archivos.

Subsistema de E/S
Un objetivo clave de un sistema operativo es ocultar las peculiaridades de
los dispositivos hardware específicosa los usuarios y a la mayoría de las
aplicaciones.
Ejemplo: En sistemas como UNIX, las particularidades de los dispositivos de
entrada/salida (E/S) se ocultan mediante el subsistema de E/S. Este
subsistema gestiona la interacción con los dispositivos de manera
uniforme y abstracta, sin exponer los detalles específicos del hardware.

Componentes delSubsistema de E/S
Gestión de Memoria: Incluye almacenamiento en búfer, gestión de caché y
gestión de colas. Estos mecanismos permiten almacenar temporalmente los
datos en tránsito entre el dispositivo y la memoria principal, optimizando las
operaciones de E/S.
Interfaz General para Controladores: Proporciona una interfaz estándarpara
interactuar con los controladores de dispositivos, independientemente del
hardware subyacente.
Controladores de Dispositivos: Son los componentes específicos que
entienden y manejan las peculiaridades del hardware. Solo el controlador
del dispositivo conoce los detalles de cómo operar el hardware específico
asignado.

Protección en Sistemas Operativos
Mecanismo que controla el acceso de procesos y usuarios a los recursos
(archivos, memoria, CPU).
Función: Asegurar que sólo procesos autorizados puedan utilizar los
recursos del sistema.
Ejemplo: El hardware de direccionamiento de memoria asegura que un
proceso no acceda a la memoria de otro.

Mecanismos de Protección
•Mecanismos:
•Control de acceso a recursos: Cada proceso tiene su propio espacio de
memoria y control de CPU.
•Temporizador: Evita que un proceso acapare la CPU indefinidamente.
•Registros de control protegidos: Solo los usuarios autorizados acceden a ciertos
registros críticos.
Mejora la fiabilidad del sistema, detectando errores antes de que afecten
a otros subsistemas.

Seguridad en Sistemas Operativos
Conjunto de medidas para defender al sistema frente a ataques internos
y externos.
Ataques comunes:
Virus y gusanos: Software malicioso que daña el sistema.
Ataques de denegación de servicio (DoS): Consumir los recursos del sistema
para bloquear a usuarios legítimos.
Robo de identidad: Uso no autorizado de las credenciales de un usuario.
Responsabilidad del Sistema: Detectar y prevenir accesos no autorizados.

Autenticación de Usuarios
Identificación de Usuarios:
Los sistemas operativos mantienen una lista con los nombres de usuario y sus ID
de usuario (UID).
En Windows NT, estos identificadores son llamados SID (Security ID).
Autenticación: Cuando un usuario inicia sesión, el sistema identifica su UID y lo
asocia a sus procesos y recursos.

Grupos de Usuarios
Agrupación de usuarios que comparten ciertos privilegios o permisos.
Función:
Facilitar la asignación de permisos a varios usuarios simultáneamente.
Ejemplo: En UNIX, un grupo puede tener permiso para leer un archivo,
mientras que el propietario puede tener permisos de lectura y escritura.

Escalado de Privilegios
Proceso mediante el cual un usuario obtiene permisos adicionales
temporalmente.
Ejemplo en UNIX: El atributo setuidpermite que un programa se ejecute con el
UID del propietario del archivo, no con el del usuario actual.
Propósito: Permitir a los usuarios ejecutar ciertas acciones que
normalmente estarían restringidas.

Mecanismos de Protección Avanzada
•Prevención de accesos inapropiados: El sistema puede estar protegido,
pero aún es vulnerable si un atacante roba las credenciales de un
usuario.
•Funciones adicionales: En algunos sistemas, la seguridad es manejada por
el sistema operativo, mientras que en otros se requiere software adicional.