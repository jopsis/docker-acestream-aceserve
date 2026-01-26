# Docker AceServe

Contenedor Docker para AceStream Engine compatible con múltiples arquitecturas (ARM32, ARM64, x86_64).

## Descripción

Este proyecto proporciona imágenes Docker del motor AceStream que funcionan de manera similar al servicio AceStream original, permitiendo la reproducción de streams P2P mediante el protocolo Ace.

**Las imágenes están disponibles en Docker Hub tanto como [`jopsis/aceserve`](https://hub.docker.com/r/jopsis/aceserve) como [`jopsis/acestream`](https://hub.docker.com/r/jopsis/acestream), con los mismos tags y para todas las arquitecturas.**
## Arquitecturas soportadas

- `linux/arm/v7` (ARM32)
- `linux/arm64` (ARM64/ARMv8)
- `linux/amd64` (x86_64)

## Uso

### Docker Run

```bash
docker run -d \
  --name aceserve \
  -p 6878:6878 \
  -p 8621:8621 \
  -p 62062:62062 \
  jopsis/aceserve:latest
```

### Docker Compose

Crea un archivo `docker-compose.yml`:

```yaml
services:
  aceserve:
    image: jopsis/aceserve:latest
    container_name: aceserve
    ports:
      - "6878:6878"
      - "8621:8621"
      - "62062:62062"
    restart: unless-stopped
```

Ejecuta el contenedor:

```bash
docker-compose up -d
```

## Puertos

- **6878**: Puerto HTTP API de AceStream (por defecto)
- **8621**: Puerto del nodo P2P, usado para comunicarse con otros peers
- **62062**: Puerto TCP para la API antigua del motor (deprecated, incluido por compatibilidad) 

## Acceso

Una vez iniciado el contenedor, puedes acceder a la interfaz web en:

```
http://localhost:6878
```

## Ejemplo de uso

Para reproducir un stream de AceStream:

```
http://localhost:6878/ace/getstream?id=CONTENTHASH
```

Donde `CONTENTHASH` es el ID del contenido AceStream que deseas reproducir.

## Uso de servidores DNS personalizados

Puedes especificar servidores DNS personalizados para el contenedor AceServe usando la clave `dns:` en tu `docker-compose.yml`. De este modo, todas las resoluciones DNS internas realizadas por el demonio utilizarán dichos DNS (y no el resolver interno de Docker).

**Ejemplo de docker-compose.yml usando DNS personalizados:**
```yaml
services:
  aceserve:
    image: jopsis/aceserve:latest
    container_name: aceserve
    ports:
      - "6878:6878"
      - "8621:8621"
      - "62062:62062"
    restart: unless-stopped
    dns:
      - 1.1.1.1
      - 1.0.0.1
```

Cuando defines la clave `dns:`, el contenedor usará esas IPs para todas las consultas DNS internas mediante el proxy. Los servidores usados realmente se detectan en tiempo de ejecución y quedan reflejados en el log del contenedor.

**Ejemplo de línea en el log:**
```
2026-01-26 14:45:37|MainThread|bootstrap|Override DNS usando ExtServers del comentario: ['1.1.1.1', '1.0.0.1']
```

Si no se especifica la opción `dns:`, se usarán los nameservers por defecto configurados por Docker.

**Para comprobar qué servidores DNS está usando el contenedor:**
```sh
docker logs aceserve | grep "Override DNS"
```
o consulta el archivo `/dev/shm/acestream.log` dentro del contenedor.

Esto asegura que todo el tráfico DNS del motor AceServe sea resolvido por los DNS que elijas y que puedes verificar en tiempo real.

## Tags disponibles

Para [`jopsis/aceserve`](https://hub.docker.com/r/jopsis/aceserve) y [`jopsis/acestream`](https://hub.docker.com/r/jopsis/acestream):

- `latest`: Última versión estable
- `vX.X.X`: Versiones específicas (ej: `v3.1.2`)

## Construcción

El proyecto incluye Dockerfiles para cada arquitectura en sus respectivas carpetas:

- `aceserve-arm32/`: Para dispositivos ARM32
- `aceserve-arm64/`: Para dispositivos ARM64
- `aceserve-x86_64/`: Para sistemas x86_64

## Errores conocidos

- `ARM v8 architecture (like Raspberry Pi 5)`:  [`Not suitable for 'modern' 16k page-size kernels OS`](https://github.com/jopsis/docker-acestream-aceserve/issues/1)

## Licencia

Este proyecto se proporciona tal cual, sin garantías.


