import os
import shutil
import time
import argparse
import logging


def setup_logging(log_file):
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def sync_folders(source, replica):
    if not os.path.exists(replica):
        os.makedirs(replica)
        logging.info(f'Created directory: {replica}')

    source_files = set(os.listdir(source))
    replica_files = set(os.listdir(replica))

    for file_name in source_files:
        source_path = os.path.join(source, file_name)
        replica_path = os.path.join(replica, file_name)

        if os.path.isdir(source_path):
            sync_folders(source_path, replica_path)
        else:
            if file_name not in replica_files or not files_match(source_path, replica_path):
                shutil.copy2(source_path, replica_path)
                logging.info(f'Copied: {source_path} -> {replica_path}')

    for file_name in replica_files - source_files:
        replica_path = os.path.join(replica, file_name)
        if os.path.isdir(replica_path):
            shutil.rmtree(replica_path)
            logging.info(f'Removed directory: {replica_path}')
        else:
            os.remove(replica_path)
            logging.info(f'Removed file: {replica_path}')


def files_match(file1, file2):
    return os.path.getmtime(file1) == os.path.getmtime(file2)


def main():
    parser = argparse.ArgumentParser(description='Synchronize two folders.')
    parser.add_argument('source', type=str, nargs='?', default='./source', help='Source folder path')
    parser.add_argument('replica', type=str, nargs='?', default='./replica', help='Replica folder path')
    parser.add_argument('interval', type=int, nargs='?', default=10, help='Synchronization interval in seconds')
    parser.add_argument('log_file', type=str, nargs='?', default='./sync.log', help='Log file path')

    args = parser.parse_args()

    os.makedirs(args.source, exist_ok=True)
    os.makedirs(args.replica, exist_ok=True)
    setup_logging(args.log_file)

    while True:
        sync_folders(args.source, args.replica)
        time.sleep(args.interval)


if __name__ == '__main__':
    main()
