
import subprocess
import psutil

PING_CMD = ["ping", "-c", "2", "google.com"]


def check_internet():
    try:
        r = subprocess.run(PING_CMD, capture_output=True)
        return r.returncode == 0
    except Exception:
        return False


def get_disks():
    disks = []

    for part in psutil.disk_partitions(all=False):
        try:
            usage = psutil.disk_usage(part.mountpoint)
        except PermissionError:
            continue

        disks.append({
            "device": part.device,
            "mount": part.mountpoint,
            "total": usage.total,
            "used": usage.used,
            "free": usage.free
        })

    return disks


