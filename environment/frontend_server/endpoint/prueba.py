import os
import ReverieComm
import sys

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        if not os.path.exists(ReverieComm.INPUT_ENDPOINT):
            os.mkfifo(ReverieComm.INPUT_ENDPOINT)
        with open(ReverieComm.OUTPUT_ENDPOINT, 'w') as out_f:
            
            fdIn = os.open(ReverieComm.INPUT_ENDPOINT, os.O_RDONLY | os.O_CREAT)
            fdOut = out_f.fileno()

            os.dup2(fdIn, 0)
            os.dup2(fdOut, 1)
            
            variable = sys.stdin.readline()
                
            print("Esto es lo que me has dado: ", variable)
            print(f"Ha leido los datos {variable}")
            os.close(fdIn)
    else:
        print(os.getpid(), pid)
