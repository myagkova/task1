import getopt
import subprocess
import sys
import time
from datetime import datetime

import psutil


def monitor_process_statistics(path, interval):
    p = subprocess.Popen(path, shell=True, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    process = psutil.Process(p.pid)
    print('time', 'cpu_usage', 'resident_set_size', 'virtual_memory_size',
          'file_descriptor', sep=";")
    while True:
        if p.poll() is not None:
            return
        with process.oneshot():
            cpu_usage = process.cpu_percent()
            memory_info = process.memory_full_info()
            rss = memory_info.rss
            vms = memory_info.vms
            num_fds = process.num_fds()
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(current_time, cpu_usage, rss, vms, num_fds, sep=";")
            time.sleep(interval)


def main(argv):
    process = ''
    interval = ''
    try:
        opts, args = getopt.getopt(argv, "h", ["process=", "interval="])
    except getopt.GetoptError:
        print(
            'test.py -process home/Telegram -interval 30')
        return
    for opt, arg in opts:
        if opt == '-h':
            print(
                'test.py -process home/Telegram -interval 30')
            return
        elif opt == "--process":
            process = arg
        elif opt == "--interval":
            interval = int(arg)
    monitor_process_statistics(process, interval)


if __name__ == '__main__':
    main(sys.argv[1:])
