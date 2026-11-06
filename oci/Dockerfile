# Dependencies for apps/mcp/oci in charys117/nas-gitops (hash-locked
# requirements.txt), plus a build-time index of OCI SDK clients and their
# operations (see build_index.py). The bridge script (server.py) stays in the
# cluster's ConfigMap.
FROM ghcr.io/astral-sh/uv:0.13.6-python3.13-trixie-slim@sha256:e586c1c65b7071aec78f02c5587c76c5011159cd76b3d6f1255f40e48e850abc

ENV UV_NO_CACHE=1 \
    UV_PYTHON_DOWNLOADS=0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt /tmp/requirements.txt
RUN uv venv /opt/venv \
 && uv pip install --python /opt/venv/bin/python --require-hashes -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt

COPY build_index.py /tmp/build_index.py
RUN cd /tmp \
 && /opt/venv/bin/python /tmp/build_index.py /opt/oci-index.sqlite \
 && rm -rf /tmp/build_index.py /tmp/*.log /root/.oci* \
 && chmod 0444 /opt/oci-index.sqlite

ENV OCI_MCP_INDEX=/opt/oci-index.sqlite
USER 10001:10001
