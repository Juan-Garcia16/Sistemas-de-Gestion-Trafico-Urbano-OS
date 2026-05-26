

## Introducción
a los
## Sistemas
## Operativos
## Ing. Juan Andrés García Moreno

¿Qué es un
## Sistema
## Operativo?
Un sistema operativo es un
programa que controla la
ejecución de aplicaciones y
programas y que actúa como
interfaz entre las aplicaciones
y el hardware del computador.

Ubicación del SO
El programa con el que los usuarios
generalmente interactúan se
denomina shell, cuando está basado
en texto, y GUI (GraphicalUser
Interface; Interfaz gráfica de usuario)
cuando utiliza elementos gráficos o
iconos. En realidad, no forma parte
del sistema operativo, aunque lo
utiliza para llevar a cabo su trabajo.
El SO se ejecuta directamente sobre
el hardware y proporciona la base para
las demás aplicaciones de software.

## Objetivos
Principales de un
## Sistema Operativo
•Facilidad de uso: Un sistema operativo
facilita el uso de un computador.
•Eficiencia: Un sistema operativo permite
que los recursos de un sistema de
computación se puedan utilizar de una
manera eficiente.
•Capacidad para evolucionar: Un sistema
operativo se debe construir de tal forma que
se puedan desarrollar, probar e introducir
nuevas funciones en el sistema sin interferir
con su servicio.

Programa de interfaz de usuario, shell o GUI
Es el nivel más bajo del software en modo
usuario y permite la ejecución de otros
programas, como un navegador Web, lector
de correo electrónico o reproductor de
música. Estos programas también utilizan
en forma intensiva el sistema operativo.

## Distinciones Importantes
•Una distinción importante entre el sistema operativo y el software que se ejecuta
en modo usuario es que, si a un usuario no le gusta, por ejemplo, su lector de
correo electrónico es libre de conseguir otro o incluso escribir el propio si así lo
desea; sin embargo, no es libre de escribir su propio manejador de interrupciones
de reloj, que forma parte del sistema operativo y está protegido por el hardware
contra cualquier intento de modificación por parte de los usuarios.
•Algunas veces esta distinción no es clara en los sistemas integrados (a los que
también se conoce como integrados o incrustados, y que podrían no tener modo
kernel) o en los sistemas interpretados (como los sistemas operativos basados en
Java que para separar los componentes utilizan interpretación y no el hardware).

¿Qué es el reloj de la CPU?
Por ejemplo, si una
CPU tiene una
frecuencia de reloj de
3.0 GHz, eso significa
que realiza 3 mil
millones de ciclos por
segundo.
El reloj de la CPU es un
oscilador que genera
pulsos de señal a una
frecuencia específica, y
estos pulsos son los que
sincronizan las
operaciones dentro del
procesador.

Función del reloj de la CPU
El reloj de la CPU tiene la tarea de marcar el ritmo de las operaciones dentro
del procesador. Cada pulso del reloj permite que la CPU realice una operación
básica, como mover datos, realizar cálculos o acceder a la memoria. A mayor
frecuencia de reloj, mayor es la cantidad de operaciones que la CPU puede
realizar en un segundo.
Por ejemplo:
Una CPU con una frecuencia de reloj de 3.0 GHz puede realizar 3 mil
millones de ciclos por segundo.

Importancia del reloj de la CPU
Rendimiento: La frecuencia del reloj es un factor determinante
del rendimiento de una CPU. En general, cuanto mayor es la
frecuencia de reloj, mayor es el rendimiento de la CPU, ya que
puede realizar más operaciones en menos tiempo.
Sincronización: El reloj asegura que todas las partes del
procesador operen de manera sincronizada. Esto es crucial para la
correcta ejecución de las instrucciones y la transferencia de datos
entre diferentes componentes de la CPU.
Relación con el Overclocking: El reloj de la CPU puede ser
ajustado para aumentar su frecuencia, práctica conocida como
overclocking.

¿De puede
modificar el
reloj de la
## CPU?
Es posible modificar el reloj de
la CPU, un proceso conocido
como overclocking. Este
procedimiento implica
aumentar la frecuencia de reloj
del procesador para mejorar su
rendimiento.

¿Qué es el
overclocking?
Consiste en aumentar la frecuencia de reloj de la
CPU (o de otros componentes como la GPU) más
allá de sus especificaciones oficiales para
incrementar el rendimiento.
Al aumentar la frecuencia de reloj, la CPU puede
ejecutar más ciclos por segundo, lo que
generalmente resulta en un rendimiento más
rápido.
https://www.youtube.com/watch?v=FTsgao_GPIs
## Consideraciones
Latencia: Aunque una mayor
frecuencia de reloj puede
significar un mejor rendimiento,
la cantidad de núcleos también
juegan un papel crucial en el
rendimiento general de la CPU.
Energía y Calor: A medida que
aumenta la frecuencia de reloj,
la CPU consume más energía y
genera más calor, lo que
requiere soluciones de
enfriamiento adecuadas para
evitar el sobrecalentamiento.

Estructura de
un Sistema
## Operativo
Se refiere a la forma en que sus componentes
están organizados y cómo interactúan entre sí
para gestionar los recursos de hardware y
software en un sistema informático. Las
principales estructuras de un sistema
operativo son:
1.Monolítico
2.Sistema en capas
3.Sistema con microkernel (micronúcleo)


1.Monolítico.
Todo el sistema operativo se ejecuta como un solo programa en modo
kernel. Está compuesto por un solo gran módulo o un conjunto de
módulos altamente interdependientes. Todas las funciones del sistema
operativo (gestión de procesos, memoria, I/O, etc.) están incluidas en
un único programa en espacio de núcleo (kernel).
Ventajas: Alta eficiencia y rendimiento, ya que todas las funciones
pueden comunicarse directamente entre sí.
Desventajas: Difícil de mantener y depurar, ya que cualquier cambio
puede afectar a todo el sistema.
Ejemplos de estos sistemas
pueden ser MS-DOS o Linux
(aunque incluye algo de
capas). Es importante tener en
cuenta que ningún sistema es
puramente de un tipo.

Componentes de una
estructura monolítica
- Un programa principal que invoca el
procedimiento de servicio solicitado.
- Un conjunto de procedimientos de servicio que
llevan a cabo las llamadas al sistema.
- Un conjunto de procedimientos utilitarios que
ayudan a los procedimientos de servicio.
Cada llamada al sistema hay un procedimiento de
servicio que se encarga de la llamada y la ejecuta.
Los procedimientos utilitarios hacen cosas que
necesitan varios procedimientos de servicio, como
obtener datos de los programas de usuario.

- Sistema en capas
El diseño se organiza en una jerarquía de capas,
donde los servicios que brinda una capa son
consumidos solamente por la capa superior.
La capa más baja (0) interactúa directamente con
el hardware, mientras que la capa más (N) alta
proporciona la interfaz de usuario (procesos de
## Usuario).
Ventajas: Diseño modular y simplificación en la
depuración, ya que los problemas en una capa no
afectan a las demás.
Desventajas: El diseño en capas puede introducir
sobrecargas adicionales y puede no ser tan
eficiente como otros enfoques.

Ejemplo de un sistema en capas – Sistema THE
Construido en Technische Hogeschool Eindhoven en Holanda por E. W.
Dijkstra (1968) y sus estudiantes.
El sistema tenía seis capas:
Capa 0 el nivel 0 proporcionaba la multiprogramación básica de la CPU
Capa 1 asignaba espacio para los procesos en la memoria principal y en
un tambor de palabras de 512K.
Capa 2 se encargaba de la comunicación entre cada proceso y la consola
del usuario, cada proceso tenía su consola.
Capa 3 se encargaba de administrar los dispositivos de E/S y de guardar en
búferes los flujos de información dirigidos para y desde ello.
Capa 4 se encontraban los programas de usuario. No tenían que
preocuparse por la administración de los procesos, la memoria, la consola
o la E/S.
Capa 5 gestionaba las interacciones y comandos del operador del
sistema, permitiendo la supervisión y control de las operaciones del
sistema operativo.

Sistema con
## Microkernel
La idea básica detrás del diseño de microkernel es lograr
una alta confiabilidad al dividir el sistema operativo en
módulos pequeños y bien definidos, sólo uno de los cuales
(el microkernel) se ejecuta en modo kernel y el resto se
ejecuta como procesos de usuario ordinarios.
Ventajas: Mayor modularidad, seguridad y estabilidad, ya
que los servicios adicionales no afectan directamente al
núcleo.
Desventajas: Puede haber una disminución en el
rendimiento debido a la sobrecarga en la comunicación
entre el núcleo y los servicios.
Estructura del sistema MINIX 3