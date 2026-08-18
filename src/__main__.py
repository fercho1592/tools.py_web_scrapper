import argparse
import asyncio

from contracts.enums.queue_enum import QueueNameEnum


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the manga processing flow.")
    parser.add_argument(
        "--queue",
        choices=QueueNameEnum.choices(),
        help="Start listening a specific queue instead of running the sequential flow.",
    )
    return parser.parse_args()


async def main():
    args = parse_args()

    if args.queue:
        from queue_listener import main as run_queue_listener

        run_queue_listener()
        return

    from waterfall_worker import main as run_waterfall_worker

    await run_waterfall_worker()


if __name__ == "__main__":
    asyncio.run(main())
