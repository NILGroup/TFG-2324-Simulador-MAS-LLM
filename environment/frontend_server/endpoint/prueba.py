import os
import ReverieComm
import sys
import time

if __name__ == '__main__':
    pid = os.fork()
    if pid == 0:
        if not os.path.exists(ReverieComm.INPUT_ENDPOINT):
            os.mkfifo(ReverieComm.INPUT_ENDPOINT)
        with open(ReverieComm.OUTPUT_ENDPOINT, 'w') as out_f:
            with open(ReverieComm.ERR_ENDPOINT, 'w') as out_err:
                fdIn = os.open(ReverieComm.INPUT_ENDPOINT, os.O_RDONLY | os.O_CREAT)
                fdOut = out_f.fileno()
                fdErr = out_err.fileno()
                
                os.dup2(fdIn, 0)
                os.dup2(fdOut, 1)
                os.dup2(fdErr, 2)
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
                        

                os.close(fdIn)
    else:
        print(pid)
