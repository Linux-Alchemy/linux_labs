# system status checker

# system_status.py

import psutil
import datetime
import os
import subprocess
import speedtest

log_file = os.path.expanduser("~/cron_status.log") # log file path

# getting the system stats
# CPU, Memory, Disk usage
def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    return cpu, memory, disk

# checking internet connectivity with ping on google server
def check_internet():
    try:
        subprocess.check_output(["ping", "-c", "1", "8.8.8.8"])
        return "OK"
    except subprocess.CalledProcessError:
        return "DOWN"

# checking the internet speed
def speed_test():
    speed = speedtest.Speedtest()
    speed.get_best_server()

    download_speed = speed.download() / 10**6  # convert to Mbps
    upload_speed = speed.upload() / 10**6      # convert to Mbps

    return round(download_speed, 2), round(upload_speed, 2)

# logging the system status to a file with timestamp
def log_status():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu, mem, disk = get_system_stats()
    net_status = check_internet()

    if net_status == "OK":
        #try:
            download, upload = speed_test()
        #except:
         #   download, upload = 0, 0
    else:
        download, upload = 0, 0

    with open(log_file, "a") as f:
        f.write(f"[{timestamp}]\n")
        f.write(f"CPU: {cpu:.1f}%\n")
        f.write(f"Memory: {mem:.1f}%\n")
        f.write(f"Disk: {disk:.1f}%\n")
        f.write(f"Internet: {net_status}\n")
        f.write(f"Download: {download} Mbps\n")
        f.write(f"Upload: {upload} Mbps\n\n")

if __name__ == "__main__":
    log_status()

