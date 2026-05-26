

## Protección
y
## Seguridad
## I N G .   J U A N   A N D R É S   G A R C Í A
## M O R E N O

## Protección
•Protección es cualquier mecanismo que controle el acceso de procesos y
usuarios a los recursos definidos por un sistema informático. Este
mecanismo debe proporcionar los medios para la especificación de los
controles que hay que imponer y para la aplicación de dichos controles.

Gestión de Protección
•Si un sistema informático tiene múltiples usuarios y permite la ejecución
concurrente de múltiples procesos, entonces el acceso a los datos debe
regularse. Para dicho propósito, se emplean mecanismos que aseguren
que sólo puedan utilizar los recursos (archivos, segmentos de memoria,
CPU y otros) aquellos procesos que hayan obtenido la apropiada
autorización del sistema operativo.

Ejemplo de Protección
•El hardware de direccionamiento de memoria asegura que un
proceso sólo se pueda ejecutar dentro de su propio espacio
de memoria; el temporizador asegura que ningún proceso
pueda obtener el control de la CPU sin después ceder el
control; los usuarios no pueden acceder a los registros de
control, por lo que la integridad de los diversos dispositivos
periféricos está protegida.

¿Qué son los Mecanismos Protección?
•El papel de la protección en un sistema informático es proporcionar un mecanismo
para la imposición de las políticas que gobiernen el uso de recursos.
•Estas políticas pueden establecerse de diversas formas. Algunas están fijas en el
diseño de un sistema, mientras que otras se formulan al administrar ese sistema.
•Hay otras políticas que son definidas por los usuarios individuales para proteger sus
propios archivos y programas. Un sistema de protección deberá tener la flexibilidad
suficiente para poder imponer una diversidad de políticas.
•Los mecanismos de protección pueden mejorar la fiabilidad, permitiendo detectar
errores latentes en las interfaces entre los subsistemas componentes. La detección
temprana de los errores de interfaz a menudo puede evitar la contaminación de un
subsistema que funciona perfectamente por parte de otro subsistema que funcione
mal.

Objetivos de la Protección
•Aislamiento de Procesos: Evitar que los procesos interfieran entre sí. Cada
proceso debe operar en su propio espacio de memoria y no debe acceder a la
memoria de otro proceso sin permiso.
•Control de Acceso: Limitar el acceso de los usuarios y procesos a los recursos.
Por ejemplo, garantizar que solo los usuarios autorizados puedan leer, escribir
o ejecutar archivos.
•Integridad de los Datos: Proteger la integridad de los datos almacenados y
garantizar que no puedan ser modificados sin permiso.

Ejemplo de Protección
•En un sistema operativo multiusuario, un usuario no debería poder acceder a los archivos o
programas de otro usuario a menos que tenga los permisos adecuados. Los permisos de acceso
para cada archivo o directorio se definen en una tabla de permisos.

Dominio de Protección
•El dominio de protecciónes un concepto clave en los sistemas
operativos que define el conjunto de recursos(como archivos,
dispositivos, segmentos de memoria) y permisos(como lectura,
escritura, ejecución) a los que un usuario, proceso o programa tiene
acceso. En otras palabras, un dominio de protección especifica qué
operaciones pueden realizar los sujetos (usuarios o procesos) sobre los
objetos (recursos) del sistema.

Concepto de Dominio de Protección
•Dominio: Es un conjunto de pares (objeto, operación) que especifica qué operaciones un sujeto
puede realizar sobre los objetos del sistema.
•Sujeto: Puede ser un usuario, proceso o programa.
•Objeto: Puede ser cualquier recurso del sistema, como archivos, impresoras, memoria,
dispositivos de E/S, etc.
•Operación: Define las acciones que se pueden realizar sobre el objeto, como lectura,
escritura, ejecución o modificación.
•Cada proceso o usuario tiene un dominio de protección que define los recursos a los que puede
acceder y qué operaciones puede realizar sobre ellos. El sistema operativo asegura que cada
sujeto esté limitado a los recursos y acciones especificados en su dominio de protección.

Ejemplo de Dominio de Protección
•Imagina un sistema con dos usuarios: Usuario Ay Usuario B. Ambos usuarios tienen acceso a diferentes archivos
en el siste ma. Los dominios de protección definen qué  archivos puede ver, modificar o ejecutar cada usuario.
1.Usuario A:
•Puede leer y escribir en Archivo 1.
•Puede solo leer Archivo 2.
•No tiene acceso a Archivo 3.
2.Usuario B:
•Puede leer y escribir en Archivo 2.
•Puede leer y ejecutar Archivo 3.
•No tiene acceso a Archivo 1.

Características del Dominio de
## Protección
1.Aislamiento:
•Los dominios de protección permiten aislar procesos y usuarios, evitando que un proceso interfiera
con los recursos de otro. Esto es fundamental para garantizar la seguridad y la estabilidad del
sistema.
2.Control de Acceso:
•El dominio de protección define un control de accesoque garantiza que solo los usuarios o procesos
autorizados puedan acceder o modificar ciertos recursos.
3.Cambio de Dominio:
•En algunos sistemas, un proceso o usuario puede cambiar de dominio, por ejemplo, cuando un
usuario ejecuta un programa con privilegios de administrador (como en UNIX con el comando sudo),
lo que cambia el dominio de protección y le otorga permisos adicionales.

Representación del Dominio de Protección
•El dominio de protección puede representarse mediante una matriz de acceso o una lista de
control de acceso (ACL):

Tipos de Dominios de Protección
1.Dominio de Usuari o:
•Cada usuario tiene un conjunto de perm isos que define a qué recursos del sistema puede
acceder y qué puede hacer con ellos.
2.Dominio de Proceso:
•Cada proceso ejecutándose en el sistema tiene su propio dominio de protección, que puede
estar basado en los permisos d el usuario q ue ejecuta el proceso.
3.Dominio de Sistema Operativo:
•Los p rocesos q ue form an p arte del sistem a op erativo suelen tener un dominio de protección
especial, con acceso privilegiado a todos los recursos del sistema.

Cambio de Dominio de Protección
•En algunos sistemas, los procesos pueden cambiar de dominio de protección cuando es
necesario, por ejemplo:
•Un proceso en un dominio de usuario puede solicitar privilegios adicionales (como el modo
superusuarioen UNIX/Linux) para realizar ciertas operaciones administrativas.
•Esto se hace mediante mecanismos como llamadas al sistemao la ejecución de programas
con privilegios elevados.

Ejemplo de Dominio de Protección en
UNIX/Linux
•En sistemas UNIX/Linux, los archivos tienen tre s tipos de permisos:
1.Propiet ario: Permisos asignados al propietario del archivo.
2.Grupo: Permisos para los miembros del grupo de l archivo.
3.Otros: Permisos para cualquier otro usuario del sistema.
•Los permisos se definen para cada tipo de usuario (propietario, grupo, otros) y las operaciones pe rmitidas son
lectura (r), escritura (w)y ejecución (x).
•Esto significa que:
•El propietariopuede leer, escribir y ejecutar el archivo.
•Los miembros del grupopueden leer y ejecutar el archivo.
•Otrosusuarios solo pueden leer e l archivo.

Importancia del Dominio de
## Protección
1.Seguridad:
•Evita que procesos o usuarios no autorizados accedan o modifiquen recursos sensib les del
sistema, com o archivos importantes, memoria del sistema o dispositivos d e E/S.
2.Estabilidad del Sistema:
•El aislamiento entre dominios evita que un error en un proceso afecte a otros procesos o al
sistema en su totalidad.
3.Mantenimi ento del Control de Recursos:
•Permite al sistema operativo tener un control granular sobre quién o q ué p uede acced er a cada
recurso y cómo lo pued e hacer, previniendo el abuso de los recursos del sistema.

## Seguridad
•La seguridaden un sistema operativo va más allá de la protección y se enfoca en prevenir
amenazas internas y externas que pueden comprometer la integridad, confidencialidad y
disponibilidad de los recursos y datos. La seguridad se encarga de proteger el sistema
operativo y los datos contra ataques como el malware, acceso no autorizado, pérdida de datos,
entre otros.

Objetivos de la Seguridad
•Confidencialidad:Garantizar que la información solo sea accesible por las
personas o sistemas autorizados.
•Integridad:Asegurar que los datos no se alteren o modifiquen sin autorización.
•Disponibilidad:Asegurar que los recursos y datos estén disponibles para los
usuarios autorizados cuando los necesiten.
•Autenticidad:Verificar la identidad de los usuarios y procesos para evitar
suplantación.

¿Cuáles son los Mecanismos de seguridad?
1.Modos de Operación:La CPU generalmente tiene al menos dos modos de operación:
•Modo usuario:Para ejecutar aplicaciones de los usuarios.
•Modo kernelo supervisor:Para las operaciones críticas del sistema operativo. Los
procesos de usuario no pueden acceder directamente a recursos protegidos (como
dispositivos o áreas de memoria reservadas) sin pasar por el sistema operativo.
2.Tablas de Acceso (Access Control Lists, ACL):Cada recurso (archivo, dispositivo,
etc.) tiene una lista que define qué usuarios o procesos pueden realizar qué tipo de
operaciones (lectura, escritura, ejecución).
3.Matriz de Acceso:Estructura que define qué acciones puede realizar cada usuario o
proceso sobre qué recursos. Es una matriz donde las filas representan sujetos
(usuarios o procesos) y las columnas representan objetos (recursos del sistema).

Ejemplo de Seguridad
•Supongamos que una empresa tiene un sistema operativo que
protege archivos confidenciales.
•Para acceder a estos archivos, los empleados deben
autenticarse utilizando una contraseña y, posteriormente, tener
permisos específicos para leer o modificar los archivos.
Además, todos los archivos se almacenan cifrados para que, si
son robados, los atacantes no puedan leer la información sin la
clave de descifrado.

Relación entre Protección y
## Seguridad
•Protecciónse enfoca en controlar el accesoa los recursos del sistema
y en garantizar que solo los usuarios o procesos autorizados puedan
interactuar con estos recursos de manera controlada.
•Seguridadse enfoca en protegerel sistema contra ataques externos y
amenazas internas, asegurando la integridad, confidencialidad y
disponibilidad de los datos y recursos.

Ejemplos Reales de Protección y
## Seguridad
1.Protecci ón en un Sistema de Archivos (Protección):
•Un sistema operativo puede definir permisos de lectura, escritura y ejecución para cada archivo.
Los usuarios comunes pueden tener permisos solo para leer ciertos archivos, mientras que los
administrad ores tienen permisos de lectura y escritura.
2.Seguridad en Redes Empresariales (Seguridad):
•En una empresa, un firewall protege la red corporativa de accesos no autorizados d esde Internet.
Adem ás, los datos que circulan dentro de la red pueden estar cifrados p ara proteger su
confidencialidad.

Ejercicio 1: Protección de Archivos en un Sistema
## Multiusuario
•Una empresa utiliza un sistema operativo multiusuario para gestionar los archivos de
sus empleados. Los archivos de cada usuario contienen información sensible y, para
garantizar la seguridad de la información, el sistema define permisos específicos para
cada archivo. El Usuario Atiene acceso completo (lectura, escritura y ejecución) a sus
propios archivos, pero no debería poder acceder a los archivos del Usuario Bsin
permiso. Sin embargo, el Usuario A nota que puede ver y editar un archivo de otro
empleado sin ninguna restricción.
•¿Qué mecanismo de protección podría estar mal configurado en este caso y qué
solución debería implementarse para asegurar que solo los usuarios autorizados
accedan a los archivos específicos de otros usuarios?

Ejercicio 2: Seguridad en una Red Empresarial
•En una empresa multinacional, se maneja información altamente sensible,
como detalles financieros y datos personales de clientes. Recientemente, la
empresa sufrió un intento de acceso no autorizado desde una dirección IP
desconocida. El departamento de IT ha detectado el intento de acceso gracias
al firewally a las políticas de seguridad de la red, que impidieron que los
datos fueran vulnerados. Sin embargo, la empresa quiere asegurarse de que
sus sistemas sean más seguros.
•¿Qué otras medidas de seguridad pueden implementarse en el sistema
operativo y la red para evitar accesos no autorizados, y cómo estas medidas
ayudan a garantizar la confidencialidad, integridad, y disponibilidadde los
datos?