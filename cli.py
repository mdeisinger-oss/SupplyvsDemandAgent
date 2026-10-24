"""Interactive Terminal CLI for MD-Supply-vs-Demand-Agent."""

import argparse
import json
import sys
from pathlib import Path

from md_supply_demand_agent.orchestration.multi_agent import global_orchestrator


def main() -> None:
    parser = argparse.ArgumentParser(
        description="MD-Supply-vs-Demand-Agent CLI (Chat & Demand File Upload)"
    )
    parser.add_argument(
        "--query",
        "-q",
        type=str,
        help="Single natural-language demand request or query.",
    )
    parser.add_argument(
        "--upload-file",
        "-f",
        type=str,
        help="Path to a .csv, .json, or .jsonl demand file to match via FCFS.",
    )
    parser.add_argument(
        "--customer-id",
        "-c",
        type=str,
        default="CLI-Enterprise-Customer",
        help="Customer identifier.",
    )
    args = parser.parse_args()

    if args.upload_file:
        path = Path(args.upload_file)
        if not path.exists():
            sys.stderr.write(f"Error: File not found: {path}\n")
            sys.exit(1)
        content = path.read_text(encoding="utf-8")
        res = global_orchestrator.handle_file_upload(
            session_id="cli-session",
            file_content=content,
            file_format="auto",
            customer_id=args.customer_id,
        )
        print(res.get("response_markdown", json.dumps(res, indent=2)))
        return

    if args.query:
        res = global_orchestrator.handle_chat_turn(
            session_id="cli-session",
            user_message=args.query,
            customer_id=args.customer_id,
        )
        print(res.get("response_markdown", json.dumps(res, indent=2)))
        return

    print("=======================================================================")
    print("  MD-Supply-vs-Demand-Agent | Interactive Terminal Session")
    print("  Type a capacity request, 'upload <path>', or 'exit' to quit.")
    print("=======================================================================")
    while True:
        try:
            user_in = input("\n[Customer] > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break
        if not user_in or user_in.lower() in ("exit", "quit"):
            break
        if user_in.lower().startswith("upload "):
            fpath = Path(user_in[7:].strip())
            if not fpath.exists():
                print(f"File not found: {fpath}")
                continue
            res = global_orchestrator.handle_file_upload(
                session_id="cli-session",
                file_content=fpath.read_text(encoding="utf-8"),
                customer_id=args.customer_id,
            )
            print("\n" + res.get("response_markdown", ""))
        else:
            res = global_orchestrator.handle_chat_turn(
                session_id="cli-session",
                user_message=user_in,
                customer_id=args.customer_id,
            )
            print("\n" + res.get("response_markdown", ""))


if __name__ == "__main__":
    main()
