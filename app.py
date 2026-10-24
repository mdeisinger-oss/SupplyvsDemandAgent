"""Web Application & REST API Server for MD-Supply-vs-Demand-Agent.

Provides:
1. Interactive Chat Input Window (`/api/chat`) for manual user demand entry and
   conversational acceptance of alternative recommendations.
2. Demand File Upload Endpoint (`/api/upload-demand`) supporting `.csv`, `.json`,
   and `.jsonl` batch demand schedules.
3. Human-in-the-Loop (HITL) Customer Acceptance Endpoint (`/api/hitl/accept` and
   `/api/hitl/reject`) to accept recommended alternatives and continue FCFS matching.
4. Live Static Supply vs. Demand Inventory, FCFS Allocation Ledger, OpenTelemetry
   Trace Spans, and Intent-vs-Outcome Audit Endpoints (`/api/state`).
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from md_supply_demand_agent.data.gcp_catalog import (
    GCP_MACHINE_TYPES,
    GCP_REGIONS_AND_ZONES,
    SPENDARK_2026_MID_MARKET_BENCHMARK,
)
from md_supply_demand_agent.memory.session_store import global_session_store
from md_supply_demand_agent.observability.intent_outcome import global_intent_outcome_auditor
from md_supply_demand_agent.observability.otel_tracer import global_tracer
from md_supply_demand_agent.observability.structured_logger import get_recent_structured_logs
from md_supply_demand_agent.orchestration.hitl import global_hitl_gate
from md_supply_demand_agent.orchestration.multi_agent import global_orchestrator


# ---------------------------------------------------------------------------
# Core Route Handlers (Framework-Agnostic for Both Flask & Stdlib WSGI/HTTP)
# ---------------------------------------------------------------------------
def handle_health() -> Tuple[Dict[str, Any], int]:
    return (
        {
            "status": "HEALTHY",
            "agent_name": "MD-Supply-vs-Demand-Agent",
            "version": "1.0.0",
            "orchestration": global_orchestrator.adk_metadata,
        },
        200,
    )


def handle_get_state(region_filter: Optional[str] = None) -> Tuple[Dict[str, Any], int]:
    supply_pools = global_session_store.query_supply(region=region_filter or None)
    total_initial = sum(int(p["initial_supply"]) for p in supply_pools)
    total_available = sum(int(p["available_supply"]) for p in supply_pools)
    total_allocated = sum(int(p["allocated_supply"]) for p in supply_pools)

    return (
        {
            "status": "SUCCESS",
            "agent_name": "MD-Supply-vs-Demand-Agent",
            "summary_kpis": {
                "total_pools": len(supply_pools),
                "total_initial_supply": total_initial,
                "total_available_supply": total_available,
                "total_allocated_supply": total_allocated,
                "pending_alternatives_count": len(global_hitl_gate.list_pending_confirmations()),
            },
            "supply_pools": supply_pools[:80],
            "fcfs_ledger": global_session_store.get_fcfs_ledger(limit=40),
            "pending_confirmations": global_hitl_gate.list_pending_confirmations(),
            "otel_spans": global_tracer.get_recent_spans(limit=30),
            "intent_vs_outcome_audit": global_intent_outcome_auditor.get_audit_trail(limit=30),
            "structured_logs": get_recent_structured_logs(limit=30),
            "catalog_metadata": {
                "regions": list(GCP_REGIONS_AND_ZONES.keys()),
                "machine_types": list(GCP_MACHINE_TYPES.keys()),
                "spendark_2026_benchmark": SPENDARK_2026_MID_MARKET_BENCHMARK,
            },
        },
        200,
    )


def handle_post_chat(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    session_id = str(payload.get("session_id") or "web-session-01")
    message = str(payload.get("message") or "").strip()
    customer_id = str(payload.get("customer_id") or "Cloud-Enterprise-Customer")

    if not message:
        return {"status": "ERROR", "message": "Message cannot be empty."}, 400

    res = global_orchestrator.handle_chat_turn(
        session_id=session_id,
        user_message=message,
        customer_id=customer_id,
    )
    return res, 200


def handle_post_upload(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    file_content = str(payload.get("file_content") or "")
    file_format = str(payload.get("file_format") or "auto")
    session_id = str(payload.get("session_id") or "web-session-01")
    customer_id = str(payload.get("customer_id") or "MidSized-Enterprise-Customer")

    if not file_content.strip():
        return {"status": "ERROR", "message": "Uploaded demand file content is empty."}, 400

    res = global_orchestrator.handle_file_upload(
        session_id=session_id,
        file_content=file_content,
        file_format=file_format,
        customer_id=customer_id,
    )
    return res, 200


def handle_post_hitl_accept(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    proposal_id = str(payload.get("proposal_id") or "").strip()
    option_rank = int(payload.get("option_rank") or 1)
    customer_id = str(payload.get("customer_id") or "Customer-Operator")
    if not proposal_id:
        return {"status": "ERROR", "message": "`proposal_id` is required."}, 400
    res = global_hitl_gate.approve_and_continue_matching(
        proposal_id=proposal_id,
        option_rank=option_rank,
        reviewer_id=customer_id,
        confirmation_note=f"Customer accepted alternative Option #{option_rank} via UI/API.",
    )
    return res, 200


def handle_post_hitl_reject(payload: Dict[str, Any]) -> Tuple[Dict[str, Any], int]:
    proposal_id = str(payload.get("proposal_id") or "").strip()
    reason = str(payload.get("reason") or "Customer declined recommended alternative.")
    res = global_hitl_gate.reject_alternative(proposal_id=proposal_id, reason=reason)
    return res, 200


# ---------------------------------------------------------------------------
# Flask App Binding (with Built-in Test Client Fallback if Flask is Absent)
# ---------------------------------------------------------------------------
try:
    from flask import Flask, jsonify, request, send_from_directory  # type: ignore

    app = Flask(__name__, static_folder="static", static_url_path="/static")

    @app.route("/")
    def index() -> Any:
        return send_from_directory(app.static_folder, "index.html")

    @app.route("/api/health", methods=["GET"])
    def health() -> Any:
        body, code = handle_health()
        return jsonify(body), code

    @app.route("/api/state", methods=["GET"])
    def get_dashboard_state() -> Any:
        body, code = handle_get_state(request.args.get("region"))
        return jsonify(body), code

    @app.route("/api/chat", methods=["POST"])
    def chat_endpoint() -> Any:
        payload = request.get_json(force=True, silent=True) or {}
        body, code = handle_post_chat(payload)
        return jsonify(body), code

    @app.route("/api/upload-demand", methods=["POST"])
    def upload_demand_endpoint() -> Any:
        if "file" in request.files:
            uploaded = request.files["file"]
            fname = (uploaded.filename or "").lower()
            fmt = "csv" if fname.endswith(".csv") else ("jsonl" if fname.endswith(".jsonl") else "json")
            payload = {
                "file_content": uploaded.read().decode("utf-8", errors="replace"),
                "file_format": fmt,
                "session_id": request.form.get("session_id", "web-session-01"),
                "customer_id": request.form.get("customer_id", "MidSized-Enterprise-Customer"),
            }
        else:
            payload = request.get_json(force=True, silent=True) or {}
        body, code = handle_post_upload(payload)
        return jsonify(body), code

    @app.route("/api/hitl/accept", methods=["POST"])
    def accept_alternative_endpoint() -> Any:
        payload = request.get_json(force=True, silent=True) or {}
        body, code = handle_post_hitl_accept(payload)
        return jsonify(body), code

    @app.route("/api/hitl/reject", methods=["POST"])
    def reject_alternative_endpoint() -> Any:
        payload = request.get_json(force=True, silent=True) or {}
        body, code = handle_post_hitl_reject(payload)
        return jsonify(body), code

    @app.route("/api/reset-supply", methods=["POST"])
    def reset_supply_endpoint() -> Any:
        return jsonify(global_session_store.reset_static_supply_inventory()), 200

except ImportError:
    import socket
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    from urllib.parse import parse_qs, urlparse

    class _DualStackHTTPServer(ThreadingHTTPServer):
        address_family = socket.AF_INET6

        def server_bind(self) -> None:
            try:
                self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
            except Exception:
                pass
            super().server_bind()

    class _MockResponse:
        def __init__(self, body: Dict[str, Any], status_code: int) -> None:
            self._body = body
            self.status_code = status_code

        def get_json(self) -> Dict[str, Any]:
            return self._body

    class _StdlibTestClient:
        def get(self, path: str) -> _MockResponse:
            parsed = urlparse(path)
            qs = parse_qs(parsed.query)
            if parsed.path == "/api/health":
                return _MockResponse(*handle_health())
            if parsed.path == "/api/state":
                region = qs.get("region", [None])[0]
                return _MockResponse(*handle_get_state(region))
            return _MockResponse({"status": "NOT_FOUND"}, 404)

        def post(self, path: str, json: Optional[Dict[str, Any]] = None) -> _MockResponse:
            payload = json or {}
            if path == "/api/chat":
                return _MockResponse(*handle_post_chat(payload))
            if path == "/api/upload-demand":
                return _MockResponse(*handle_post_upload(payload))
            if path == "/api/hitl/accept":
                return _MockResponse(*handle_post_hitl_accept(payload))
            if path == "/api/hitl/reject":
                return _MockResponse(*handle_post_hitl_reject(payload))
            if path == "/api/reset-supply":
                return _MockResponse(global_session_store.reset_static_supply_inventory(), 200)
            return _MockResponse({"status": "NOT_FOUND"}, 404)

    class _StdlibWebApp:
        def test_client(self) -> _StdlibTestClient:
            return _StdlibTestClient()

        def run(self, host: str = "0.0.0.0", port: int = 8080, debug: bool = False) -> None:
            static_html = (Path(__file__).parent / "static" / "index.html").read_bytes()
            client = self.test_client()

            class Handler(BaseHTTPRequestHandler):
                def do_GET(self) -> None:
                    if self.path == "/" or self.path.startswith("/static/index.html"):
                        self.send_response(200)
                        self.send_header("Content-Type", "text/html; charset=utf-8")
                        self.end_headers()
                        self.wfile.write(static_html)
                        return
                    resp = client.get(self.path)
                    self.send_response(resp.status_code)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(resp.get_json()).encode("utf-8"))

                def do_POST(self) -> None:
                    length = int(self.headers.get("Content-Length", "0"))
                    raw = self.rfile.read(length).decode("utf-8", errors="replace") if length else "{}"
                    try:
                        payload = json.loads(raw)
                    except Exception:
                        payload = {"file_content": raw}
                    resp = client.post(self.path, json=payload)
                    self.send_response(resp.status_code)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps(resp.get_json()).encode("utf-8"))

            try:
                server = _DualStackHTTPServer(("::", port), Handler)
                print(f"Serving MD-Supply-vs-Demand-Agent Web UI (dual-stack IPv6/IPv4) on http://[::]:{port}")
            except Exception:
                server = ThreadingHTTPServer((host, port), Handler)
                print(f"Serving MD-Supply-vs-Demand-Agent Web UI on http://{host}:{port}")
            server.serve_forever()

    app = _StdlibWebApp()  # type: ignore


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
