#!/usr/bin/env python3
from src.datauploader import Uploader

def main() -> None:
    du = Uploader()
    du.run()


if __name__ == '__main__':
    main()