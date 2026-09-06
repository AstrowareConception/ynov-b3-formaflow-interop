from __future__ import annotations

import argparse

from astrobridge.messaging.consumer import consume_once


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("consumer", choices=["administration", "notification"])
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()
    for _ in range(args.count):
        print(consume_once(args.consumer))


if __name__ == "__main__":
    main()
