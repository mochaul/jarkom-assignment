import socket, os, platform

def server():
    TCP_IP = "localhost"
    TCP_PORT = 2603
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as netSocket:
        netSocket.bind((TCP_IP, TCP_PORT))
        netSocket.listen(1)
        print("Server ready!")
        return netSocket.accept()

def hardware_info():
    data = dict(arsitektur=platform.architecture()[0], vendor="", core="", clock="", cache="")
    with open('/proc/cpuinfo') as f:
        for line in f:
        # Ignore the blank line separating the information between
        # details about two processing units
            if line.strip():
                data_line = line.rstrip('\n')
                if data_line.startswith('vendor_id'):
                    vendor = line.rstrip('\n').split(':')[1]
                    data["vendor"] = vendor
                if data_line.startswith('model name'):
                    name = line.rstrip('\n').split(':')[1]
                    data["core"] = name
                if data_line.startswith('cpu MHz'):
                    clock = line.rstrip('\n').split(':')[1]
                    data["clock"] = "{:.2f}".format(float(clock) / 1000)
                if data_line.startswith('cache size'):
                    cache = line.rstrip('\n').split(':')[1]
                    data["cache"] = cache
    return data

def physical_mem_info():
    data = dict(total="", used="", free="")
    p = os.popen("vmstat -s | grep 'total memory'")
    data["total"] = str(p.read())
    p = os.popen("vmstat -s | grep 'used memory'")
    data["used"] = str(p.read())
    p = os.popen("vmstat -s | grep 'free memory'")
    data["free"] = str(p.read())
    return data

def swap_mem_info():
    data = dict(total="", used="", free="")
    with os.popen("vmstat -s | grep 'total swap'") as p:
        data["total"] = str(p.read())
    with os.popen("vmstat -s | grep 'used swap'") as p:
        data["used"] = str(p.read())
    with os.popen("vmstat -s | grep 'free swap'") as p:
        data["free"] = str(p.read())
    return data

def storage_info():
    p = os.popen('df -h')
    return str(p.read())

def conn_status():
    #Pinging default gateway
    with os.popen("ping -q -w 1 -c 1 `ip r | grep default | cut -d ' ' -f 3` > /dev/null && echo ok || echo error") as p:
        if p.read() == "ok":
            return "Status: Online"
        else:
            return "Status: Offline"

def last_login():
    result = ""
    with os.popen("last") as p:
        result += p.read()
    # with os.popen("lastb") as p:
    #     result += p.read()
    return result

def print_hardware():
    hw_info = hardware_info()
    hw_str = "Hardware Info:\n"
    hw_str += "\ta. Arsitektur: {}\n".format(hw_info["arsitektur"])
    hw_str += "\tb. Model processor\n"
    hw_str += "\t\t  i. {}\n".format(hw_info["vendor"])
    hw_str += "\t\t ii. {}\n".format(hw_info["core"])
    hw_str += "\t\tiii. {} GHz\n".format(hw_info["clock"])
    hw_str += "\tc. Besaran cache: {}\n".format(hw_info["cache"])
    return hw_str

def print_physical_mem():
    pm_info = physical_mem_info()
    pm_str = "Memori fisik\n"
    pm_str += "\ta. Total: {}\n".format(pm_info["total"])
    pm_str += "\tb. Used: {}\n".format(pm_info["used"])
    pm_str += "\tb. Free: {}\n".format(pm_info["free"])
    return pm_str

def print_swap_mem():
    sm_info = swap_mem_info()
    sm_str = "Memori swap\n"
    sm_str += "\ta. Total: {}\n".format(sm_info["total"])
    sm_str += "\tb. Used: {}\n".format(sm_info["used"])
    sm_str += "\tb. Free: {}\n".format(sm_info["free"])
    return sm_str

def print_storage():
    storage_str = "Storage\n"
    storage_str += "\t" + storage_info() + "\n"
    return storage_str

def print_connection_status():
    conn_str = "Status koneksi ke internet\n"
    conn_str += conn_status()  + "\n\n"
    return conn_str

def print_last_login():
    acc_str = "Akses\n"
    acc_str += "\t" + last_login() + "\n"
    return acc_str

if __name__ == "__main__":
    conn, addr = server()
    BUFFER_SIZE = 1024
    print ("Connection address: ", addr)
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data: break
        data_str= data.decode('utf-8')
        data_sent = ""
        if data_str == "-h":
            data_sent = print_hardware()
        elif data_str == "-p":
            data_sent = print_physical_mem()
        elif data_str == "-s":
            data_sent = print_swap_mem()
        elif data_str == "-t":
            data_sent = print_storage()
        elif data_str == "-c":
            data_sent = print_connection_status
        elif data_str == "-l":
            data_sent = print_last_login()
        elif data_str == "-a":
            data_sent = print_hardware()
            data_sent += print_physical_mem()
            data_sent += print_swap_mem()
            data_sent += print_storage()
            data_sent += print_connection_status()
            data_sent += print_last_login()
        conn.send(data_sent.encode('utf-8'))
    conn.close()