

## Algoritmos
de
## Asignación
de Memoria
## Ing. Juan Andrés García Moreno

Algoritmos de Asignación y Reemplazo de
## Memoria
•En un sistema operativo es fundamental tener algoritmos eficientes
para asignar y reemplazar páginas o segmentos en la memoria.
•Estos algoritmos ayudan a decidir cómo asignar la memoria física
disponible y cómo gestionar el reemplazo de páginas cuando la
memoria se llena.

- Algoritmos de Asignación de Memoria
a.Asignación de Primer Ajuste (FirstFit)
b.Asignación de Mejor Ajuste (BestFit)
c.Asignación de Peor Ajuste (WorstFit)
d.Asignación de Ajuste Rápido (Quick Fit)

a. Asignación de Primer Ajuste (FirstFit)
•Este algoritmo busca el primer bloque de memoria libre que sea lo
suficientemente grande para el proceso o segmento. La asignación
se realiza en ese bloque, dejando el resto del espacio libre.
•Ventajas: Es rápido porque simplemente encuentra el primer espacio
adecuado.
•Desventajas: Puede producir fragmentación externaa medida que se dejan
pequeños espacios no utilizados.

b. Asignación de Mejor Ajuste (BestFit)
•Busca el bloque libre más pequeño que sea lo suficientemente
grande para el proceso. El objetivo es dejar el menor espacio libre
posible tras la asignación.
•Ventajas: Minimiza el desperdicio de memoria libre.
•Desventajas: Puede generar fragmentación externa más rápidamente, ya que
los pequeños espacios que deja son difíciles de reutilizar.

c. Asignación de Peor Ajuste (WorstFit)
•Elige el bloque libre más grande disponible, con la idea de que dividir
este bloque deje un fragmento suficientemente grande como para
que sea reutilizable.
•Ventajas: Reduce el número de pequeños bloques de memoria que no pueden
ser utilizados.
•Desventajas: A menudo desperdicia grandes bloques de memoria para
procesos pequeños.

d. Asignación de Ajuste Rápido (Quick Fit)
•Divide la memoria en listas de bloques de tamaños predefinidos y
asigna el proceso a un bloque de la lista correspondiente. Este
enfoque mejora el tiempo de búsqueda en sistemas donde se
asignan y liberan muchos procesos.
•Ventajas: Muy rápido en la asignación de memoria.
•Desventajas: Requiere reorganización si los bloques de memoria no se ajustan
perfectamente a los tamaños predefinidos.

- Algoritmos de Reemplazo de Memoria
•Cuando no hay suficientes marcos de página o segmentos
disponibles en la memoria física, el sistema operativo debe elegir una
página o segmento existente para eliminar y hacer espacio. Aquí es
donde entran en juego los algoritmos de reemplazo.
a.ReemplazoFIFO (First In, First Out)
b.ReemplazoLRU (Least Recently
## Used)
c.ReemplazoLFU (Least Frequently
## Used)
d.Reemplazo Aleatorio
e.Algoritmo Óptimo (OPT)
f.Reemplazo Clock (Reloj)

a. ReemplazoFIFO (First In, First Out)
•Este algoritmo elimina la página que fue cargada primero en la
memoria, independientemente de su uso reciente. La idea es
sencilla: las páginas se tratan en forma de cola.
•Ventajas: Fácil de implementar.
•Desventajas: No toma en cuenta qué páginas son más utilizadas, lo que puede
generar reemplazos innecesarios de páginas importantes.

b. ReemplazoLRU (Least Recently Used)
•Elimina la página que no ha sido utilizada por más tiempo. Se basa en
la idea de que las páginas que no se han usado en mucho tiempo
probablemente no se necesitarán en el futuro inmediato.
•Ventajas: Eficiente en situaciones en las que el acceso a las páginas sigue un
patrón predecible.
•Desventajas: Implementarlo de manera eficiente puede ser costoso en
términos de tiempo y recursos.

c. ReemplazoLFU (Least Frequently Used)
•Este algoritmo elimina la página que ha sido utilizada con menos
frecuencia. La suposición es que las páginas menos usadas
probablemente no se necesitarán pronto.
•Ventajas: Funciona bien cuando algunos datos se usan repetidamente,
mientras que otros solo se usan temporalmente.
•Desventajas: Pueden ocurrir problemas si una página fue usada intensamente
en el pasado, pero ya no es relevante.

d. Reemplazo Aleatorio
•Elige una página de manera completamente aleatoria para eliminarla.
Aunque no es un algoritmo eficiente en términos de rendimiento, es
muy fácil de implementar y puede ser útil en sistemas que no
necesitan precisión.
•Ventajas: Muy simple de implementar.
•Desventajas: Ineficiente, ya que no toma en cuenta patrones de uso.

e. Algoritmo Óptimo (OPT)
•Este es el algoritmo teóricamente más eficiente. Se basa en eliminar
la página que no será usada en el futuro por el mayor tiempo posible.
•Ventajas: Es el algoritmo más eficiente si se conoce con antelación qué
páginas se necesitarán.
•Desventajas: Es imposible de implementar en sistemas reales, ya que no se
puede predecir el futuro con exactitud.

f. Reemplazo Clock (Reloj)
•Es una mejora sobre el algoritmo FIFO. Cada página tiene un "bit de
uso" que se pone a 1 cuando la página es utilizada. El sistema
reemplaza páginas cuyo bit de uso es 0, y si encuentra una con bit 1,
lo cambia a 0 y sigue buscando.
•Ventajas: Eficiente en cuanto a tiempo de procesamiento y espacio.
•Desventajas: Puede no ser tan preciso como LRU o LFU en la elección de
páginas para reemplazar.

Hiperpaginación (Thrashing)
•La hiperpaginación es una condición que ocurre cuando un sistema
operativo pasa la mayor parte de su tiempo intercambiando páginas
entre la memoria y el disco en lugar de ejecutar procesos.
- Esto suele suceder cuando no hay suficientes marcos de página
disponibles para los procesos activos, lo que provoca que las
páginas se intercambien de manera constante.

Causas de la Hiperpaginación
•Falta de marcos suficientes: Si los procesos necesitan más páginas
de las que hay marcos disponibles en la memoria física, el sistema
comienza a intercambiar páginas de manera excesiva.
•Mala elección de reemplazo: Si el algoritmo de reemplazo de
páginas no es eficiente (por ejemplo, reemplazar páginas que se
necesitan de nuevo inmediatamente), el sistema caerá en un ciclo de
intercambio constante.
•Demasiados procesos activos: Ejecutar demasiados procesos
simultáneamente, todos compitiendo por la memoria, puede causar
hiperpaginación.

Soluciones para evitar la Hiperpaginación
•Ajustar el número de marcos asignados: Aumentar el número de marcos
de página por proceso puede ayudar a reducir la hiperpaginación.
•Reducir el número de procesos activos: Limitar el número de procesos
concurrentes puede liberar marcos de página y reducir la frecuencia de
intercambio.
•Algoritmos eficientes de reemplazo: Implementar algoritmos de
reemplazo que gestionen adecuadamente las páginas de manera eficiente
(como LRU o Clock) puede reducir la hiperpaginación.
•Control de carga del sistema: Reducir la carga del sistema ajustando el
número de procesos simultáneos y limitando la memoria utilizada por cada
proceso.