import os
import ReverieComm
import sys
import time

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        if not os.path.exists(ReverieComm.INPUT_ENDPOINT):
            os.mkfifo(ReverieComm.INPUT_ENDPOINT)

        fdIn = os.open(ReverieComm.INPUT_ENDPOINT, os.O_RDONLY | os.O_CREAT)
        os.dup2(fdIn, 0)
        os.close(fdIn)
        
        fdOut = os.open(ReverieComm.OUTPUT_ENDPOINT, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        os.dup2(fdOut, 1)
        os.close(fdOut)
        
        fdErr = os.open(ReverieComm.ERR_ENDPOINT, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
        os.dup2(fdErr, 2)
        os.close(fdErr)

        i = 0
        while True:
            try:
                variable = sys.stdin.readline()
                if not variable:
                    pass
                if (len(variable) == 0):
                    time.sleep(1)
                else:
                    i += 1
                    print(f"{i}:")
                    print("Esto es lo que me has dado: ", variable)
            except Exception as e:
                """
                Si ocurre algún error inesperado habría que eliminar el proceso del ReverieServer desde una excepción como esta
                Quizá la excepción se haría en la reescritura de start_server, donde se esperan los comandos
                """
                print(e.with_traceback, file=sys.stderr)
                        
    else:
        print(pid)
