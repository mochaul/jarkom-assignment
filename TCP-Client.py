import socket, sys

def client(args):
    print("for help type: python TCPClient.py --help")
    if args[1] == "--help":
        print("usage:")
        print("python TCPClient.py -s IP -p port -h //informasi hardware")
        print("python TCPClient.py -s IP -p port -p //informasi memori fisik")
        print("python TCPClient.py -s IP -p port -s //informasi swap memori")
        print("python TCPClient.py -s IP -p port -t //informasi storage")
        print("python TCPClient.py -s IP -p port -c //status koneksi")
        print("python TCPClient.py -s IP -p port -l //terakhir login")
        print("python TCPClient.py -s IP -p port -a //tampilkan semua informasi")
    else:
        TCP_IP = args[2]
        TCP_PORT = int(args[4])
        OPTION = bytes(args[-1], 'utf-8')
        BUFFER_SIZE = 1024
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as netSocket:
            netSocket.connect((TCP_IP, TCP_PORT))
            netSocket.send(OPTION)
            data = netSocket.recv(BUFFER_SIZE)
            data_str = data.decode('utf-8')
            print(data_str)
            netSocket.close()

if __name__ == "__main__":
    client(sys.argv)