"""Run baseline scan (chỉ định brand + prompts)."""
import argparse
import asyncio

from agent.runner.orchestrator import run_scan


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand-id", type=int, required=True)
    parser.add_argument("--prompt-ids", type=int, nargs="*", default=None)
    parser.add_argument("--ai-engines", type=str, nargs="*", default=None)
    parser.add_argument("--n-runs", type=int, default=3)
    args = parser.parse_args()

    result = await run_scan(
        brand_id=args.brand_id,
        prompt_ids=args.prompt_ids,
        ai_engines=args.ai_engines,
        n_runs=args.n_runs,
    )
    print(f"Result: {result}")


if __name__ == "__main__":
    asyncio.run(main())
