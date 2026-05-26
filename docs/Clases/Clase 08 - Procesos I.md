

## PROCESOSI
## SUBPROCESOS, IMPLEMENTACIÓN Y ASIGNACIÓN DE RECURSOS
## ING. JUAN ANDRÉS GARCÍA MORENO

## PROCESO
•Puede pensarse en un proceso como en un programa en
ejecución. Un proceso necesita ciertos recursos, como tiempo de
CPU, memoria, archivos y dispositivos de E/S para llevar a cabo su
tarea. Estos recursos se asignan al proceso en el momento de
crearlo o en el de ejecutarlo.

## RECURSOS UTILIZADOS EN
## LA EJECUCIÓN DE UN
## PROCESO
•Tiempos de la CPU
•Memoria de archivos
•Dispositivos E/S

## EJEMPLO EJECUCIÓN DE UN PROCESO
•Ejemplo: Considere un proceso cuya función sea la de mostrar el
estado de un archivo en la pantalla de un terminal. A este proceso
se le proporciona como entrada el nombre del archivo y el proceso
ejecutaría las apropiadas instrucciones y llamadas al sistema para
obtener y mostrar en el terminal la información deseada, luego,
cuando el proceso termina, el SO reclama los recursos
reutilizables.

## SUBPROCESO(THREAD)
•Un subprocesoo threades la unidad más pequeña de
procesamiento que puede gestionar un sistema operativo dentro
de un programa. Los subprocesos permiten que una aplicación
realice múltiples tareas de manera concurrente, lo que mejora la
eficiencia y la velocidad del procesamiento. Cada programa tiene
al menos un threadprincipal, pero puede tener varios threads
adicionales que se ejecutan simultáneamente.

## CARACTERÍSTICAS DE LOS SUBPROCESOS (THREADS):
1.Ejecución Concurrente:
•Los subprocesos permiten que diferentes partes de un programa se ejecuten de forma paralela o concurrente. Por
ejemplo, un navegador web puede usar un threadpara renderizar la página y otro para descargar datos en segundo
plano.
2.Compartición de Recursos:
•Los threads de un mismo proceso comparten la misma memoriay recursosdel proceso, como variables globales y
archivos abiertos. Esto permite una comunicación más rápida y eficiente entre los threads, en comparación con los
procesos separados, que no comparten memoria.
3.Contexto Ligero:
•A diferencia de los procesos completos, los subprocesos tienen un contexto de ejecución más ligero, lo que significa
que cambiar entre threads es más rápido que cambiar entre procesos, ya que no requieren la duplicación completa
de recursos.
4.Estados de un Subproceso:
•Un subproceso puede estar en los siguientes estados: Nuevo, Listo, Ejecutando, Esperando(bloqueado) o
Terminado. El sistema operativo gestiona los cambios de estado de los threads de manera similar a como lo hace
con los procesos.

## VENTAJAS DE LOS SUBPROCESOS
•Paralelismo:Los subprocesos permiten aprovechar los sistemas
multinúcleo, donde varias tareas pueden ejecutarse simultáneamente en
diferentes núcleos de CPU, lo que acelera el procesamiento.
•Eficiencia:Dado que los threads comparten la memoria del proceso
principal, la sobrecarga en la creación y administración de threads es
mucho menor que la de los procesos.
•Mejor Uso de Recursos:Permite que las aplicaciones realicen varias
tareas a la vez, como descargar archivos y realizar cálculos, sin bloquear
la interfaz de usuario.

## EJEMPLO DE USO DE SUBPROCESOS
•En un navegador web, diferentes subprocesos pueden encargarse
de tareas específicas:
•Thread1:Descarga contenido de una página web.
•Thread2:Renderiza el contenido descargado en la pantalla.
•Thread3:Maneja la interacción del usuario (clics,
desplazamientos).
•Todos estos subprocesos funcionan de manera independiente pero
colaboran para mejorar la eficiencia y la experiencia del usuario.

## TIPOS DE THREADS
•Threads a nivel de usuario (User-LevelThreads):
oGestionados por una biblioteca en espacio de usuario sin la intervención directa del sistema operativo.
Son más rápidos de crear y gestionar, pero pueden tener desventajas en términos de multitarea si el
sistema operativo no puede programarlos eficientemente.
•Threads a nivel de núcleo (Kernel-LevelThreads):
oGestionados directamente por el sistema operativo. Son más lentos de crear y gestionar en comparación
con los threads a nivel de usuario, pero permiten un mejor control y equilibrio entre los recursos del
sistema.

## DIFERENCIA ENTRE PROCESOS Y SUBPROCESOS
•Procesos:
oCada proceso tiene su propio espacio de direcciones, es decir, su propia memoria, lo
que hace que la comunicación entre procesos sea más lenta y costosa.
oCambiar entre procesos implica una mayor sobrecarga porque el sistema operativo
debe intercambiar los contextos completos de los procesos.
•Subprocesos (Threads):
oLos threads dentro de un mismo proceso comparten la misma memoria, lo que permite
una comunicación más rápida y eficiente.
oCambiar entre threads es más rápido porque el sistema operativo no tiene que cambiar
todo el contexto, solo parte de él.

## ESTADO DEL PROCESO
•Nuevo: el proceso está siendo
creado.
•En ejecución: se están ejecutando
las instrucciones.
•En espera: el proceso está
esperando a que se produzca un
suceso (como la terminación de
una operación de E/So la
recepción de una señal).
•Preparado: el proceso está a la
espera de que le asignen a un
procesador.
•Terminado: ha terminado la
ejecución del proceso.

## EJEMPLO DE INSTANCIA DE EJECUCIÓN DE UN PROCESO
1.Procesos y Memoria:
•La imagen muestra tres procesos
(A, B, y C) cargados en la
memoria principal, además de
un distribuidorque gestiona la
asignación de CPU a los
procesos.
•El procesadorejecuta
instrucciones de estos procesos
en una secuencia dictada por el
contador de programa, el cual
apunta a la instrucción que debe
ejecutarse en un momento dado.

## EJEMPLO DE INSTANCIA DE EJECUCIÓN DE UN PROCESO
-  Distribuidor y Trazas:
•El distribuidores un pequeño
programa que decide cuándo el
procesador cambia de un proceso a
otro, asegurando que cada proceso
reciba una cantidad justa de tiempo
de CPU.
•Los procesos se ejecutan durante un
tiempo limitado o hasta que se
requiera una operación de
entrada/salida (E/S). Si un proceso
debe esperar (como ocurre en el
proceso Bdespués de una
operación de E/S), el distribuidor
asigna la CPU a otro proceso.

## EJEMPLO DE INSTANCIA DE EJECUCIÓN DE UN PROCESO
## 3. Trazas:
•Una trazaes el listado de
todas las instrucciones
ejecutadas por un proceso. En
el caso del ejemplo, las trazas
de los procesos A, B, y Cestán
intercaladas para que el
procesador no esté inactivo
mientras un proceso espera
una operación de E/S.

## EJEMPLO DE INSTANCIA DE EJECUCIÓN DE UN PROCESO
- Ejecución por Time-Out:
•El sistema operativo impone un
límite de tiempo(time-out) de 6
ciclos de instrucciones por
proceso antes de pasar al
siguiente proceso. Esto evita que
un proceso monopolice la CPU.
•En el ejemplo, el proceso A
ejecuta sus 6 primeras
instrucciones, luego el distribuidor
asigna la CPU al proceso B. Tras
ejecutar 4 instrucciones, el
proceso Bespera una operación
de E/S, y entonces el distribuidor
asigna la CPU al proceso C.

## EJEMPLO DE INSTANCIA DE EJECUCIÓN DE UN PROCESO
- Secuencia de Ejecución:
•La secuenciade instrucciones
ejecutadas está determinada
por las trazas de cada proceso,
donde el distribuidor asegura
que todos los procesos tengan
acceso a la CPU sin
interrupciones largas. Si un
proceso aún está esperando,
el distribuidor avanza al
siguiente proceso listo para
ejecutarse.

## TIPOS DE RECURSOS
•La asignación de recursosen un sistema operativo es el proceso mediante el cual se distribuyen los recursos
disponibles entre los distintos procesos que lo requieren. Los recursos pueden ser físicoso lógicos, como el
tiempo de CPU, memoria, dispositivos de E/S, archivos, entre otros.
- Recursos de CPU:
•El procesadores uno de los recursos más críticos,
ya que es el encargado de ejecutar las instrucciones
de los procesos. Se asigna usando técnicas de
planificacióncomo round-robin, prioridades, o
multinivel.
- Memoria principal:
•Cada proceso necesita memoria para almacenar
instrucciones y datos. El gestor de memoriaes el
encargado de asignar y liberar espacio de memoria de
manera eficiente, evitando conflictos entre procesos.
- Dispositivos de E/S:
•Los procesos necesitan acceder a discos,
impresoras, redes, entre otros. El sistema operativo
controla el acceso a estos dispositivos, utilizando
técnicas de cola de esperao bloqueopara
garantizar que los recursos sean utilizados de forma
justa y eficiente.
## 4. Archivos:
•Los procesos pueden solicitar acceso a archivos
almacenados en el sistema de archivos. El sistema
operativo controla quién puede leer o escribir en
estos archivos mediante permisos y bloqueos.

## MECANISMOS DE ASIGNACIÓN DE RECURSOS
- Planificación del CPU:
➢El planificadordecide qué proceso obtiene
acceso a la CPU y por cuánto tiempo. En
sistemas de tiempo compartido, los procesos
alternan el uso de la CPU en intervalos
regulares, lo que garantiza que todos reciban
una porción del tiempo de ejecución.
- Asignación de memoria:
➢La memoria se asigna de varias maneras,
como particiones fijas, segmentación, o
paginación. Estos métodos aseguran que los
procesos tengan el espacio que necesitan sin
interferir entre ellos.
- Bloqueo y sincronización:
➢Cuando varios procesos compiten por el
mismo recurso, el sistema operativo utiliza
mecanismos de sincronizacióncomo
semáforoso bloqueospara garantizar que los
recursos se usen de forma ordenada y segura.
- Sistemas de archivos:
➢El sistema operativo utiliza permisos para
controlar el acceso a los archivos y evitar
conflictos entre los procesos que los utilizan
simultáneamente. Los archivos pueden
bloquearse para lectura o escritura.

## PROBLEMAS COMUNES EN LA ASIGNACIÓN DE
## RECURSOS
1.Interbloqueo (Deadlock):
➢Ocurre cuando un conjunto de procesos se queda esperando
indefinidamente por recursos que están siendo utilizados por otros
procesos del mismo conjunto. El sistema operativo debe implementar
algoritmos de prevención, detección y recuperación de deadlocks.
2.Inanición (Starvation):
➢Sucede cuando un proceso espera indefinidamente por un recurso debido a
que otros procesos con mayor prioridad lo acaparan continuamente.

## EJEMPLO DE ASIGNACIÓN DE RECURSOS:
•Si tenemos un sistema operativo que ejecuta múltiples aplicaciones, como un
navegador web y un editor de texto, ambos procesos requerirán tiempo de CPU,
memoria y acceso a discos. El sistema operativo será el encargado de gestionar estos
recursos y asegurar que ambos procesos puedan ejecutarse eficientemente sin
interferirse entre sí.
•La asignación de recursoses una tarea fundamental para garantizar que los procesos
en ejecución puedan funcionar correctamente, utilizando los recursos del sistema de
manera justa y evitando conflictos como deadlockso inanición.

## KAHOOTDEL TEMA