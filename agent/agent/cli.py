"""CLI entrypoint — `python -m agent.cli <command> [args]`.

Commands:
    runner --brand-id 1 --n-runs 3
    parse --response-id 100
    diagnose --brand-id 1 --prompt-id 5
"""
import argparse
import asyncio
import sys


def main() -> None:
    parser = argparse.ArgumentParser(prog="agent", description="GEO AI Agent CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # runner
    runner_p = subparsers.add_parser("runner", help="Run scan for a brand")
    runner_p.add_argument("--brand-id", type=int, required=True)
    runner_p.add_argument("--prompt-ids", type=int, nargs="*", default=None)
    runner_p.add_argument("--engines", type=str, nargs="*", default=None,
                          help="Engine names: chatgpt, claude, gemini (LLM) hoặc tavily (search). Default = all 4.")
    runner_p.add_argument("--n-runs", type=int, default=3)
    runner_p.add_argument("--once", action="store_true", help="Run once (no scheduler)")

    # parse
    parse_p = subparsers.add_parser("parse", help="Parse mentions from response")
    parse_p.add_argument("--response-id", type=int, required=True)

    # diagnose
    diag_p = subparsers.add_parser("diagnose", help="Run diagnosis on (brand, prompt)")
    diag_p.add_argument("--brand-id", type=int, required=True)
    diag_p.add_argument("--prompt-id", type=int, required=True)

    args = parser.parse_args()

    if args.command == "runner":
        from agent.runner.orchestrator import run_scan
        asyncio.run(run_scan(
            brand_id=args.brand_id,
            prompt_ids=args.prompt_ids,
            ai_engines=args.engines,
            n_runs=args.n_runs,
        ))
    elif args.command == "parse":
        from agent.parser.mention_parser import parse_response
        asyncio.run(parse_response(args.response_id))
    elif args.command == "diagnose":
        from agent.diagnosis.agent import diagnose
        asyncio.run(diagnose(brand_id=args.brand_id, prompt_id=args.prompt_id))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
