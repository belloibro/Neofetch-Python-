import platform, os

def show_fetch():
    uname = platform.uname()

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
    print(f"\033[1;32mMemory Total:\033[0m {mem_total}")
    print(f"\033[1;32mMemory Available:\033[0m {mem_free}")

if __name__ == "__main__":
    show_fetch()
