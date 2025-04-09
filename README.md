One-way synchronization ✅

The function sync_folders(source, replica) ensures that the content of replica exactly matches source.

Adding new files: If a file exists in source but not in replica, it is copied:


if file_name not in replica_files or not files_match(source_path, replica_path):
    shutil.copy2(source_path, replica_path)
    logging.info(f'Copied: {source_path} -> {replica_path}')
Removing unnecessary files: If a file exists in replica but not in source, it is deleted:


for file_name in replica_files - source_files:
    os.remove(replica_path)
    logging.info(f'Removed file: {replica_path}')
Periodic synchronization ✅

The while True: loop in main() ensures that synchronization happens at regular intervals:

while True:
    sync_folders(args.source, args.replica)
    time.sleep(args.interval)
The interval is defined by the user (default is 10 seconds).

Logging of file operations ✅

Logging is configured in the setup_logging(log_file) function:

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
All operations are saved to a log file and displayed in the console, e.g.:


logging.info(f'Copied: {source_path} -> {replica_path}')
logging.info(f'Removed file: {replica_path}')
Command-line arguments support ✅

The program reads folder paths, synchronization interval, and log file path from command-line arguments:

parser.add_argument('source', type=str, nargs='?', default='./source')
parser.add_argument('replica', type=str, nargs='?', default='./replica')
parser.add_argument('interval', type=int, nargs='?', default=10)
parser.add_argument('log_file', type=str, nargs='?', default='./sync.log')
If arguments are missing, the program creates default directories and a log file.

No use of third-party folder synchronization libraries ✅

The code does not use external libraries like rsync or dirsync.

All operations (copying, deleting, comparing files) are implemented manually using os, shutil, and time.

Allowed use of well-known algorithms ✅

File comparison is done using modification time (os.path.getmtime()):

def files_match(file1, file2):
    return os.path.getmtime(file1) == os.path.getmtime(file2)
Can be easily extended to use MD5 checksums for more precise comparison.
