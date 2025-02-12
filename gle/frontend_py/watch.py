import sys
import time
import subprocess
import os

def watch_for_changes(filename):
    mtime = 0
    process = None
    while True:
        stat = os.stat(filename)
        if stat.st_mtime != mtime:
            mtime = stat.st_mtime
            if process:
                process.terminate()
            process = subprocess.Popen([sys.executable, filename])
        time.sleep(1)

if __name__ == "__main__":
    watch_for_changes(sys.argv[1])
