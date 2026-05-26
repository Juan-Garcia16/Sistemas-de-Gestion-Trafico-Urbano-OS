

## Memoria
## Virtual
## Ing. Juan Andrés García Moreno

## Memoria Virtual
+La memoria virtual es una técnica de administración de memoria que
permite a los sistemas operativos utilizar más memoria de la que está
físicamente disponible, mediante el uso de un área de almacenamiento
secundario, como el disco duro. Esto permite que los programas se
ejecuten, aunque requieran más memoria de la que tiene el sistema,
mejorando la eficiencia y multiprogramacióndel sistema.
+Es una técnica de gestión de memoria que permite que el sistema
operativo y los programas usen más memoria de la que físicamente está
disponible en el equipo. Esto se logra utilizando una combinación de
memoria RAMy almacenamiento secundario(como el disco duro o
SSD), que funciona como una extensión de la memoria principal.

Analogía sencilla
+Comparar la memoria virtual con un escritorio y un archivador.
La RAMes el escritorio, donde se colocan los documentos que
se necesitan en el momento. El disco duroes como un
archivador: tiene una gran capacidad, pero es más lento
acceder a él. La memoria virtual permite mover documentos del
escritorio al archivador cuando no se usan activamente,
liberando espacio para otros documentos importantes.

Beneficios de la Memoria Virtual
1.Permite la ejecución de programas grandes:
+Programas que requieren más memoria que la disponible en la RAM pueden ejecutarse gracias a la memoria
virtual, que carga solo las partes necesarias en un momento dado.
2.Optimización del uso de la RAM:
+Con memoria virtual, el sistema no necesita almacenar programas completos en la RAM, sino solo las secciones
que se están usando, lo que maximiza el uso eficiente de la memoria física disponible.
3.Multiprogramación y rendimiento:
+La memoria virtual facilita la multiprogramación, permitiendo que múltiples procesos estén en ejecución y
compartan los recursos de memoria sin interferencias. El sistema puede ejecutar varias aplicaciones
simultáneamente al administrar la memoria de forma dinámica.
4.Protección y aislamiento:
+La memoria virtual proporciona aislamiento entre procesos. Cada proceso tiene su propio espacio de
direcciones virtual, lo que impide que un proceso pueda acceder a la memoria de otro. Esto aumenta la seguridad
y la estabilidad del sistema.

Ejemplos de Uso Práctico
•Edición de video: En aplicaciones de edición de video, los archivos
pueden ser muy grandes. La memoria virtual permite trabajar con
archivos mayores a la capacidad de la RAM, cargando solo las
partes que se necesitan en el momento.
•Videojuegos: Los videojuegos con mundos abiertos utilizan
memoria virtual para cargar áreas específicas del mapa conforme el
jugador se mueve, en lugar de cargar todo el entorno a la vez.
•Multitarea: Cuando varios programas están abiertos en una
computadora, la memoria virtual permite cambiar entre ellos sin que
todos ocupen espacio en la RAM al mismo tiempo.

Propósito de la Memoria Virtual
+La memoria virtual permite a los programas utilizar un espacio
de direcciones mayor que la memoria física. Divide el espacio
en bloques (páginas), que se cargan en la memoria principal
solo cuando se necesitan. Esto se llama paginación bajo
demanda.

## Ejemplo
+Imagina que tienes un programa que necesita 4 GB de
memoria, pero el sistema solo tiene 2 GB de RAM. Gracias a la
memoria virtual, el sistema carga solo las partes del programa
que se están utilizando, almacenando el resto en el disco. A
medida que el programa usa otras secciones, el sistema
intercambia esas partes desde y hacia la memoria.

## Paginación Bajo Demanda
+La paginación bajo demandaes una técnica que solo carga
en la memoria las páginas necesarias para la ejecución
inmediata. Si una página no está en la memoria y se necesita,
se produce un fallo de páginay el sistema la carga desde el
disco.
+Ejemplo: Editor de Texto

## Ejemplo
+Un editor de texto solo carga en memoria las partes del
documento que estás viendo o editando, mientras que el resto
se guarda en el disco. Si haces scrolla otra parte del
documento, el sistema carga esas páginas en la memoria.

Rendimiento de la Paginación Bajo
## Demanda
+El rendimiento depende de la frecuencia de fallos de página.
Un número elevado de fallos ralentiza el sistema, mientras que
una buena predicción reduce los tiempos de espera.

## Ejemplo
+En un videojuego, las partes del mapa que no estás viendo se
cargan bajo demanda. Si hay muchas fallas de página (cambio
frecuente entre partes del mapa), el rendimiento del juego
disminuye, causando retrasos.

Copia Durante la Escritura
+La copia durante la escriturapermite que los procesos
compartan páginas de memoria hasta que uno de ellos
necesite modificarlas. Entonces, se crea una copia de la página
para el proceso que la necesita, ahorrando así memoria y
mejorando el rendimiento.

## Ejemplo
+Al abrir un documento en modo lectura, todos los usuarios ven
la misma página de memoria. Si alguien hace una modificación,
el sistema crea una copia de esa página solo para el usuario
que realizó el cambio, permitiendo que los demás sigan viendo
el original.

Sustitución de Páginas
+Cuando no hay suficiente memoria para todas las páginas activas, el
sistema debe decidir qué página reemplazar. Existen varios algoritmos
de sustitución de páginaspara optimizar esta decisión.
+Sustitución Básica de Páginas
+Sustitución de Páginas FIFO
+Sustitución Óptima de Páginas
+Sustitución de Páginas LRU
+Sustitución de Páginas Mediante Aproximación
## LRU
+Algoritmo de los Bits de Referencia Adicionales
+Algoritmo de Segunda Oportunidad
+Algoritmo Mejorado de Segunda Oportunidad
+Sustitución de Páginas Basada en Contador
+Algoritmos de Búfer de Páginas
+Aplicaciones y Sustitución de Páginas

Sustitución de Páginas FIFO
+FIFO (First In, First Out) reemplaza la página que lleva más
tiempo en memoria, independientemente de si se ha usado
recientemente.
+Ejemplo: Imagina una fila de libros en un estante. El primer
libro en entrar es el primero en salir cuando llega uno nuevo.

Sustitución Óptima de Páginas
+Óptimo reemplaza la página que no será usada en el futuro
más cercano, aunque es teórico ya que requiere conocer el
acceso futuro.
+Ejemplo: Supón que sabes qué libros usarán los estudiantes
en las próximas semanas. Puedes eliminar el libro que nadie
necesitará pronto.

Sustitución de Páginas LRU
+LRU (Least Recently Used) reemplaza la página que no se ha
utilizado durante el mayor tiempo.
+Ejemplo: Imagina una pila de documentos. El documento que no has
consultado en mucho tiempo se coloca al final y se descarta primero
cuando necesitas espacio.

+Sustitución de Páginas Mediante Aproximación LRU
+Para implementar LRU, se utilizan aproximaciones que reducen el costo
computacional.
+Algoritmo de los Bits de Referencia Adicionales
+Cada página tiene un bit que indica si ha sido referenciada. El sistema revisa estos
bits para decidir qué página reemplazar.
+Ejemplo: Cada libro tiene una marca que indica si fue consultado. El libro menos
marcado se reemplaza.
+Algoritmo de Segunda Oportunidad
+Resumen: Similar a FIFO, pero da una "segunda oportunidad" a las páginas
referenciadas recientemente.
+Ejemplo: Antes de quitar un libro, verificas si ha sido consultado. Si sí, lo colocas al
final de la fila.
+Algoritmo Mejorado de Segunda Oportunidad
+Resumen: Este algoritmo usa dos bits para ofrecer una mejora sobre la segunda
oportunidad.
+Ejemplo: Si un libro fue consultado hace poco y es popular, se le da prioridad para
quedarse en el estante.

Sustitución de Páginas Basada en
## Contador
+Cada página tiene un contador de veces que ha sido usada,
permitiendo reemplazar la página menos usada (LFU) o la más
antigua.
+Ejemplo: Un contador en cada libro registra su uso; el libro con
menor conteo se reemplaza.

Algoritmos de Búfer de Páginas
+Algunos sistemas utilizan un búfer que guarda páginas
recientemente reemplazadas, por si son requeridas de nuevo.
+ Ejemplo: Si quitas un libro, lo guardas en un estante temporal
en caso de que alguien lo necesite nuevamente.

Aplicaciones y Sustitución de Páginas
+En aplicaciones específicas, se adaptan los algoritmos para
maximizar el rendimiento según las necesidades de cada
sistema.
+Ejemplo: Un sistema de base de datos podría usar un
algoritmo de reemplazo más conservador, priorizando las
páginas que se usan frecuentemente.