import os, sys, json, time

local_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(local_dir, '../')
backend_dir = os.path.join(frontend_dir, '../../reverie/backend_server/')

sys.path.append(frontend_dir)
sys.path.append(backend_dir)

from reverie import ReverieServer

# Este será un fifo
INPUT_ENDPOINT = f"{local_dir}/reverieInput"

# Este es un regular file
# Preferiría hacerlo fifo, pero si no hay nadie leyendo se bloquea
OUTPUT_ENDPOINT = f"{local_dir}/reverieOutput"

# Aquí se enviarán los errores
ERR_ENDPOINT = f"{local_dir}/reverieError"

def cargar_reverieServer(json_path):
  json_path = sys.argv[1]
  with open(json_path,'r') as json_file:
    params = json.load(json_file)
  new = params['new']
  forked = params['forked']
  params = params['params']
  if new:
    rc = ReverieServer(new, forked, params=[params['sim_code'], params['personas']])
  elif forked:
    rc = ReverieServer(new, forked, params=[params['fork_sim_code'], params['sim_code']])
  else:
    rc = ReverieServer(new, forked, params=[params['sim_code']])
  return rc

def configurar_comunicacion(o_f):
  if not os.path.exists(INPUT_ENDPOINT):
    os.mkfifo(INPUT_ENDPOINT)
  if not os.path.exists(OUTPUT_ENDPOINT):
    os.mkfifo(OUTPUT_ENDPOINT)

  fdIn = open(INPUT_ENDPOINT, 'r')

  fdOut = open(OUTPUT_ENDPOINT, 'w')

  fdErr = open(ERR_ENDPOINT, 'w')
  
  o_f.append(fdErr.fileno()+1)
  o_f.append(fdErr.fileno()+2)
  o_f.append(fdErr.fileno()+3)

  os.dup2(0, o_f[0])
  os.dup2(1, o_f[1])
  os.dup2(2, o_f[2])

  os.close(0)
  os.close(1)
  os.close(2)

  os.dup2(fdIn.fileno(), 0)
  os.dup2(fdOut.fileno(), 1)
  os.dup2(fdErr.fileno(), 2)
  
  fdIn.close()
  fdOut.close()
  fdErr.close()

def cerrar_comunicacion(o_f):
  os.close(0)
  os.close(1)
  os.close(2)

  os.dup2(o_f[0],0)
  os.dup2(o_f[1],1)
  os.dup2(o_f[2],2)

  os.close(o_f[0])
  os.close(o_f[1])
  os.close(o_f[2])

  o_f.clear()

def exec_command(rc):
  command = input().strip()
  rc.exec_command(command)



if __name__ == '__main__':
  # Recibo ruta de json con
  # new, forked, params: {sim_code, fork_sim_code, personas}
  json_path = sys.argv[1]
  rc = cargar_reverieServer(json_path=json_path)
  os.remove(json_path)
  if os.path.exists(ERR_ENDPOINT):
    os.remove(ERR_ENDPOINT)
  old_fds = []
  while not rc.stopped:
    configurar_comunicacion(old_fds)
    exec_command(rc)
    cerrar_comunicacion(old_fds)
    time.sleep(0.5)
