

## M E M O R I A
I  N  G .     J  U  A  N     A  N  D  R  É  S     G  A  R  C  Í  A     M  O  R  E  N  O

## I M P O R T A N C I A   D E   L A   G E S T I Ó N   D E
## M E M O R I A
•La administración de la memoria es una función central de un sistema operativo
(SO), que asigna, organiza y supervisa los recursos de memoria física y virtual de
tu computadora. La gestión eficaz de la memoria permite que múltiples
programas y procesos compartan recursos de memoria limitados para una
experiencia informática de usuario optimizada y receptiva.

## P R O P Ó S I T O   D E   L A   G E S T I Ó N   D E
## M E M O R I A
•El propósito principal de un sistema operativo es ejecutar programas. Estos
programas, junto con los datos a los que acceden, deben encontrarse en memoria
principal durante la ejecución (al menos parcialmente).
•El S.O debe garantizar que cada proceso y aplicación en ejecución tenga acceso
a los recursos de memoria que necesita sin interferir con otros procesos ni
provocar fallas del sistema. Un S.O debe rastrear qué ubicaciones de memoria se
utilizan para realizar esta tarea. Asigna espacio de memoria a nuevos procesos
cuando comienzan a ejecutarse y desasigna procesos antiguos cuando ya no son
necesarios.

## ¿ C Ó M O   F U N C I O N A   L A   G E S T I Ó N   D E
## M E M O R I A   E N   E L   S I S T E M A
## O P E R A T I V O ?
•La gestión de la memoria en los sistemas operativos es compleja e involucra varios
componentes vitales que trabajan juntos para asignar y utilizar los recursos de
memoria de manera efectiva. Algunos son:
•Jerarquía de memoria
•Protección de la memoria
•Memoria virtual y paginación

## M E M O R I A   P R I N C I P A L
## R A M   ( M E M O R I A   D E   A C C E S O   A L E A T O R I O )
•La memoria principal se utiliza para mantener datos e instrucciones que están siendo
utilizados o procesados activamente. Permite un acceso rápido de lectura y escritura, lo cual
es esencial para el funcionamiento eficiente de aplicaciones y del sistema operativo.
•Volatilidad: La memoria principal es volátil, lo que significa que pierde su contenido cuando
se apaga la energía.
•Velocidad: La memoria principal es significativamente más rápida que el almacenamiento
secundario.
•Capacidad: La capacidad de la memoria principal puede variar ampliamente dependiendo
del sistema.

## C O N F O R M A C I Ó N   D E L   G E S T O R   D E   M E M O R I A
•Se encarga de las tareas relacionadas con la administración de la Memoria Principal:
•Asignación de Memoria Principal a los procesos que la solicitan
•Localización de espacios libres, y ocupados.
•Aprovechamiento máximo de dicha memoria.
•La memoria es una amplia tabla de datos, cada uno de los cuales con su propia dirección.
•Tanto el tamaño de la tabla, como el de los datos incluidos en ella dependen de cada
arquitectura concreta.
•Para que los programas puedan ser ejecutados es necesario que estén cargados en memoria
principal.
•La información que es necesario almacenar de modo permanente se guarda en dispositivos
de almacenamiento secundarios también conocidos como memoria secundaria.

## A S I G N A C I Ó N   D E   M E M O R I A
•Una de las principales responsabilidades de un sistema operativo en la gestión de
la memoria es asignar memoria para diversos procesos y aplicaciones. La
memoria se puede asignar estáticamente en el momento de la compilación o
dinámicamente durante la ejecución del programa. Se realiza mediante el uso de
algoritmos de asignación proporcionados por los proveedores de sistemas
operativos para maximizar el rendimiento del sistema.

## M E M O R I A   Y   M U L T I P R O G R A M A C I Ó N
•Es la capacidad de ejecutar varios programas simultáneamente depende de cómo
se maneja la memoria disponible para los diferentes procesos.
•Esto se logra aprovechando la capacidad del sistema para intercambiar
rápidamente entre procesos, de modo que mientras un proceso está esperando
(por ejemplo, esperando entrada/salida), otro proceso puede usar el procesador

## A S I G N A C I Ó N   D E   M E M O R I A   E N
## M U L T I P R O G R A M A C I Ó N
•En un sistema de multiprogramación, varios programas residen en la memoria
principal de manera simultánea. Cada proceso necesita un segmento de memoria
para ejecutar sus instrucciones y almacenar sus datos. La gestión eficiente de la
memoria es crucial para asegurar que todos los procesos tengan el espacio
necesario sin desperdiciar recursos.

## T É C N I C A S   D E   A S I G N A C I Ó N   D E
## M E M O R I A
•Swapping(intercambio)
•Paginación y Segmentación
•Fragmentación interna y externa

## S W A P P I N G( I N T E R C A M B I O )
•El sistema operativo transfiere temporalmente procesos (o parte de ellos) desde
la memoria principal al almacenamiento secundario (generalmente una partición
de intercambio o "swap"). Cuando el proceso que fue transferido al disco necesita
ejecutarse nuevamente, el sistema operativo lo trae de vuelta a la memoria RAM,
intercambiándolo por otro proceso que esté en un estado de espera o que no
necesite ejecutarse de inmediato.

## P R O C E S O   D E  S W A P P I N G
•Swap-out: Mover un proceso desde la memoria principal al almacenamiento
secundario para liberar espacio en la RAM.
•Swap-in:Traer un proceso de vuelta desde el almacenamiento secundario a la
memoria principal cuando necesita ejecutarse.

## E J E M P L O   D E  S W A P P I N G
•Imagina un sistema con 4 GB de RAM y 6 procesos activos que requieren un total
de 5 GB de memoria para ejecutarse. En este caso, el sistema no puede mantener
todos los procesos en la RAM al mismo tiempo. Algunos procesos menos
prioritarios o que están en espera son "swappedout" al disco, liberando espacio
en la RAM para que los procesos prioritarios o que están en ejecución puedan
continuar.
•Cuando un proceso en el disco necesita ejecutar, el sistema operativo realiza un
"swap-in" y lo trae de vuelta a la memoria, intercambiándolo con otro proceso
que no sea crítico en ese momento.

## V E N T A J A S   D E L  S W A P P I N G
•Mayor Multiprogramación: Permite ejecutar más procesos de los que cabrían
simultáneamente en la memoria física.
•Utilización Óptima de Recursos: Evita que los procesos inactivos ocupen memoria
física, liberando espacio para procesos más activos.

## D E S V E N T A J A S   D E L  S W A P P I N G
•Alto Costo de Tiempo: El acceso al disco es mucho más lento que el acceso a la
memoria RAM, por lo que mover procesos entre la memoria y el disco genera un
costo significativo en tiempo.
•Thrashing: Si el sistema se encuentra en un estado en el que constantemente tiene
que intercambiar procesos entre la RAM y el disco, puede llegar a un punto en el
que pasa más tiempo realizando swappingque ejecutando procesos. Este
fenómeno se llama thrashingy reduce drásticamente el rendimiento del sistema.

## P A G I N A C I Ó N
•Paginaciónes una técnica de gestión de memoria en los sistemas operativos que
permite dividir el espacio de direcciones de un proceso y la memoria física en
bloques de tamaño fijo llamados páginas(memoria lógica) y marcos(memoria
física), respectivamente. Su principal objetivo es mejorar la utilización de la
memoria y facilitar la asignación de memoria a los procesos, eliminando el
problema de la fragmentación externa.

## ¿ C Ó M O   F U N C I O N A   L A   P A G I N A C I Ó N ?
1.División de la Memoria
2.Asignación de Memoria
3.Traducción de Direcciones

## 1 .   D I V I S I Ó N   D E   L A   M E M O R I A
•La memoria física (RAM) se divide en bloques de tamaño fijo llamados marcos (o
frames).
•El espacio de direcciones de cada proceso se divide en bloques del mismo
tamaño, llamados páginas.

## 2 .   A S I G N A C I Ó N   D E   M E M O R I A
•Cuando un proceso se carga en memoria, sus páginas no necesitan ocupar un
bloque contiguo de marcos. Pueden asignarse a marcos dispersos en la memoria
física.
•Cada vez que el CPU necesita acceder a una dirección lógica, la tabla de
páginas del proceso se utiliza para traducir la dirección lógica (número de
página) en una dirección física (número de marco).

## 3 .   T R A D U C C I Ó N   D E   D I R E C C I O N E S
•La dirección lógica se divide en dos partes: el número de página y el
desplazamiento dentro de la página. El sistema operativo utiliza el número de
página para buscar en la tabla de páginas cuál es el marco correspondiente en
la memoria física.
•Luego, utiliza el desplazamiento dentro de la página para acceder a la dirección
específica dentro de ese marco.

## V E N T A J A S   D E   L A   P A G I N A C I Ó N
•Elimina la Fragmentación Externa: Dado que las páginas y los marcos tienen el mismo tamaño, no
hay problemas de fragmentación externa. Esto significa que no hay espacios grandes en la
memoria física que se desperdicien.
•Asignación Flexible de Memoria: Los procesos no necesitan ocupar un bloque contiguo de memoria
física, lo que facilita la asignación de memoria incluso cuando la memoria está fragmentada.
•Aislamiento de Procesos: La paginación ayuda a aislar los procesos entre sí, ya que cada proceso
tiene su propio espacio de direcciones virtual, y cualquier intento de acceder a una dirección fuera
de su espacio resulta en una violación de acceso.
•Memoria Virtual: La paginación es la base de la implementación de la memoria virtual,
permitiendo que un proceso utilice más memoria de la que está físicamente disponible mediante el
uso del almacenamiento secundario (disco) para almacenar páginas que no se usan activamente.

## D E S V E N T A J A S   D E   L A   P A G I N A C I Ó N
•Sobrecarga de la Tabla de Páginas: Cada proceso necesita una tabla de páginas para
gestionar la traducción de direcciones lógicas a direcciones físicas. Si el proceso tiene un
espacio de direcciones muy grande, la tabla de páginas puede consumir mucha memoria.
•Fragmentación Interna: Aunque no hay fragmentación externa, puede haber
fragmentación interna si un proceso no utiliza completamente las páginas asignadas, lo
que genera desperdicio dentro de una página.
•Fallas de Página (Page Faults): Si una página que un proceso necesita no está en la
memoria física (por ejemplo, ha sido paginada al disco), se produce una falla de página.
El sistema operativo debe entonces cargar la página desde el disco, lo cual es una
operación costosa en términos de tiempo.

## T I P O S   D E   P A G I N A C I Ó N
1.Paginación Simple:
•Es la forma básica donde todas las páginas de un proceso tienen el mismo tamaño y se asignan a marcos de
igual tamaño en la memoria física.
2.Paginación por Demanda:
•En lugar de cargar todas las páginas de un proceso en la memoria física de inmediato, se cargan solo las
páginas que son necesarias en ese momento. Las páginas restantes se guardan en el disco y se traen a la
memoria solo cuando se requieren.
•Ventaja: Ahorra memoria física al no cargar todo el proceso.
•Desventaja: Las fallas de páginason más frecuentes si el sistema no predice bien qué páginas se necesitarán.
3.Paginación Inversa (InvertedPaging):
•En vez de tener una tabla de páginas por proceso, hay una tabla global de páginas que mapea cada marco
físico con la página de un proceso en particular.
•Ventaja: Reduce el tamaño total de las tablas de páginas.
•Desventaja: La traducción de direcciones puede ser más lenta porque requiere una búsqueda más compleja.

## P R O B L E M A   D E   F R A G M E N T A C I Ó N
## I N T E R N A   E N   P A G I N A C I Ó N
•Aunque la paginación elimina la fragmentación externa, puede haber
fragmentación internasi el proceso no utiliza completamente una página
asignada. Por ejemplo, si el tamaño de página es de 4 KB y el proceso solo
necesita 2 KB, los 2 KB restantes en esa página se desperdician.

## E J E M P L O   D E   P A G I N A C I Ó N
•Un sistema tiene una memoria física de 16 KB, dividida en marcos de 4 KB, y que hay un proceso
con un espacio de direcciones de 12 KB, dividido en 3 páginas de 4 KB cada una.
•Solución:
•Cuando el proceso se carga, las 3 páginas pueden asignarse a cualquier marco libre en la
memoria física, no necesariamente de manera contigua.
•El sistema operativo utiliza la tabla de páginasdel proceso para traducir la dirección lógica
(el número de página) en la dirección física (el número de marco).
•Si el proceso accede a una dirección que corresponde a una página no cargada en memoria,
se produce una falla de páginay el sistema operativo carga la página desde el disco.

## S W A P P I N GV S .   P A G I N A C I Ó N
•Aunque el swappingy la paginaciónson técnicas de gestión de memoria, tienen
diferencias clave:
•Swappingintercambia procesos completos entre la memoria y el disco.
•Paginaciónintercambia solo pequeñas porciones de un proceso (páginas)
entre la memoria y el disco, lo que permite una asignación de memoria más
granular y eficiente.

## S E G M E N T A C I Ó N
•La segmentaciónes una técnica de gestión de memoria que permite dividir el
espacio de direcciones de un proceso en diferentes segmentos lógicos. Estos
segmentos representan partes del proceso, como código, datos, pila, y otras
estructuras que tienen significado semántico. La segmentación proporciona una
forma de organizar la memoria que refleja la estructura lógica del programa, en
lugar de dividir la memoria en bloques de tamaño fijo como en la paginación.

## C A R A C T E R Í S T I C A S   D E   L A
## S E G M E N T A C I Ó N
1.División en Segmentos
2.Tamaño Variable.
3.Tabla de Segmentos.
4.Dirección Lógica.

## 1 .   D I V I S I Ó N   E N   S E G M E N T O S
•La memoria se divide en segmentos, que son unidades de tamaño variable. Cada
segmento puede tener un propósito específico, como:
•Segmento de código: Contiene las instrucciones ejecutables del programa.
•Segmento de datos: Almacena variables y estructuras de datos.
•Segmento de pila: Utilizado para la gestión de funciones y almacenamiento
temporal de datos.

## 2 .   T A M A Ñ O   V A R I A B L E
•A diferencia de la paginación, donde todas las páginas tienen el mismo tamaño,
los segmentos pueden variar en tamaño según las necesidades del programa.

## 3 .   T A B L A   D E   S E G M E N T O S
•Cada proceso tiene una tabla de segmentosque mantiene información sobre
cada segmento, incluyendo su base (dirección de inicio en memoria) y límite
(tamaño del segmento). Esto permite que el sistema operativo traduzca las
direcciones lógicas a direcciones físicas.

## 4 .   D I R E C C I Ó N   L Ó G I C A
•Una dirección lógica en un sistema segmentado se representa mediante dos
componentes:
•Número de segmento: Identifica el segmento específico.
•Desplazamiento: Indica la posición dentro del segmento.

## V E N T A J A S   D E   L A   S E G M E N T A C I Ó N
1.Organización Lógica.
2.Facilita el Compartimiento.
3.Protección y Aislamiento.
4.Eliminación de Fragmentación Externa.

## 1 .   O R G A N I Z A C I Ó N
## L Ó G I C A
•La segmentación permite organizar
la memoria de manera que refleje
la estructura lógica del programa, lo
que facilita la programación y la
gestión de recursos.
## 2 .   F A C I L I T A   E L
## C O M P A R T I M I E N T O
•Los segmentos pueden ser
compartidos entre procesos, lo que
es útil para bibliotecas de código y
otras estructuras de datos que se
utilizan en múltiples programas.

## 3 .   P R O T E C C I Ó N   Y
## A I S L A M I E N T O
•Al tener segmentos bien definidos,
es más fácil implementar
mecanismos de protección y
aislamiento entre procesos,
evitando que un proceso acceda a
segmentos de otro.
## 4 .   E L I M I N A C I Ó N   D E
## F R A G M E N T A C I Ó N   E X T E R N A
•Aunque la segmentación puede presentar
fragmentación interna, ayuda a evitar la
fragmentación externa al asignar solo la
cantidad necesaria de memoria para cada
segmento.

## D E S V E N T A J A S   D E   L A   S E G M E N T A C I Ó N
1.Fragmentación Externa:
•Puede haber fragmentación externa cuando los segmentos se asignan y liberan de
manera irregular, dejando espacios libres entre ellos.
2.Sobrecarga de la Tabla de Segmentos:
•Cada proceso requiere una tabla de segmentos que puede consumir memoria,
especialmente si un proceso tiene muchos segmentos.
3.Acceso a la Memoria:
•El acceso a la memoria puede ser un poco más lento debido a la necesidad de
buscar en la tabla de segmentos para obtener la dirección física.

## E J E M P L O   D E   S E G M E N T A C I Ó N
•Supongamos que tenemos un programa que requiere los siguientes segmentos:
Segmento 0 (Código): 10 KB
Segmento 1 (Datos): 5 KB
Segmento 2 (Pila): 3 KB
•La tabla de segmentos para este proceso podría verse así:
## Segmento
## 0
## 1
## 2
Base (Dirección)
## 0x0000
0x000A
0x000F
Límite (Tamaño)
## 10 KB
## 5 KB
## 3 KB

## S O L U C I Ó N   E J E M P L O   D E
## S E G M E N T A C I Ó N
•Si el programa intenta acceder a la dirección lógica (1, 200) (donde 1 es el
número de segmento y 200 es el desplazamiento), el sistema operativo buscaría
en la tabla de segmentos:
•El segmento 1 tiene una base de 0x000A y un límite de 5 KB.
•La dirección física se calcularía como: Base + Desplazamiento = 0x000A + 200 = 0x000C8.
La segmentación es una técnica eficaz para gestionar la memoria en sistemas operativos, proporcionando una
organización que refleja la estructura lógica del programa. Aunque presenta ciertas desventajas, como la
posibilidad de fragmentación externa, sus beneficios en términos de organización y protección de procesos la
hacen una opción valiosa en la gestión de memoria.

## D I F E R E N C I A S   E N T R E   S E G M E N T A C I Ó N   Y
## P A G I N A C I Ó N

## F R A G M E N T A C I Ó N   I N T E R N A   Y
## F R A G M E N T A C I Ó N   E X T E R N A
•Son dos tipos de problemas que pueden surgir en la gestión de la memoria de un
sistema operativo, relacionados con la forma en que se asigna y utiliza la
memoria para los procesos. Ambas implican desperdicio de memoria, pero
difieren en cómo y por qué ocurre este desperdicio.

## F R A G M E N T A C I Ó N   I N T E R N A
•La fragmentación interna ocurre cuando la memoria asignada a un proceso
excede ligeramente la cantidad de memoria que realmente necesita. Esto sucede
cuando se asignan bloques de memoria de tamaño fijo (como en la paginación),
lo que puede generar desperdicio de memoria dentro de los bloques asignados.

## C A U S A S   D E   L A   F R A G M E N T A C I Ó N
## I N T E R N A
•Ocurre en técnicas de asignación de memoria con bloques de tamaño fijo, como la
paginación o cuando los sistemas de memoria asignan bloques en unidades fijas.
•Si un proceso necesita menos memoria de la que se le ha asignado (por ejemplo,
si un bloque de 4 KB se asigna a un proceso que necesita 3.5 KB), el espacio
restante dentro del bloque se desperdicia.

## E J E M P L O
•Un sistema de memoria con bloques fijos de 4 KB y un proceso que necesita 6.5
KB de memoria. Como el tamaño del bloque es fijo, el proceso se asignará a dos
bloques:
•Primer bloque: 4 KB (lleno completamente).
•Segundo bloque: 4 KB (pero solo se usan 2.5 KB, el resto de 1.5 KB se
desperdicia).
Resultado: Hay fragmentación interna porque una parte del segundo bloque (1.5
KB) no se utiliza.

## S O L U C I O N E S
•Paginación por demanda o uso de bloques más pequeños podría reducir la
fragmentación interna, pero no la eliminaría por completo.
•Asignación dinámica con bloques de tamaño ajustado puede ayudar en algunas
situaciones.

## F R A G M E N T A C I Ó N   E X T E R N A
•La fragmentación externa ocurre cuando se asignan bloques de tamaño variable
a los procesos y con el tiempo los procesos se cargan y descargan de la memoria,
dejando espacios pequeños o "agujeros" dispersos por la memoria que no son
suficientes para satisfacer nuevas solicitudes de memoria.

## C A U S A S   D E   L A   F R A G M E N T A C I Ó N
## E X T E R N A
•Ocurre típicamente en técnicas de asignación de memoria de tamaño variable,
como en la segmentación o en sistemas de memoria con bloques de tamaño
dinámico.
•A medida que los procesos se asignan y liberan, se crean pequeños espacios
libres entre los bloques de memoria que no son lo suficientemente grandes para
asignar a nuevos procesos, aunque el espacio total libre sea suficiente.

## E J E M P L O
•Supongamos que tienes un sistema que asigna bloques de memoria
variable, y asignas los siguientes bloques a procesos:
•Proceso A: 10 KB
•Proceso B: 15 KB
•Proceso C: 20 KB
•Si luego el Proceso B termina y se libera su bloque de 15 KB, pero un nuevo proceso
necesita 18 KB de memoria, no podrá usar ese espacio libre. Aunque hay 15 KB
disponibles, el proceso de 18 KB no cabe allí.
•Resultado: La fragmentación externa ocurre porque la memoria tiene espacio
disponible, pero no de tamaño suficiente para acomodar los procesos que lo necesitan.

## S O L U C I O N E S
•Compactación de memoria: Reorganizar la memoria para agrupar los bloques
libres en una sola área contigua de memoria libre. Sin embargo, este proceso
puede ser costoso en términos de tiempo y recursos.
•Segmentación con paginación: Combinar las técnicas de segmentación y
paginación puede ayudar a reducir la fragmentación externa al permitir que los
segmentos se dividan en páginas de tamaño fijo.
•Asignación de memoria por "mejor ajuste" o "primer ajuste": Estas son
estrategias para asignar la memoria de manera más eficiente.

## C O M P A R A C I Ó N   E N T R E   F R A G M E N T A C I Ó N
## I N T E R N A   Y   E X T E R N A
AspectoFragmentación InternaFragmentación Externa
## Definición
Desperdicio dentro de bloques de
memoria asignados que no se usan
completamente.
Espacios libres dispersos entre
bloques de memoria que no son
suficientes para nuevos procesos.
Ocurre en
Paginación o cualquier sistema que
use bloques de tamaño fijo.
Segmentación o asignación de
bloques de tamaño variable.
Causa principal
Bloques de tamaño fijo que no se
usan completamente.
Bloques de tamaño variable que
dejan pequeños espacios entre
ellos.
Soluciones comunes
Usar bloques de tamaño más
ajustado o dinámico.
Compactación, mejor ajuste,
combinación de segmentación y
paginación.

## E J E R C I C I O   E N   C L A S E
•En un sistema con 512 MB de memoria física, varios procesos están en ejecución. Un proceso en
particular, llamado Proceso A, requiere 150 MB de memoria, pero solo hay 80 MB disponibles en ese
momento. El sistema operativo debe gestionar esta situación para que el Proceso A pueda ejecutarse
correctamente. Utilizar la técnica adecuada para resolver el problema