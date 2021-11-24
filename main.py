from .options import get_parser
from multiprocessing import Process
from .syn_content import synchronize_content


def main():
    args = get_parser()
    synchronize_content(args.root, args.interval_time)


if __name__ == "__main__":
    main()