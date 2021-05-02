from pyflightcoach.manage_logs import LogRegister, LogHandle
from pathlib import Path


reg = LogRegister.from_folder(Path('data/private_logs'))