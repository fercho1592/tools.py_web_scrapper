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
    parser.add_argument(
        "--prepare-links",
        metavar="FILE",
        help="Read manga links from a file and prepare a queue-ready output file.",
    )
    return parser.parse_args()


async def main():
    args = parse_args()

    if args.prepare_links:
        from prepare_links_worker import main as run_prepare_links_worker

        run_prepare_links_worker(args.prepare_links)
        return

    if args.queue:
        from queue_listener import main as run_queue_listener

        run_queue_listener()
        return

    from waterfall_worker import main as run_waterfall_worker

    await run_waterfall_worker()


if __name__ == "__main__":
    asyncio.run(main())
