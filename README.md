# Workshop sobre DOCKER & GIT

El objetivo de este workshop es dar una demostración sobre los conceptos de git y docker impartidos en el curso **Fundamentos de Data Engineering** del **Diploma en Data Engineering** de [Instituto CPE](https://institutocpe.edu.uy/oferta-de-cursos/diploma-en-data-engineering/).

No se darán contenidos teóricos ya que los mismos se detallan en el curso, el objetivo de este repo es detallar los pasos de la demo para poder reproducirlos o usarlo como *cheatsheet*.

## Git & Github

### Inicialización del proyecto

Para iniciar un repositorio git, es necesario trasladarse mediante la consola hasta el directorio donde tendremos nuestro proyecto, y ejecutar el siguiente comando.

```
git init
```

Este comando creará un repositorio en el directorio, y se podrá empezar a generar versiones del mismo. 

El primer paso es generar un archivo `README.md` que permite a quien visita el repo entender cuál es el objetivo del mismo y cómo utilizarlo, como ocurre en este caso. 

Para agregar el nuevo archivo a instancia git:

```
git add README.md
```

Esto pasa al archivo seleccionado a una instancia de `staging` en donde cuando se entienda que la versión nueva está lista, se puede realizar un `commit`. Un `commit` no es más que una nueva versión del repositorio para la `branch` en que estamos trabajando.

```
git commit -m 'Agregando el archivo README'
```

Ahora se tiene una nueva versión de la `branch` principal, o `main`. Pero se está trabajando únicamente a nivel local. Para poder llevar esto a la nube, se debe vincular con un repositorio remoto en [Github](https://github.com/), y enviar mediante el comando `push`.  

```
git remote add origin <git_repo_url>
```

Luego de esto, se puede enviar nuestro repositorio a la nube.

```
git push --set-upstream origin master
```

### Branching y Merging

Para crear una rama, o `branch`, se debe asignarle un nombre.

```
git branch my-branch
```

Crearla no significa ya estar en la rama, hay que moverse hacia la misma.

```
git checkout my-branch
```

Podemos chequear en qué rama estamos, junto con todo lo importante que ocurra en la misma, utilizando el comando `status`.

```
git status
```

Luego de realizar los cambios convenientes en esa `branch`, realizar los `commits` correspondientes, y realizar un `push` hacia la rama remota, se debe generar un `pull request` para unir los cambios de la rama nueva con la principal.

Un `pull request` (PR) se puede realizar mediante la herramienta GIT que se esté utilizando para el trabajo colaborativo. En este caso, Github.

Una vez que el PR es realizado, es esperable que un colega haga una revisión del código a integrar a la rama principal. Lo que se denomina `code review`. Esta es una buena práctica ya que agrega una capa de seguridad adicional a este proceso. 

Una vez aprobado el PR, ya sea con revisiones o no, se genera un `merge` con la rama `main`, y de este modo queda integrada la rama de desarrollo al producto final.

## Docker

Para utilizar Docker es conveniente tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/).

Para obtener una imagen docker, se puede utilizar el comando `pull`.

```
docker pull ubuntu
```

Si se observa la instancia de Docker Desktop, se puede observar como una `imagen` de ubuntu se ha obtenido. Para activar dicha imagen y empezar a interactuar con ella, es necesario crear un `container` que la integre.

```
docker run -it --name my_first_container ubuntu
```

Al dejar de interactuar con la instancia docker, se deja de ejecutar el contenedor, por tanto, si queremos volver a activarlo, se debe usar el comando `start` y `sh` al final.

```
docker start -it my_first_container sh
```

Usando el comando `stop` se puede detener al contenedor. También es posible ver en cualquier momento el estado de los contenedores mediante el comando `ps`.

```
docker ps
```

También es posible ejecutar comandos con mayor complejidad, que permitan incorporar otros elementos al contenedor. En el siguiente ejemplo:

- Se genera un nombre para el contenedor (`--name`)
- Se agrega la variable de entorno POSTGRES_PASSWORD, que permite ser accedida dentro de la instancia (`-e`)
- Se habilita un puerto para que la instancia pueda ser accesible desde el exterior (`-p`). Esto hace posible, por ejemplo, acceder mediante un cliente de base de datos. 
- No se descargó previamente la imagen `postgres`, pero docker lo hace automático por nosotros (`-d`)

```
docker run \
    --name my-postgres \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -p 5432:5432 \
    -d postgres
```


