# Docker AceServe

Docker container for AceStream Engine with support for multiple architectures (ARM32, ARM64, x86_64).

## Description

This project provides Docker images for the AceStream engine that work similarly to the original AceStream service, allowing P2P stream playback using the Ace protocol.

**Images are available on Docker Hub both as [`jopsis/aceserve`](https://hub.docker.com/r/jopsis/aceserve) and [`jopsis/acestream`](https://hub.docker.com/r/jopsis/acestream), with identical tags for all architectures.**
## Supported Architectures

- `linux/arm/v7` (ARM32)
- `linux/arm64` (ARM64/ARMv8)
- `linux/amd64` (x86_64)

## Usage

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

Create a `docker-compose.yml` file:

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

Run the container:

```bash
docker-compose up -d
```

## Ports

- **6878**: AceStream HTTP API port (default)
- **8621**: P2P node port, used to communicate with other peers
- **62062**: TCP port for old engine API (deprecated, included for compatibility)

## Access

Once the container is running, you can access the web interface at:

```
http://localhost:6878
```

## Usage Example

To play an AceStream stream:

```
http://localhost:6878/ace/getstream?id=CONTENTHASH
```

Where `CONTENTHASH` is the ID of the AceStream content you want to play.

## Using Custom DNS Servers

You can specify custom DNS servers for the AceServe container via the `dns:` key in your `docker-compose.yml`. This will ensure that all internal DNS resolution performed by the daemon uses your specified servers (not Docker's internal resolver).

**Example docker-compose.yml with custom DNS:**
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

When you set the `dns:` option, the container will use those IP addresses for all DNS lookups made by the internal resolver. The actual servers in use are detected and logged by the application at runtime.

**Log example:**
```
2026-01-26 14:45:37|MainThread|bootstrap|Override DNS using ExtServers from comment: ['1.1.1.1', '1.0.0.1']
```

If `dns:` is not specified, it will fallback to the default nameserver(s) configured by Docker.

**To check which DNS servers are currently used by the container:**
```sh
docker logs aceserve | grep "Override DNS"
```
or look inside the container file `/dev/shm/acestream.log`.

This helps ensure all DNS resolution by the AceServe engine is under your control and you can verify it at runtime.


## Available Tags

For both [`jopsis/aceserve`](https://hub.docker.com/r/jopsis/aceserve) and [`jopsis/acestream`](https://hub.docker.com/r/jopsis/acestream):

- `latest`: Latest stable version
- `vX.X.X`: Specific versions (e.g., `v3.1.2`)

## Build

The project includes Dockerfiles for each architecture in their respective folders:

- `aceserve-arm32/`: For ARM32 devices
- `aceserve-arm64/`: For ARM64 devices
- `aceserve-x86_64/`: For x86_64 systems

## Known Issues

- `ARM v8 architecture (like Raspberry Pi 5)`:  [`Not suitable for 'modern' 16k page-size kernels OS`](https://github.com/jopsis/docker-acestream-aceserve/issues/1)

## License

This project is provided as-is, without warranties.

