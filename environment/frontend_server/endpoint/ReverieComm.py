import os
import sys
local_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(local_dir, '../')
backend_dir = os.path.join(frontend_dir, '../../reverie/backend_server/')

sys.path.append(frontend_dir)
sys.path.append(backend_dir)

# Este será un fifo
INPUT_ENDPOINT = f"{local_dir}/reverieInput"

# Este es un regular file
# Preferiría hacerlo fifo, pero si no hay nadie leyendo se bloquea
OUTPUT_ENDPOINT = f"{local_dir}/reverieOutput"

# Aquí se enviarán los errores
ERR_ENDPOINT = f"{local_dir}/reverieError"

PID_INFO_FILE = f"{local_dir}/reverie_pid"

from reverie import ReverieServer

class ReverieComm(ReverieServer):
  def redirect_std(self):
    if not os.path.exists(ReverieComm.INPUT_ENDPOINT):
      os.mkfifo(INPUT_ENDPOINT)

    fdIn = os.open(INPUT_ENDPOINT, os.O_RDONLY | os.O_CREAT)
    os.dup2(fdIn, 0)
    os.close(fdIn)
    
    fdOut = os.open(OUTPUT_ENDPOINT, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    os.dup2(fdOut, 1)
    os.close(fdOut)
    
    fdErr = os.open(ERR_ENDPOINT, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    os.dup2(fdErr, 2)
    os.close(fdErr)

  def __init__(self,
               forked,
               params):
    # Redirigimos el input output que usará el reverie server a los pipes
    self.redirect_std()

    # Creamos el Reverie Server == Los archivos de la nueva simulación
    ReverieServer.__ini__(forked, params)

    # Guardamos el pid en un fichero para terminar el proceso cuando se termine con la simulacion desde el front
    with open(PID_INFO_FILE, 'w') as pid_file:
      pid_file.write(os.getpid())
    
    # Si ocurre algun problema desde el back se aborta la ejecución de la simulación y escribimos los fallos en la salida de error
    try:
      self.open_server()
    except Exception as e:
      print(e.with_traceback, file=sys.stderr)

  @staticmethod
  def write_command(command):
    with open(INPUT_ENDPOINT, 'w') as in_file:
      in_file.write(command)

  @staticmethod
  def run(n_steps):
    """
    Ejecuta el numero de pasos especificado
    """
    ReverieComm.write_command(f"run {n_steps}")

  @staticmethod
  def save():
    """
    Guarda el progreso
    """
    ReverieComm.write_command("save")

  @staticmethod
  def finish():
    """
    Termina la simulación y guarda el progreso
    """
    ReverieComm.write_command("finish")

  @staticmethod
  def exit():
    """
    Termina la simulación
    No guarda el estado
    Y elimina toda la información de la simulación
    """
    ReverieComm.write_command("exit")