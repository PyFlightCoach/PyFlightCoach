from pathlib import Path
import os
from datetime import datetime
import shutil
import argparse

parser = argparse.ArgumentParser(description='Collect logs from a memory card')
parser.add_argument('-s', '--source', nargs='?', help='folder to get logs from if not /media/*')
parser.add_argument('-t', '--target', nargs='?', help='folder to save logs in if not current')

args = parser.parse_args()

source_folder = args.source if args.source else Path('/media/') 
target_folder = args.target if args.target else Path()

all_logs = sorted(list(source_folder.rglob('*.BIN')))

for file in all_logs:

    date = datetime.fromtimestamp(os.path.getmtime(file))
    folder = Path(date.strftime('%Y_%m_%d'))
    folder.mkdir(exist_ok=True)
    
    if not (folder / file.name).exists():
        print(f'copying {file} to {folder / file.name}')
        shutil.copyfile(file, folder / file.name )
    