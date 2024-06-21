# Workshop sobre DOCKER & GIT

El objetivo de este workshop es dar una demostración sobre los conceptos de git y docker impartidos en el curso **Fundamentos de Data Engineering** del **Diploma en Data Engineering** de [Instituto CPE](https://institutocpe.edu.uy/oferta-de-cursos/diploma-en-data-engineering/).

No se darán contenidos teóricos ya que los mismos se detallan en el curso, el objetivo de este repo es detallar los pasos de la demo para poder reproducirlos o usarlo como *cheatsheet*.

## Git & Github

### Inicialización del proyecto

Para iniciar un repositorio git, es necesario trasladarse mediante la consola hasta el directorio donde tendremos nuestro proyecto, y ejecutar el siguiente comando.

```bash
git init
```

Este comando creará un repositorio en el directorio, y se podrá empezar a generar versiones del mismo. 

El primer paso es generar un archivo `README.md` que permite a quien visita el repo entender cuál es el objetivo del mismo y cómo utilizarlo, como ocurre en este caso. 

Para agregar el nuevo archivo a instancia git:

```bash
git add README.md
```

Esto pasa al archivo seleccionado a una instancia de `staging` en donde cuando se entienda que la versión nueva está lista, se puede realizar un `commit`. Un `commit` no es más que una nueva versión del repositorio para la `branch` en que estamos trabajando.

```bash
git commit -m 'Agregando el archivo README'
```

Ahora se tiene una nueva versión de la `branch` principal, o `main`. Pero se está trabajando únicamente a nivel local. Para poder llevar esto a la nube, se debe vincular con un repositorio remoto en [Github](https://github.com/), y enviar mediante el comando `push`.  

```bash
git remote add origin <git_repo_url>
```

Luego de esto, se puede enviar nuestro repositorio a la nube.

```bash
git push --set-upstream origin master
```

### Branching y Merging

Para crear una rama, o `branch`, se debe asignarle un nombre.

```bash
git branch my-branch
```

Crearla no significa ya estar en la rama, hay que moverse hacia la misma.

```bash
git checkout my-branch
```

Podemos chequear en qué rama estamos, junto con todo lo importante que ocurra en la misma, utilizando el comando `status`.

```bash
git status
```

Luego de realizar los cambios convenientes en esa `branch`, realizar los `commits` correspondientes, y realizar un `push` hacia la rama remota, se debe generar un `pull request` para unir los cambios de la rama nueva con la principal.

Un `pull request` (PR) se puede realizar mediante la herramienta GIT que se esté utilizando para el trabajo colaborativo. En este caso, Github.

Una vez que el PR es realizado, es esperable que un colega haga una revisión del código a integrar a la rama principal. Lo que se denomina `code review`. Esta es una buena práctica ya que agrega una capa de seguridad adicional a este proceso. 

Una vez aprobado el PR, ya sea con revisiones o no, se genera un `merge` con la rama `main`, y de este modo queda integrada la rama de desarrollo al producto final.

## Docker

Para utilizar Docker es conveniente tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/).

Para obtener una imagen docker, se puede utilizar el comando `pull`.

```bash
docker pull ubuntu
```

Si se observa la instancia de Docker Desktop, se puede observar como una `imagen` de ubuntu se ha obtenido. Para activar dicha imagen y empezar a interactuar con ella, es necesario crear un `container` que la integre.

```bash
docker run -it --name my_first_container ubuntu
```

Al dejar de interactuar con la instancia docker, se deja de ejecutar el contenedor, por tanto, si queremos volver a activarlo, se debe usar el comando `start` y `sh` al final.

```bash
docker start -it my_first_container sh
```

Usando el comando `stop` se puede detener al contenedor. También es posible ver en cualquier momento el estado de los contenedores mediante el comando `ps`.

```bash
docker ps
```

También es posible ejecutar comandos con mayor complejidad, que permitan incorporar otros elementos al contenedor. En el siguiente ejemplo:

- Se genera un nombre para el contenedor (`--name`)
- Se agrega la variable de entorno POSTGRES_PASSWORD, que permite ser accedida dentro de la instancia (`-e`)
- Se habilita un puerto para que la instancia pueda ser accesible desde el exterior (`-p`). Esto hace posible, por ejemplo, acceder mediante un cliente de base de datos. 
- No se descargó previamente la imagen `postgres`, pero docker lo hace automático por nosotros (`-d`)

```bash
docker run \
    --name my-postgres \
    -e POSTGRES_PASSWORD=mysecretpassword \
    -p 5432:5432 \
    -d postgres
```

En algunos casos es necesario crear instancias de Docker que hagan cosas predeterminadas, como ejecutar determinados procesos. Para eso es necesario crear un `Dockerfile`, como el que aparece en este repositorio.

```
FROM python:3.9

RUN apt-get update && \
    apt-get install -y --no-install-recommends 

WORKDIR /app

COPY requirements.txt *.py ./

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "my-script.py"]
```

La estructura del `Dockerfile` es la siguiente:
- **FROM** hace referencia a la imagen base.
- **RUN** es un comando que genera que se corra en consola lo que venga a continuación.
- **WORKDIR** es el nombre del directorio dentro de la instancia de Docker en donde se almacenarán los archivos.
- **COPY** indica qué archivos del presente directorio llevar adentro de la instancia.
- **ENTRYPOINT** es el comando a ejecutar inmediatamente cada vez que la imagen es demandada por un contenedor.

Para construir esta imagen customizada a partir de este `Dockerfile`, se puede correr el siguiente comando. Una vez hecho esto, debería aparecer en el listado de imagenes en `Docker Desktop`.

```bash
docker build -t my_image .
```

Se puede utilizar esta imagen como cualquier otra. En este caso se uso específico de esta imagen es ejecutar un script de Python.

```python
import pandas as pd 
import os 
import datetime as dt

data_path = os.getenv('DATA_PATH')
data_name = os.getenv('DATA_NAME')

print(f'Data path: {data_path} \n Data name: {data_name}')

try:
    df = pd.read_csv(data_path)

    print(f'Dataset succesfully read: {len(df)} rows')

    df.columns = [col.lower() for col in df.columns]

    df.columns = [col.replace(' ', '_') for col in df.columns]

    df.to_csv(f'data/{data_name}_{dt.date.today()}.csv')

    print('Dataset stored as csv succesfully')

except Exception as e:
    print(f'Something went wrong: {e}')
```

Este script obtiene dos variables de entorno y luego las utiliza para descargar un csv de una determinada ruta **DATA_PATH** y le asigna un determinado nombre **DATA_NAME** junto con la fecha de la extracción. Además, le aplica una limpieza a las columnas, pasando sus nombres a minúsculas y reemplazando los espacios por `_`.

Para ejecutar este script dentro de un contenedor se puede utilizar un comando como el siguiente.

```bash
docker run \
  --name my-python-container \
  -e DATA_PATH=my_csv_path \
  -e DATA_NAME=my_dataset_name \
  -v /my_local_path/data:/app/data \
  my_python_image 
```

Se puede apreciar que además del nombre del contenedor y las variables de entorno necesarias para ejecutar el script, aparece otro elemento: el `volume`. Los volúmenes son carpetas sincronizadas entre la instancia local y el contenedor, de modo de poder acceder a lo que ocurre en ellos. Es necesario en este caso ya que queremos acceder al dataset generado como resultado de este proceso. 