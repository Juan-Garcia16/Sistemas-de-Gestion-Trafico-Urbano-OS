

Registros del
## Procesador
## Ing. Juan Andrés García
## Moreno

Conjuntos de Registros
Un procesador incluye un conjunto de registros que proporcionan
un tipo de memoria que es más rápida y de menor capacidad que
la memoria principal. Los registros del procesador sirven para dos
funciones:
•Registros visibles para el usuario.
•Registros de control y estado.
•No hay una clasificación nítida de los registros entre estas dos
categorías. Por ejemplo, en algunas máquinas el contador de
programa es visible para el usuario, pero en muchas otras no lo
es.

Registros visibles para el usuario o
Registros de Propósito General (GPR)
•Son los registros que el programador puede utilizar
directamente para almacenar datos temporales, realizar
operaciones aritméticas y lógicas, y manejar direcciones de
memoria. Son los registros más comúnmente utilizados en la
programación a nivel de ensamblador.

Registros visibles para el usuario
•Se puede acceder por medio del lenguaje de máquina ejecutado por el
procesador que está generalmente disponible para todos los programas,
incluyendo tanto programas de aplicación como programas de sistema.
•Los tipos de registros que están normalmente disponibles son registros de
datos, de dirección y de códigos de condición.
•Un programa puede utilizar los registros de datos para diversas funciones:
ejemplo operaciones sobre datos.

Restricciones de los registros
visibles para el usuario.
1.Tamaño Fijo.
2.Acceso Condicionado: Compatibilidad con
## Instrucciones.
3.Uso en Programas en Modo Usuario vs. Modo
## Kernel.
4.Reglas de Llamado.
5.Sincronización en Sistemas Multiproceso.
6.Acceso a Registros Reservados.
7.Almacenamiento de Tipos de Datos.
8.Restricciones de Instrucciones SIMD.
Importante para garantizar
estabilidad del sistema.
Aunque los programadores
tienen acceso directo a estos
registros, deben seguir ciertas
reglas y convenciones para
evitar errores y asegurar que
sus programas funcionen de
manera eficiente y segura.

Registros GPR - Registros de
## Dirección. Parte I
•Contienen direcciones de memoria principal de datos e instrucciones,
o una parte de la dirección que se utiliza en el cálculo de la dirección
efectiva o completa.
•Estos registros pueden ser en sí mismos de propósito general, o
pueden estar dedicados a una forma, o modo, particular de
direccionamiento de memoria.
•Cómo estos registros pueden ser utilizados para diferentes
propósitos dependiendo de la necesidad del programa o del modo de
operación del procesador.

Registros GPR - Registros de
Dirección. Parte II
•Registros de Propósito General:
Descripción: Estos registros pueden ser utilizados para una
variedad de operaciones. No están limitados a un solo uso
específico.
•Registros Dedicados a una Forma o Modo Particular de
Direccionamiento de Memoria:
Descripción: Para algunas arquitecturas estos modos de
direccionamiento determinan cómo se calculan las direcciones de
memoria y cómo se accede a los datos almacenados en esas
direcciones.

Registros GPR - Registros de
Dirección. Parte III
•En resumen, estos registros pueden ser en sí mismos de
propósito general, o pueden estar dedicados a una forma, o
modo, particular de direccionamiento de memoria.
•Algunos ejemplos de Registro de Dirección son:
1.Registro de Índice
2.Puntero de Segmento
3.Puntero de Pila

- Registro de Índice
•Un registro índice es un registro especial en la CPU que almacena un valor
numérico llamado índice. Este valor es utilizado para modificar la dirección base y
acceder a diferentes posiciones de memoria de manera flexible.
•El registro índice se utiliza principalmente en operaciones que requieren acceso
secuencial a datos en memoria, como recorrer arrays, listas, o estructuras de
datos similares.

1ª - Registro Índice – Direccionamiento indexado
•El direccionamiento indexado es un modo de direccionamiento en el cual
se obtiene la dirección efectiva de memoria sumando un valor de base
(generalmente almacenado en un registro) con el valor almacenado en un
registro índice.
•Fórmula:
DirecciónEfectiva=DirecciónBase+(Índice × Tamañodecadaelemento)

Ejercicio – Cálculo de la Dirección Efectiva
•Se necesita acceder al tercer elemento del array (que tiene el valor 30).
1.Dirección Base: La dirección del primer elemento del array es 1000.
2.Índice: El índice sería 2 (ya que el primer elemento es el índice 0).
3.Tamaño de cada elemento: Cada entero ocupa 4 bytes.
•La fórmula para calcular la dirección efectiva será:
DirecciónEfectiva= DirecciónBase+( Índice ×Tamañodecadaelemento)
DirecciónEfectiva=1000+(2×4)=1000+8=1008

## Ejemplo - Registro Índice
•Array: Supongamos que tienes un array almacenado en la memoria y quieres acceder a
diferentes elementos de ese array.
•Base: La dirección de inicio del array se almacena en un registro, por ejemplo, en un
Registro de Base.
•Índice: El número de la posición (offset) en el array que deseas acceder se almacena en
un Registro Índice.
•Acceso: Para acceder al tercer elemento del array, el sistema suma la dirección base del
array (la dirección del primer elemento) con el valor del registro índice multiplicado por el
tamaño de un elemento (por ejemplo, si los elementos son de 4 bytes, el índice sería 2
para acceder al tercer elemento).
•Resultado: El resultado de esta suma es la dirección efectiva en la memoria donde se
encuentra el tercer elemento del array.

Ventajas del Direccionamiento
## Indexado
•Acceso Secuencial: Facilita el acceso secuencial a estructuras de
datos, como arrays y tablas, ya que solo necesitas modificar el valor
en el registro índice para recorrer diferentes elementos.
•Flexibilidad: Permite manipular datos en memoria de forma eficiente,
sin necesidad de recalcular manualmente cada dirección de memoria.
•Optimización: En operaciones repetitivas, como bucles que recorren
un array, este modo de direccionamiento simplifica y acelera el
acceso a elementos consecutivos.

## Aplicaciones Comunes
•Recorrido de Arrays: Ideal para iterar sobre elementos de un array,
donde cada elemento se encuentra en una dirección de memoria
secuencial.
•Tablas de Búsqueda: Usado en tablas donde las entradas están
almacenadas secuencialmente, permitiendo un acceso rápido a
cualquier entrada.
•Manejo de Matrices: Facilita el acceso a elementos de una matriz
mediante la suma de un índice a la dirección base de la matriz.

- Registros de Dirección -
Puntero de segmento.
•Este esquema organiza la memoria principal de una
computadora en bloques llamados segmentos, cada
uno de los cuales contiene un grupo de datos o
instrucciones.

¿Qué es la segmentación de
memoria?
•Segmentación es una técnica utilizada en sistemas operativos y
arquitecturas de computadoras para gestionar y acceder a la
memoria de manera más eficiente y estructurada.
•En lugar de tratar toda la memoria como un único bloque lineal y
continuo de direcciones (como ocurre en el direccionamiento lineal),
la segmentación divide la memoria en segmentos.

Tipos de segmento
•Un segmento es un bloque de memoria de tamaño variable que se dedica a
almacenar un conjunto específico de datos o instrucciones. Los segmentos
pueden variar en tamaño y se utilizan para separar diferentes tipos de
información en la memoria.
•Código (Texto): Segmentos que contienen las instrucciones del programa
que deben ser ejecutadas por la CPU.
•Datos: Segmentos que contienen datos globales, estructuras de datos,
variables, etc.
•Pila (Stack): Segmentos que se utilizan para la pila de ejecución, donde se
almacenan datos temporales como direcciones de retorno, parámetros de
funciones, y variables locales.

¿Cómo Funciona la Segmentación?
•Direccionamiento: Para acceder a una ubicación en memoria, el
sistema utiliza dos componentes:
1.Número de Segmento: Identifica cuál de los segmentos de
memoria se va a utilizar.
2.Desplazamiento: Indica la posición exacta dentro del
segmento a la que se desea acceder.
•Cálculo de Direcciones: La dirección efectiva de un dato o
instrucción se calcula sumando la dirección base del segmento
(que se encuentra en un registro de segmento) al
desplazamiento dentro de ese segmento.

Ventajas de la Segmentación
•Organización Lógica: Permite una mejor organización y protección
de la memoria, ya que diferentes partes de un programa (código,
datos, pila) pueden estar en segmentos separados.
•Protección: Cada segmento puede tener sus propias propiedades de
protección (por ejemplo, solo lectura, lectura/escritura), lo que mejora
la seguridad.
•Flexibilidad en la Gestión de Memoria: Como los segmentos son de
longitud variable, se pueden ajustar dinámicamente para adaptarse a
las necesidades del programa y del sistema operativo.

## Ejemplo Práctico – Segmentación
de Datos
•Supongamos que un programa está compuesto por un segmento
para su código, otro segmento para sus datos, y un tercero para su
pila. Si el programa necesita más memoria para los datos, el
segmento de datos puede expandirse sin afectar a los otros
segmentos, como el código o la pila.

- Puntero de pila
•Es un registro especial en la CPU y fundamental en la arquitectura de las
computadoras, se utiliza para gestionar y acceder a la pila (o stack) de la
memoria para almacenar datos temporales.
•La pila está ubicada en la memoria RAM y suele crecer o decrecer hacia
direcciones de memoria más bajas o más altas, dependiendo de la arquitectura
de la CPU.

Operaciones Principales con el
Puntero de Pila
1.Push (Empujar)
•Qué es: Almacenar un dato en la cima de la pila.
•Proceso: El puntero de pila se ajusta (decrece o incrementa, dependiendo de
la arquitectura) para apuntar a una nueva dirección, y luego el dato se
almacena en esa ubicación.
2.Pop (Sacar)
•Qué es: Recuperar (o quitar) el último dato almacenado en la pila.
•Proceso: El dato se lee desde la ubicación actual apuntada por el puntero de
pila, y luego el puntero se ajusta (incrementa o decrece) para reflejar la nueva
cima de la pila.

Ejemplo de Uso del Puntero de
## Pila
•Llamadas a Subrutinas: Cuando una subrutina es llamada, la dirección de
retorno (la dirección a la que el programa debe volver después de completar
la subrutina) se empuja a la pila. Al finalizar la subrutina, esta dirección se
recupera (se saca) de la pila para regresar el control a la parte adecuada del
programa.
•Almacenamiento de Variables Locales: Durante la ejecución de una función
o procedimiento, las variables locales a esa función pueden almacenarse en
la pila. Esto es especialmente útil para manejar la recursión, donde cada
llamada a una función puede tener su propio conjunto de variables locales
almacenadas en diferentes partes de la pila.

Importancia del Puntero de Pila
•Manejo de Funciones y Procedimientos: El puntero de pila es crucial
para el manejo correcto de llamadas a funciones, ya que permite que
las funciones manejen sus propias variables locales y direcciones de
retorno de manera segura y aislada.
•Seguridad: Al mantener un control estricto sobre el acceso a la pila,
el puntero de pila ayuda a evitar errores como desbordamientos de
pila (stack overflow), que pueden llevar a comportamientos
inesperados o fallos del programa.

Arquitectura CPU

Arquitectura de los Registros
AX, AH, AL (Acumulador):a menudo conserva el
resultado temporal después de una operación
aritmética o lógica.
BX, BH, BL (Base):Se utiliza para guardar la
dirección base de listas de datos en la memoria.
CX, CH, CL (Contador):Contiene el conteo para
ciertas instrucciones de corrimientos y
rotaciones, de iteraciones en el ciclo loop y
operaciones repetidas de cadenas.
DX, DH, DL (Datos):Contiene la parte más
significativa de un producto después de una
multiplicación; la parte más significativa del
dividendo antes de la división.

Resumen - Dirección Efectiva con Desplazamiento
(Base + Desplazamiento)
•Es un modo de direccionamiento en el cual la dirección física o lógica de un
dato en memoria (Dirección Efectiva, EA) se obtiene sumando una
dirección base fija y un valor de desplazamiento (también llamado offset).
EA = Base + Desplazamiento
## Ejemplo:
Supongamos un array de 15 elementos, cada uno de 4 bytes, cuyo primer
elemento comienza en la dirección 3000. Calcula la dirección efectiva para
el octavo elemento utilizando el direccionamiento con desplazamiento.
•Cálculo del desplazamiento:
EA=Base+Desplazamiento
## (8−1)×4=7×4=28.(8-1)
Suma a la base: 3000 + 28 = 3028.

Resumen II
EA=DirecciónBase+(Índice × Tamañodelelemento)
•El direccionamiento indexado es un modo de direccionamiento en el que la Dirección
Efectiva (EA) se calcula sumando:
EA=DirecciónBase+(Índice × Tamañodelelemento)
•Ejemplo:
Dado un array de 20 elementos de 8 bytes cada uno, y sabiendo que la dirección base es
5000, utiliza el direccionamiento indexado para calcular la dirección efectiva del quinto
elemento.
## Desplazamiento: (5−1)×8=4×8=32
Dirección efectiva: 5000+32=5032.
•Si el índice se cuenta desde 1** (más común en enunciados académicos):
EA=Base+((Posiciónelemento−1)×Tamañoelemento)

Resumen III - Registro índice
•Un registro índice es un registro especial de la CPU que se utiliza para modificar o
calcular la dirección efectiva (EA) de una instrucción, especialmente cuando
trabajamos con arreglos, tablas o estructuras de datos.
•Fórmula General
퐸퐴=DirecciónBase+(RegistroÍndice × Tamañodelelemento)
•En algunos procesadores, el registro índice ya almacena el desplazamiento en bytes
y no es necesario multiplicar por el tamaño del elemento.
•Ejemplo
•Datos: base 4000, registro índice contiene 150 (se asume que es índice en número de elementos),
tamaño por elemento 2 bytes.
•Desplazamiento por el registro: 150×2=300.
•Dirección efectiva: 4000+300=4300.

Resumen IV - Dirección Relativa (PC +
## Desplazamiento)
•El direccionamiento relativo es un modo de direccionamiento en el que la
Dirección Efectiva (EA) se obtiene sumando un desplazamiento a la
dirección actual contenida en el contador de programa (PC).
EA= PC + Desplazamiento
•Es muy utilizado para instrucciones de salto (branching), llamadas a
funciones y control de flujo, ya que permite que el código sea independiente
de la ubicación en memoria.
Datos: PC = 1000, desplazamiento = 50 bytes.
Dirección efectiva: 1000+50=1050
•Nota: en implementaciones reales a veces se usa PC apuntando a la siguiente
instrucción y se suma además el tamaño de la instrucción; aquí usamos la definición
simple pedida.

Resumen V - Registro de Segmento
•En arquitecturas con segmentación de memoria, un registro de segmento
es un registro especial de la CPU que almacena la dirección base de un
segmento de memoria (código, datos, pila, etc.).
La Dirección Efectiva (EA) se obtiene sumando a esta base un
desplazamiento (offset) que indica la posición dentro del segmento.
EA=BasedelSegmento + Offset
•Ejemplo:
Datos: base de segmento = 12000
Desplazamiento dentro del segmento = 3500.
Dirección efectiva: 12000+3500=15500.
## Respuesta: 15500