# Dependencies for apps/mcp/monarch in charys117/nas-gitops: the upstream
# robcerda/monarch-mcp-server at a pinned commit, from its hash-locked
# requirements. The bridge script (server.py) stays in the cluster's ConfigMap.
FROM ghcr.io/astral-sh/uv:0.13.6-python3.12-trixie-slim@sha256:bf889bda77474aa50c351caf1538b855ef2b7a30add45f26ca50dcb6ade06402

ARG MONARCH_MCP_REF=5cc005783086ef232cdb967a5259b4cfa78d05f4
ENV UV_NO_CACHE=1 \
    UV_PYTHON_DOWNLOADS=0 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN uv venv /opt/venv \
 && uv pip install --python /opt/venv/bin/python --require-hashes \
      -r "https://raw.githubusercontent.com/robcerda/monarch-mcp-server/${MONARCH_MCP_REF}/requirements-lock.txt" \
 && uv pip install --python /opt/venv/bin/python --no-deps \
      "monarch-mcp-server @ https://github.com/robcerda/monarch-mcp-server/archive/${MONARCH_MCP_REF}.tar.gz" \
 && /opt/venv/bin/python -c "import monarch_mcp_server.app, monarchmoney"

USER 10001:10001
