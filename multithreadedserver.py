import socket
from threading import Thread
import time
from commonthread import CommonThread


ADDRESS = "127.0.0.1"

PORT = 2222
def main():


    s = socket.socket()
    s.bind((ADDRESS,PORT))

    s.listen(5)
    print("Listing for clients ...")
    while True:
        c , addr = s.accept()
        print("Client Connected :  "  , addr)
        clientThread = CommonThread(c)
        clientThread.start()

if __name__ == "__main__":
    main()