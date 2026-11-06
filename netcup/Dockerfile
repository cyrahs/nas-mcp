# Dependencies for apps/mcp/netcup in charys117/nas-gitops (hash-locked
# requirements.txt). The bridge script (server.py) stays in the cluster's ConfigMap.
FROM ghcr.io/astral-sh/uv:0.13.6-python3.12-trixie-slim@sha256:bf889bda77474aa50c351caf1538b855ef2b7a30add45f26ca50dcb6ade06402

ENV UV_NO_CACHE=1 \
    UV_PYTHON_DOWNLOADS=0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt /tmp/requirements.txt
RUN uv venv /opt/venv \
 && uv pip install --python /opt/venv/bin/python --require-hashes -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt \
 && /opt/venv/bin/python -c "import mcp.server.fastmcp, httpx, uvicorn"

USER 10001:10001
