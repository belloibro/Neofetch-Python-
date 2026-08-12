import platform, os, subprocess, json

def show_fetch():
    uname = platform.uname()

    # RAM Info
    mem_total, mem_free = "N/A", "N/A"
    try:
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if 'MemTotal' in line:
                    mem_total = f"{int(line.split()[1]) // 1024}MB"
                elif 'MemAvailable' in line:
                    mem_free = f"{int(line.split()[1]) // 1024}MB"
    except Exception:
        pass

    # Storage Info
    storage_total, storage_free = "N/A", "N/A"
    try:
        st = os.statvfs('/data/data/com.termux/files/home')
        storage_total = f"{(st.f_blocks * st.f_frsize) // (1024**3)}GB"
        storage_free = f"{(st.f_bavail * st.f_frsize) // (1024**3)}GB"
    except Exception:
        pass

    # Battery Info
    battery_status = "N/A"
    try:
        out = subprocess.check_output(["termux-battery-status"], timeout=3).decode('utf-8')
        bdata = json.loads(out)
        battery_status = f"{bdata.get('percentage')}% ({bdata.get('status')})"
    except Exception:
        pass

    print("\033[1;34m" + r"""
  _____                          _ 
 |_   _|__ _ __ _ __ ___  _   _| |
   | |/ _ \ '__| '_ ` _ \| | | | |
   | |  __/ |  | | | | | | |_| |_|
   |_|\___|_|  |_| |_| |_|\__,_(_)
""" + "\033[0m")

    print(f"\033[1;32mOS:\033[0m {uname.system} {uname.release}")
    print(f"\033[1;32mNode:\033[0m {uname.node}")
    print(f"\033[1;32mArch:\033[0m {uname.machine}")
    print(f"\033[1;32mRAM Total / Free:\033[0m {mem_total} / {mem_free}")
    print(f"\033[1;32mStorage Total / Free:\033[0m {storage_total} / {storage_free}")
    if battery_status != "N/A":
        print(f"\033[1;32mBattery:\033[0m {battery_status}")

if __name__ == "__main__":
    show_fetch()
