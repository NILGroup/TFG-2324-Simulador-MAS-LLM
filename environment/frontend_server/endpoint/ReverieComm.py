import os
import sys
import time
import datetime
import json
import subprocess
import psutil
from pathlib import Path

local_dir = os.path.dirname(os.path.abspath(__file__))
frontend_dir = os.path.join(local_dir, '../')
backend_dir = os.path.join(frontend_dir, '../../reverie/backend_server/')
executable_file = os.path.join(local_dir, 'backendWrapp.py')

sys.path.append(frontend_dir)
sys.path.append(backend_dir)

__current_file_path__ = f"{local_dir}/{__file__}"

# Este será un fifo
INPUT_ENDPOINT = f"{local_dir}/reverieInput"
# Es un fifo
OUTPUT_ENDPOINT = f"{local_dir}/reverieOutput"

# Aquí se enviarán los errores
ERR_ENDPOINT = f"{local_dir}/reverieError"

# Se encarga de guardar el fichero en el que se almacena el pid del proceso que ejecuta el ReverieServer
PID_INFO_FILE = f"{local_dir}/reverie_pid"

# Almacena los parametros para ejecutar el nuevo ReverieServer
PARAMS_IN_FILE = f"{local_dir}/params_in.json"



from reverie import ReverieServer

class ReverieComm():
  def __init__(self):
    pass

  def comprobar_error(self):
    archivo_error = Path(ERR_ENDPOINT)
    huboError = archivo_error.stat().st_size > 0
    return huboError

  def write_command(self, command):
    in_file = open(INPUT_ENDPOINT, 'w')
    with open(OUTPUT_ENDPOINT, 'r') as out_file:
      in_file.write(command)
      in_file.flush()
      in_file.close()
      ret = out_file.readlines()
    return ret

  def sum_up(self):
    """
    Solicita el resumen de la simulacion al backend
    """
    print("Solicitando resumen")
    return self.write_command("summ_up")

  def run(self, n_steps=1):
    """
    Ejecuta el numero de pasos especificado
    """
    self.write_command(f"run {n_steps}")

  def save(self):
    """
    Guarda el progreso
    """
    self.write_command("save")

  def finish(self):
    """
    Termina la simulación y guarda el progreso
    """
    self.write_command("finish")
    self.cerrar_back()

  def exit(self):
    """
    Termina la simulación
    No guarda el estado
    Y elimina toda la información de la simulación
    """
    self.write_command("exit")
    self.cerrar_back()

  def test(self):
    print("llamando a test")
    self.write_command("test")
    print("test terminado")
  
  def cerrar_back(self):
    with open(PID_INFO_FILE) as reverie_pid_f:
      reverie_pid = int(json.load(reverie_pid_f)["pid"])
    if psutil.pid_exists(reverie_pid):
      try:
        os.waitpid(reverie_pid, 0)
      except ChildProcessError:
        print(f"El proceso {reverie_pid} no es un proceso hijo del proceso actual.")
      except OSError as e:
        if e.errno == os.errno.ECHILD:
            print(f"No hay proceso hijo con PID {reverie_pid}.")
        else:
            raise
    os.remove(PID_INFO_FILE)
  


def generar_back(post_dict):
  def eliminar_back_antiguo():
    if os.path.exists(PID_INFO_FILE):
      with open(PID_INFO_FILE) as reverie_pid_f:
        reverie_pid = int(json.load(reverie_pid_f)["pid"])
      if psutil.pid_exists(reverie_pid):
        ReverieComm().finish()
      else:
        os.remove(PID_INFO_FILE)
    else:
      print("No existe")

  def gen_json(post_dict):
    def traducir_para_back(post_dict):
      """
      Es necesario para transformar el input recibido de JS en el diccionario que se espera en el back
      INPUT:
        un diciconario con el siguiente formato:
        {
          "numPersonajes": ['2'],
          "nombreSimulacion": ["..."],
          
          "nombre1": ["..."],
          "currently1": ["..."]
          "innate1": ["extrovertido", "amigable"...] # por ver, pero asumimos que tendrá ese formato
          "learned1": ["..."]
          "lifestyle1": ["..."]
          
          "nombre2": ["..."],
          "currently2": ["..."]
          "innate2": ["extrovertido", "amigable"...] # por ver, pero asumimos que tendrá ese formato
          "learned2": ["..."]
          "lifestyle2": ["..."]
        }
      OUTPUT:
        {
          valor_nombre_persona1: {innate: "val1, val2, ...", currently: "...", ...}
          valor_nombre_persona2: {innate: ...}
        }
      """
      ret_dict = dict()
      n_pers = int(post_dict["numPersonajes"])
      sim_code = str(post_dict["sim_code"])
      personas_dict = dict()
      for i in range(1, n_pers+1):
        persona_name = post_dict[f"nombre{i}"]
        personas_dict [persona_name] = dict()
        personas_dict [persona_name]['innate'] = post_dict[f"innate{i}"]
        personas_dict [persona_name]['currently'] = post_dict[f"currently{i}"]
        personas_dict [persona_name]['learned'] = post_dict[f"learned{i}"]
        personas_dict [persona_name]['lifestyle'] = post_dict[f"lifestyle{i}"]
      ret_dict = {"sim_code": sim_code.replace(" ", "_"), "personas": personas_dict}
      return ret_dict
    """
    Vuelca los parametros en un archivo .json que leerá el proceso del Back
    """
    json_dict = {}
    json_dict['new'] = True if post_dict['nueva'] == 'si' else False
    json_dict['forked'] = True if 'forked' in post_dict.keys() and post_dict['forked'] == 'si' else False
    if json_dict['new']:
      json_dict['params'] = traducir_para_back(post_dict)
    else:
      json_dict['params'] = post_dict
    
    with open(PARAMS_IN_FILE, 'w') as params_file:
      params_file.write(json.dumps(json_dict))
    return json_dict

  def generar_nuevo_proceso():
    proceso = subprocess.Popen(["python3", f"{executable_file}", f"{PARAMS_IN_FILE}"],cwd=backend_dir)
    return proceso.pid

  def guardar_pid(pid):
    pid_file_meta = dict()
    pid_file_meta['reverie_server_creation_time'] = datetime.datetime.today().strftime("%B %d, %Y, %H:%M:%S")
    pid_file_meta['pid'] = str(pid)
    with open(PID_INFO_FILE, 'w') as pid_file:
      pid_file.write(json.dumps(pid_file_meta, indent=2))

  eliminar_back_antiguo()
  gen_json(post_dict)
  pid = generar_nuevo_proceso()
  guardar_pid(pid)

  return post_dict['sim_code']

def generar_context(sim_code):
  def create_context(rc):
    context = {"sim_code": rc.sim_code,
            "step": rc.step,
            "mode": "simulate"}
    
    persona_names = [(name, name.replace(" ", "_")) for name in rc.personas]
    context['persona_names'] = persona_names

    persona_init_pos = [[name, rc.personas_tile[name][0], rc.personas_tile[name][1]] for name in rc.personas_tile]
    context['persona_init_pos'] = persona_init_pos
    
    return context

  # Esperamos hasta un minuto tratando de generar el back
  i = 60
  while i > 0 and os.path.exists(PARAMS_IN_FILE):
    i -= 1
    print("Esperando a que se genere el back")
    time.sleep(1)
  if i == 10:
    raise Exception("No se pudo crear el ReverieServer")

  rc = ReverieServer.instancia_sencilla(sim_code)
  return create_context(rc)
