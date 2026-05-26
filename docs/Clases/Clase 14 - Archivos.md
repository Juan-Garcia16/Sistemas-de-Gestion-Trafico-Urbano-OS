

## ARCHIVOS
## Ing. Juan Andrés García Moreno

## CONCEPTO DE ARCHIVO
Un archivo es una unidad lógica de almacenamiento de
datos definida por el sistema operativo que permite
almacenar información en dispositivos no volátiles.

## TIPOS DE ARCHIVOS
Datos: Números, letras, archivos de texto, etc.
Programas: Código ejecutable y scripts.

## ATRIBUTOS DE ARCHIVOS
•Nombre: Identificador del archivo.
•Ubicación: Dirección del archivo en el dispositivo.
•Tamaño y tipo: Ayuda al sistema a conocer el formato.
•Permisos: Determinan los niveles de acceso (lectura, escritura,
ejecución).
•Fechas de acceso/modificación: Utilizadas para control y
seguridad

## EJEMPLO PRÁCTICO
Crear y visualizar diferentes atributos en un archivo de texto,
modificando permisos y observando los metadatos de los archivos
en el sistema (con comandos como ls-l en Linux o diren Windows).

## LINUX
Crear un archivo
echo "Este es un archivo de prueba" > archivo.txt
Visualizar permisos y otros atributos
ls-l archivo.txt
Cambiar permisos (usando chmod)
chmod644 archivo.txt  # Permisos de lectura y escritura para el propietario, solo lectura para los
demás
chmod755 archivo.txt  # Permisos de lectura, escritura y ejecución para el propietario,  solo lectura y
ejecución para los demás
Ver otros metadatos (como la fecha de creación, último acceso, etc.)
statarchivo.txt

## WINDOWS
## (CONSOLA DE COMANDOS -CMD)
Crear unarchivo:
echo Este es un archivo de prueba > archivo.txt
Visualizar atributos y metadatos:
dirarchivo.txt
Cambiar atributos(usando attrib)
attrib+r archivo.txt  # Cambia el archivo a solo lectura
attrib-r archivo.txt  # Quita el atributo de solo lectura
Ver permisos y más detalles (usando icacls)
icaclsarchivo.txt

## MÉTODOS DE ACCESO A
## ARCHIVOS
•Acceso Secuencial:
•El archivo se lee/escribe en orden de principio a fin.
•Ejemplo: Leer un archivo de texto línea por línea.
•Acceso Directo:
•Permite acceder directamente a un registro sin leer en secuencia.
•Ejemplo: Bases de datos que consultan bloques específicos de información.
•Acceso Indexado:
•Utiliza un índice que apunta a bloques de datos específicos.
•Ejemplo Práctico: Crear un índice para acceder a registros en un archivo que simule una
lista de precios.

## OPERACIONES BÁSICAS EN
## ARCHIVOS
•Creación: El sistema asigna espacio y añade una entrada en el directorio.
•Escritura y Lectura: Involucran punteros que indican la posición en el
archivo.
•Borrado y Truncado: Eliminación y reducción del contenido manteniendo la
entrada del archivo.
•Ejemplo Práctico: Uso de comandos como touch(creación), cato type
(lectura), rm(borrado) y truncate(truncado) en un sistema operativo basado
en Linux.

## MÉTODOS DE ACCESO A
## ARCHIVOS
•Acceso Secuencial:
•El archivo se lee/escribe en orden de principio a fin.
•Ejemplo: Leer un archivo de texto línea por línea.
•Acceso Directo:
•Permite acceder directamente a un registro sin leer en secuencia.
•Ejemplo: Bases de datos que consultan bloques específicos de información.
•Acceso Indexado:
•Utiliza un índice que apunta a bloques de datos específicos.
•Ejemplo Práctico: Crear un índice para acceder a registros en un archivo que simule una
lista de precios.

## ESTRUCTURA DE DIRECTORIOS
Los sistemas de archivos modernos organizan y gestionan la
información a través de estructuras de directorios. Un directorio
actúa como un contenedor que agrupa y organiza archivos y
subdirectorios en un sistema de almacenamiento, permitiendo una
administración eficiente y un acceso rápido a los datos.

## FUNCIÓN DEL DIRECTORIO
La función principal del directorioes organizar y gestionar los archivos en
una estructura que permita un acceso ordenado, eficiente y seguro. Los
directorios ayudan a:
•Evitar conflictos de nombresal permitir que varios archivos con el mismo nombre
existan en diferentes ubicaciones.
•Controlar el accesomediante permisos, evitando que usuarios no autorizados
puedan acceder o modificar archivos.
•Facilitar la administraciónde archivos y su almacenamiento, permitiendo al
usuario organizar sus datos en categorías, temas o cualquier estructura lógica.

## TIPOS DE ESTRUCTURAS DE
## DIRECTORIOS
Existen varias configuraciones para estructurar directorios en un
sistema operativo, cada una con sus propias ventajas y limitaciones.
A continuación, se describen las estructuras más comunes:
1.Directorio de Único Nivel
2.Directorio de Dos Niveles
3.Estructura en Árbol (Jerárquica)
4.Grafo Acíclico Dirigido

## 1.DIRECTORIO DE ÚNICO NIVEL
## Descripción:
Todos los
archivos se
almacenan en un
único directorio
sin
subdirectorios.
Esta estructura
es la más simple
y fácil de
implementar.
## Ventajas:
•Fácil de administrar,
ya que solo existe un
nivel.
•Acceso rápido a
cualquier archivo, ya
que todos están en
la misma ubicación.
## Desventajas:
•Conflictos de
nombres, ya que no
se pueden tener
archivos con el
mismo nombre.
•Falta de
organización y
estructura
jerárquica, lo que
dificulta la gestión
de un gran volumen
de archivos.
## Ejemplo: Un
sistema antiguo
o muy básico en
el que todos los
archivos de todos
los usuarios
están en una
única carpeta,
sin ningún tipo
de clasificación.

## 2.DIRECTORIO DE DOS NIVELES
•Descripción: La estructura de dos niveles introduce un directorio principal y subdirectorios
para cada usuario. Cada usuario tiene su propio espacio donde puede crear y organizar sus
archivos sin interferir con otros usuarios.
•Ventajas:
oPermite que varios usuarios tengan archivos con el mismo nombre sin conflictos, ya
que están en directorios separados.
oFacilita la compartición de archivos entre usuarios mediante la asignación de permisos.
•Desventajas:
oFalta de flexibilidad en la organización interna de los archivos de cada usuario, ya que el
directorio de dos niveles no admite subdirectorios adicionales.
•Ejemplo: Sistemas multiusuario de los años 70 y 80, donde cada usuario tiene un espacio
independiente en el sistema (/home/usuario1, /home/usuario2).

## 3.ESTRUCTURA EN ÁRBOL
## (JERÁRQUICA)
•Es la estructura más común en los sistemas operativos actuales.  Organiza los archivos y directorios en forma de
árbol, permitiendo crear subdirectorios dentro de otros directorios. Esto permite una organización  jerárquica
donde los usuarios pueden categorizar archivos y carpetas.
•Ventajas:
oOrganiza los archivos de manera lógica, facilitando  la clasificación  y el acceso a grandes cantidades de
datos.
oPermite a los usuarios crear subdirectorios según sus necesidades, proporcionando gran flexibilidad.
oLos directorios raíz y subdirectorios facilitan  la asignación  de permisos, con control a nivel de cada
carpeta.
•Desventajas:
oPuede ser compleja de navegar en sistemas con muchos niveles y directorios anidados.
•Ejemplo: Los sistemas modernos como Windows,  Linux y macOS utilizan  una  estructura en árbol. En Linux,  la
raíz (/) contiene subdirectorios como /home, /etc, /usr, y cada  uno de ellos puede tener sus propios
subdirectorios.

## 4.GRAFO ACÍCLICO DIRIGIDO
Esta estructura permite que los archivos y directorios sean compartidos entre varios usuarios o procesos mediante enlaces
simbólicos (o "symlinks") y enlaces duros. Los enlaces crean referencias adicionales que permiten que un archivo o directorio
exista en varias ubicaciones.
▪Ventajas:
•Permite la compartición de archivos y directorios de forma eficiente y flexible, sin necesidad de duplicar el archivo o
directorio.
•Evita conflictos en el acceso a archivos compartidos, ya que un archivo puede estar en múltiples ubicaciones
lógicas.
▪Desventajas:
•Requiere control adicional para evitar ciclos (referencias circulares), lo que podría causar bucles infinitos. Los
sistemas operativos deben implementar verificaciones para evitar estos problemas.
▪Ejemplo: En Linux, los enlaces simbólicos (ln-s) permiten que un archivo de un directorio se enlace en otro directorio.
Esto es útil para accesos compartidos y configuraciones de sistema en /etc.

## EJEMPLO PRÁCTICO: CREAR Y MANIPULAR
## DIRECTORIOS EN WINDOWS
- Crear Directorios y Subdirectorios
Crea un directorio llamado proyectos en el directorio principal del usuario
(C:\Usuarios\TuUsuario\o simplemente C:\Users\YourUser\en inglés):
mkdir%USERPROFILE%\proyectos
Dentro de proyectos, crea dos subdirectorios llamados proyecto1 y proyecto2:
mkdir%USERPROFILE%\proyectos\proyecto1
mkdir%USERPROFILE%\proyectos\proyecto2

## EJEMPLO PRÁCTICO: CREAR Y MANIPULAR
## DIRECTORIOS EN WINDOWS
- Crear Archivos dentro de Subdirectorios
Crea un archivo de texto en proyecto1 usando el comando echo para agregar
contenido inicial:
echo Este es el archivo 1 de proyecto1 > %USERPROFILE%\proyectos\proyecto1\archivo1.txt
También puedes crear un archivo vacío usando el comando typenul:
typenul> %USERPROFILE%\proyectos\proyecto1\archivo_vacio.txt
Crear un archivo dentro de proyecto1 usando el comando touch.

## EJEMPLO PRÁCTICO: CREAR Y MANIPULAR
## DIRECTORIOS EN WINDOWS
- Visualizar la Estructura de Directorios
Para ver la estructura de directorios y los archivos dentro de proyectos,
puedes usar el comando tree:
tree %USERPROFILE%\proyectos
Si deseas ver solo los archivos y carpetas en un nivel específico, usa:
dir %USERPROFILE%\proyectos /s
Para ver la estructura de directorios y los archivos dentro de proyectos, puedes usar el comando tree:

## EJEMPLO PRÁCTICO: CREAR Y MANIPULAR
## DIRECTORIOS EN WINDOWS
- Acceder a Archivos Usando Rutas Relativas y Absolutas
Ruta Absoluta: accede a archivo1.txt desde cualquier ubicación en el sistema
utilizando su ruta completa.
type %USERPROFILE%\proyectos\proyecto1\archivo1.txt
Ruta Relativa: navega hasta el directorio proyecto1 y accede a archivo1.txt usando
solo el nombre del archivo:
cd %USERPROFILE%\proyectos\proyecto1
type archivo1.txt
Para ver la estructura de directorios y los archivos dentro de proyectos, puedes usar el comando tree:

## EJEMPLO PRÁCTICO: CREAR Y MANIPULAR
## DIRECTORIOS EN WINDOWS
- Crear Accesos Directos (Simulación de Grafo Acíclico)
En Windows, los accesos directos funcionan de manera similar a los enlaces
simbólicos en Linux, permitiendo apuntar a archivos o carpetas desde distintas
ubicaciones.
Crear un acceso directo a archivo1.txt en el directorio proyecto2:
mklink %USERPROFILE%\proyectos\proyecto2\enlace_a_archivo1.txt %USERPROFILE%\proyectos\proyecto1\archivo1.txt
▪Nota: Este comando solo funciona en el Símbolo del sistema y requiere permisos de administrador.
Ahora se puede acceder a enlace_a_archivo1.txt desde proyecto2, el cual apunta al
archivo original en proyecto1.
Para ver la estructura de directorios y los archivos dentro de proyectos, puedes usar el comando tree:

## EJEMPLO PRÁCTICO: CREAR Y MANIPULAR
## DIRECTORIOS EN WINDOWS
- Borrar Archivos y Directorios
Para eliminar el archivo archivo1.txt en proyecto1, utiliza:
del %USERPROFILE%\proyectos\proyecto1\archivo1.txt
Para eliminar un directorio completo (incluidos los archivos
que contiene), utiliza:
rmdir %USERPROFILE%\proyectos\proyecto2 /s /q
Para ver la estructura de directorios y los archivos dentro de proyectos, puedes usar el comando tree:

## COMANDOS EN WINDOWS

## MONTAJE Y COMPARTICIÓN DE
## ARCHIVOS
El montaje y compartición de archivos son dos conceptos
fundamentales en la gestión de sistemas de archivos en un sistema
operativo. Ambos conceptos permiten organizar y hacer accesibles
los archivos y sistemas de archivos a los usuarios y aplicaciones de
manera eficiente y controlada.

## 1.MONTAJE DE SISTEMAS DE
## ARCHIVOS
El montaje es el proceso de asociar un sistema de archivos (ubicado en un
dispositivo de almacenamiento, como un disco duro, SSD o unidad USB)
con un directorio en el sistema operativo, llamado punto de montaje.
Una vez montado, el sistema de archivos se hace accesible al usuario y a
las aplicaciones como una extensión del sistema de archivos principal.

## PROCESO DE MONTAJE
•Punto de Montaje: Es un directorio donde el sistema de archivos se
"adjunta" para que el usuario pueda acceder a él. Por ejemplo, en
sistemas Unix/Linux, se usa el directorio /mnt o /media.
•Verificación de Acceso: Durante el montaje, el sistema operativo
verifica permisos y control de acceso para asegurar que el dispositivo
puede integrarse sin problemas de seguridad.
•Estructura del Sistema de Archivos: Una vez montado, el sistema de
archivos sigue la estructura del sistema operativo, permitiendo
acceder a archivos y directorios con rutas estandarizadas.

## EJEMPLOS DE MONTAJE EN
## SISTEMAS OPERATIVOS
Linux/Unix:
•El comando mount permite montar sistemas de archivos en puntos de montaje
específicos.
•Ejemplo: Para montar un sistema de archivos en /mnt/disco, se puede usar:
sudomount /dev/sdb1 /mnt/disco
•Para desmontar, se utiliza umount
sudo umount /mnt/disco
Los sistemas de archivos también pueden montarse automáticamente al inicio agregando una
entrada en el archivo /etc/fstab.

## EJEMPLOS DE MONTAJE EN
## SISTEMAS OPERATIVOS
## Windows:
•En Windows, los discos se montan automáticamente en letras de unidad, como C:, D:, E:
•También es posible asignar un directorio de montaje a una unidad de almacenamiento usando
la herramienta "Disk Management" o el comando mountvol.
•Ejemplo: Para montar una unidad en una carpeta específica, se podría utilizar:
mountvolC:\punto_montaje \\?\Volume{GUID}

## VENTAJAS DEL MONTAJE DE
## SISTEMAS DE ARCHIVOS
•Flexibilidad: Permite acceder a múltiples sistemas de archivos y
dispositivos de almacenamiento desde una única jerarquía de
archivos.
•Integración y Expansión: Facilita la expansión del almacenamiento
sin afectar la estructura de directorios principal.
•Seguridad: El sistema operativo controla los permisos de montaje,
previniendo el acceso no autorizado a dispositivos de almacenamiento
externos.

## COMPARTICIÓN DE ARCHIVOS
La compartición de archivos es el proceso mediante el cual los
archivos y directorios se ponen a disposición de múltiples usuarios
o dispositivos en una red. Esto es esencial en sistemas
multiusuario y entornos de red, donde se requiere acceso
colaborativo a los recursos.

## TIPOS DE COMPARTICIÓN DE
## ARCHIVOS
1.Local (Dentro de un Sistema):
1.En sistemas multiusuario, los archivos pueden compartirse entre usuarios en el mismo sistema
utilizando permisos de archivo y listas de control de acceso (ACL).
2.Los permisos definen qué usuarios pueden leer, escribir o ejecutar los archivos.
2.Remota (A través de una Red):
1.En entornos de red, la compartición de archivos permite acceder a archivos en diferentes
dispositivos mediante protocolos de red.
2.Los métodos comunes de compartición de archivos en red incluyen:
1.NFS (Network File System): Un protocolo usado en sistemas Unix/Linux que permite compartir directorios a través
de una red.
2.SMB (Server Message Block): Protocolo de compartición de archivos en redes Windows, que permite compartir
archivos, impresoras y otros recursos.
3.FTP (File Transfer Protocol) y SFTP: Protocolos que permiten la transferencia de archivos entre sistemas.

## COMPARTICIÓN DE ARCHIVOS EN
## LINUX CON NFS
•En Linux, se puede configurar un servidor NFS para compartir directorios
con otros sistemas en la red.
•Ejemplo: Compartir el directorio /home/usuario/compartido en una red.
•En el servidor:
sudo exportfs -o rw /home/usuario/compartido
•En el cliente, se monta el recurso compartido:
sudo mount servidor:/home/usuario/compartido  /mnt/remoto


## COMPARTICIÓN DE ARCHIVOS EN
## WINDOWS CON SMB
•En Windows, la compartición de archivos se realiza mediante SMB. Los usuarios pueden
crear carpetas compartidas y asignar permisos específicos.
•Ejemplo: Compartir una carpeta llamada Documentos en una red.
oClic derecho en la carpeta > Propiedades > Compartir.
oAsignar permisos para usuarios específicos de la red.
oLos usuarios de la red pueden acceder a la carpeta compartida mediante \\nombre_equipo\Documentos.

## USANDO FTP PARA
## COMPARTICIÓN DE ARCHIVOS
•FTP permite compartir archivos entre sistemas mediante una conexión remota.
•Ejemplo: En un servidor Linux, instalar y configurar vsftpd como servidor FTP:
sudo apt install vsftpd
sudo systemctl start vsftpd
•Los clientes pueden conectarse usando un cliente FTP (como FileZilla) o mediante el
comando ftp en la terminal.


## VENTAJAS DE LA COMPARTICIÓN
## DE ARCHIVOS
•Colaboración: Facilita el trabajo en equipo, permitiendo a varios
usuarios acceder y modificar los mismos archivos.
•Optimización de Recursos: Reduce la necesidad de duplicar
archivos en varios dispositivos, ya que los usuarios pueden acceder a
los mismos archivos en un servidor central.
•Escalabilidad: Es especialmente útil en entornos empresariales y
educativos, donde se requiere el acceso controlado a grandes
volúmenes de datos por múltiples usuarios.

## CONSIDERACIONES DE SEGURIDAD EN LA
## COMPARTICIÓN DE ARCHIVOS
•Control de Acceso: Implementar permisos de lectura, escritura y ejecución
para garantizar que solo usuarios autorizados puedan acceder a los
archivos.
•Cifrado de Transferencia: Al compartir archivos en red, es recomendable
utilizar métodos seguros como SFTP o FTPS para proteger los datos en
tránsito.
•Auditoría y Monitoreo: Supervisar el acceso y las modificaciones en
archivos compartidos para detectar cualquier actividad no autorizada o
malintencionada.

## EJEMPLOS PRÁCTICOS DE MONTAJE Y
## COMPARTICIÓN EN WINDOWS Y LINUX
1.Ejemplo en Linux:
•Montar un dispositivo USB en el directorio /mnt/usb:
sudomount /dev/sdb1 /mnt/usb
•Compartir el directorio /mnt/usb en la red mediante NFS:
sudoexportfs-o rw/mnt/usb

## EJEMPLOS PRÁCTICOS DE MONTAJE Y
## COMPARTICIÓN EN WINDOWS Y LINUX
1.Ejemplo en Windows:
•Crear una carpeta llamada Proyectos en C:\Users\Usuario\Proyectos.
•Compartir la carpeta en la red:Clic derecho en la carpeta Proyectos, seleccionar Propiedades > Compartir.
•Agregar usuarios con permisos específicos y aplicar la configuración.
•Acceder a la carpeta desde otro equipo en la red mediante la ruta \\NombreEquipo\Proyectos.

## ACCESO REMOTO CON FTP
•Configurar un servidor FTP en Linux con vsftpd para
compartir archivos de manera remota.
•En el cliente, acceder al servidor FTP usando:
ftp servidor

## PROTECCIÓN DE ARCHIVOS
La protección de archivos es una función esencial de los sistemas
operativos que asegura que los datos almacenados estén accesibles
únicamente por usuarios o procesos autorizados, evitando el acceso
no deseado o malintencionado. A través de la protección de
archivos, los sistemas operativos garantizan la integridad,
confidencialidad y disponibilidad de los datos.

## ¿POR QUÉ ES IMPORTANTE
## PROTEGER LOS ARCHIVOS?
1.Prevención de Acceso No Autorizado:
▪Impide que usuarios sin permisos accedan, modifiquen o eliminen archivos críticos del sistema o
archivos privados de otros usuarios.
2.Asegurar la Integridad de los Datos:
▪Protege los archivos contra modificaciones accidentales o intencionadas.
3.Garantizar la Confidencialidad:
▪Permite que los archivos privados sean accesibles solo por los propietarios o usuarios autorizados.
4.Control de Recursos Compartidos:
▪En entornos multiusuario o de red, evita que los archivos compartidos sean manipulados de forma
inadecuada.

## MÉTODOS DE PROTECCIÓN DE
## ARCHIVOS
Los sistemas operativos utilizan diversos métodos para proteger
archivos. A continuación, se describen los más comunes:
a.Permisos de Archivos
b.Propietarios y Grupos
c.Listas de Control de Acceso (ACLs)
d.Contraseñas de Archivos
e.Encriptación

## MECANISMOS DE PROTECCIÓN
## EN SISTEMAS OPERATIVOS
•Sistemas Linux/Unix
a.Linux/Unix utiliza permisos básicos representados en tres niveles:
propietario, grupo y otros.
b.Ejemplo: Un archivo puede tener permisos -rw-r--r-- que indican:
•Propietario (rw): Puede leer y escribir.
•Grupo (r): Solo puede leer.
•Otros (r): Solo pueden leer.

## COMANDOS BÁSICOS
## PARA GESTIONAR
## PERMISOS

## PROTECCIÓN EN SISTEMAS
## WINDOWS
•En Windows, los permisos se gestionan desde las Propiedades del archivo, en la pestaña Seguridad.
•Tipos de permisos:
oControl total:  Permite  todas las acciones  (lectura,  escritura,  eliminación).
oModificar:  Permite  editar contenido, pero no eliminar el archivo.
oLectura/Ejecución:  Solo permite  abrir o ejecutar  el archivo.
## ▪
•Ejemplo: Configurar permisos avanzados para un archivo:
•Clic derecho en el archivo > Propiedades > Seguridad > Editar permisos.

## DESAFÍOS Y SOLUCIONES EN LA
## PROTECCIÓN DE ARCHIVOS
•Colaboración en Red:
•Problema: Un usuario intenta acceder a un archivo sin permisos.
•Solución: Configurar permisos detallados usando ACLs o cifrar el archivo.
•Colaboración en Red:
•Problema: Varios usuarios necesitan trabajar con el mismo archivo.
•Solución: Usar protocolos seguros como SMB (Windows) o NFS (Linux) con permisos controlados.
•Colaboración en Red:
•Problema: Un archivo se elimina accidentalmente.
•Solución: Configurar políticas de respaldo y recuperación, como herramientas de recuperación en Windows o rsync en
## Linux.