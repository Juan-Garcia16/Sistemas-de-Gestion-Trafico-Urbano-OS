

Introducción a las Computadoras
## Ing. Juan Andrés García Moreno

¿Q ué hace un Sist ema
O perat ivo?
Un sistema operativo (SO) explota los recursos de
hardware de uno o más procesadores para ofrecer un
conjunto de servicios a los usuarios del sistema.
El sistema operativo también gestiona la memoria
secundaria y los dispositivos de entrada/salida (E/S) en
nombre de los usuarios.

¿Q ué es un Sist ema O perat ivo
## (SO )?
Un sistema operativo (SO) es un conjunto de programas
que actúan como intermediarios entre el usuario y el
hardware de una computadora. Su función principal es
gestionar los recursos de hardware y proporcionar
servicios a los programas de aplicación.

Int roducción a  las
Compu t adoras
Un sistema operativo hace de intermediario entre, por un
lado, los programas de aplicación, las herramientas y los
usuarios, y, por otro, el hardware del computador.

Component es Básicos de  una
Compu t adora
Al más alto nivel, un computador consta del procesador,
la memoria y los componentes de E/S, incluyendo uno o
más  módulos de cada tipo.
Estos componentes se interconectan de manera que se
pueda lograr la función principal del computador, que es
ejecutar programas.

Element os Est ruct urales
principales de u na compu t adora
Según la definición anterior, se puede decir que hay
cuatro elementos estructurales principales:
•Procesador
•Memoria principal
•Módulos de E/S
•Bus del sistema

## Procesador
Controla el funcionamiento del computador y realiza sus
funciones de procesamiento de datos (Realiza cálculos y
ejecuta instrucciones de programas). Cuando sólo hay un
procesador, se denomina usualmente unidad central De
proceso (Central Processing Unit, CPU).
Cache: Memoria de alta velocidad cercana al procesador,
que almacena datos e instrucciones de uso frecuente.

## Memoria
Memoria Principal (RAM): Almacena datos e instrucciones
que la CPU necesita de manera inmediata. Es volátil, lo
que significa que pierde su contenido al apagar la
computadora.
Memoria Secundaria: Almacenamiento no volátil utilizado
para guardar datos y programas a largo plazo. Incluye
discos duros (HDD), unidades de estado sólido (SSD),
unidades flash y medios ópticos (CD, DVD).

Módulos  de  E/S
Transfieren los datos entre el computador y su entorno
externo.
•Dispositivos de Entrada: Permiten al usuario interactuar con la
computadora. Ejemplos: teclado, ratón, escáner.
•Dispositivos de Salida: Muestran resultados al usuario. Ejemplos:
monitor, impresora, altavoces.
•Dispositivos de Entrada/Salida Combinados: Dispositivos que
pueden tanto recibir como enviar datos. Ejemplos: pantallas
táctiles, módems, tarjetas de red.

C o m p o n e n t e s   d e
u n   c o m p u t a d o r :
v i s i ó n   a l   m á s   a l t o
n i v e l

¿ C ó m o   s e   r e a l i z a   e l   i n t e r c a m b i o   d e
d a t o s   e n t r e   p r o c e s a d o r   y   m e m o r i a
p r i n c i p a l ?
Una de las funciones del procesador es el intercambio de
datos con la memoria. Para este fin, se utilizan
normalmente dos registros internos (al procesador):
RDIM y RDAM.

## RD IM Y  RD AM
Registro de dirección de memoria (RDIM): especifica la
dirección de memoria de la siguiente lectura o escritura.
Registro de datos de memoria (RDAM): contiene los datos
que se van a escribir en la memoria o que recibe los datos
leídos de la memoria.

Int ercambio de dat os  en el
módu lo  E /S
Este intercambio de datos es similar al del procesador, un
registro de dirección de E/S (RDIE/S) especifica un
determinado dispositivo de E/S, y un registro de datos de
E/S (RDAE/S) permite el intercambio de datos entre un
módulo de E/S y el procesador.

Composición de  un módulo  de
memoria
Un módulo de memoria consta de un conjunto de posiciones
definidas mediante direcciones numeradas secuencialmente.
Cada posición contiene un patrón de bits que se puede
interpretar como una instrucción o como datos.
Un módulo de E/S transfiere datos desde los dispositivos
externos hacia el procesador y la memoria, y viceversa.
Contiene buffers (es decir, zonas de almacenamiento
internas) que mantienen temporalmente los datos hasta que
se puedan enviar.