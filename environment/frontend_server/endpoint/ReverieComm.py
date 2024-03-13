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

from reverie import ReverieServer

class ReverieComm(ReverieServer):
  pass