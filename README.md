# nas-mcp

Images for the self-written MCP bridges that run in the home cluster
(`apps/mcp/<bridge>` in charys117/nas-gitops). Each image only carries the
bridge's Python dependencies in `/opt/venv`; the bridge script itself
(`server.py`) stays in the cluster as a ConfigMap, so changing it needs no
rebuild.

| Bridge | Image | Contents |
| --- | --- | --- |
| monarch | `ghcr.io/cyrahs/nas-mcp:monarch` | robcerda/monarch-mcp-server at the commit in `MONARCH_MCP_REF`, from its hash-locked requirements |
| netcup | `ghcr.io/cyrahs/nas-mcp:netcup` | `netcup/requirements.txt` |
| oci | `ghcr.io/cyrahs/nas-mcp:oci` | `oci/requirements.txt`, plus `/opt/oci-index.sqlite` (see below) |

Images are built for linux/amd64 on every push to `main` that touches the
bridge's directory, tagged `<bridge>` and `<bridge>-<commit sha>`. Pull
requests build without pushing. Flux in nas-gitops follows the `<bridge>` tag
by digest and rolls the pod.

## Updating dependencies

- monarch: bump `MONARCH_MCP_REF` in `monarch/Dockerfile`.
- netcup / oci: edit `requirements.in`, then regenerate the lock file:

  ```sh
  uv pip compile --generate-hashes --universal --python-version 3.12 requirements.in -o requirements.txt --no-header  # netcup
  uv pip compile --generate-hashes --universal --python-version 3.13 requirements.in -o requirements.txt --no-header  # oci
  ```

## oci client index

Oracle's `oci-cloud-mcp-server` answers `find_oci_api` (without `client_fqn`)
and `list_oci_clients` by importing every module of the OCI SDK, about 17,500
of them, which leaves the process at roughly 530 MiB. `oci/build_index.py`
runs that discovery once while the image is built and writes each client's
operations, one-line summaries and signatures to `/opt/oci-index.sqlite`
(`OCI_MCP_INDEX`). The bridge in nas-gitops serves those two tools from the
index and gives the same answers.
