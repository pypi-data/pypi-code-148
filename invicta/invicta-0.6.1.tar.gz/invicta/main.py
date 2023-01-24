#!/usr/bin/env python3

"""Entry point for Invicta."""

from . import arguments


def main():
    args = arguments.process_args()
    args.func(args)


if __name__ == "__main__":
	main()

