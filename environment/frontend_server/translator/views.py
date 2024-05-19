"""
Author: Joon Sung Park (joonspk@stanford.edu)
File: views.py
"""
import os
import sys
import string
import random
import json
from os import listdir
import os

import datetime
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse

from global_methods import *

from django.contrib.staticfiles.templatetags.staticfiles import static
from translator.models import *

from endpoint.ReverieComm import generar_back, generar_context, ReverieComm, PID_INFO_FILE

sys.path.append('../../reverie/')

from compress_sim_storage import compress


"""
No encuentra el archivo para comprimir
# import compressed_sim_storage
"""





def landing(request): 
  context = {}
  template = "landing/landing.html"
  return render(request, template, context)


def demo(request, sim_code, step, play_speed="2"): 
  move_file = f"compressed_storage/{sim_code}/master_movement.json"
  meta_file = f"compressed_storage/{sim_code}/meta.json"
  step = int(step)
  play_speed_opt = {"1": 1, "2": 2, "3": 4,
                    "4": 8, "5": 16, "6": 32}
  if play_speed not in play_speed_opt: play_speed = 2
  else: play_speed = play_speed_opt[play_speed]

  # Loading the basic meta information about the simulation.
  meta = dict() 
  with open (meta_file) as json_file: 
    meta = json.load(json_file)

  sec_per_step = meta["sec_per_step"]
  start_datetime = datetime.datetime.strptime(meta["start_date"] + " 00:00:00", 
                                              '%B %d, %Y %H:%M:%S')
  for i in range(step): 
    start_datetime += datetime.timedelta(seconds=sec_per_step)
  start_datetime = start_datetime.strftime("%Y-%m-%dT%H:%M:%S")

  # Loading the movement file
  raw_all_movement = dict()
  with open(move_file) as json_file: 
    raw_all_movement = json.load(json_file)
 
  # Loading all names of the personas
  persona_names = dict()
  persona_names = []
  persona_names_set = set()
  for p in list(raw_all_movement["0"].keys()): 
    persona_names += [{"original": p, 
                       "underscore": p.replace(" ", "_"), 
                       "initial": p[0] + p.split(" ")[-1][0]}]
    persona_names_set.add(p)

  # <all_movement> is the main movement variable that we are passing to the 
  # frontend. Whereas we use ajax scheme to communicate steps to the frontend
  # during the simulation stage, for this demo, we send all movement 
  # information in one step. 
  all_movement = dict()

  # Preparing the initial step. 
  # <init_prep> sets the locations and descriptions of all agents at the
  # beginning of the demo determined by <step>. 
  init_prep = dict() 
  for int_key in range(step+1): 
    key = str(int_key)
    val = raw_all_movement[key]
    for p in persona_names_set: 
      if p in val: 
        init_prep[p] = val[p]
  persona_init_pos = dict()
  for p in persona_names_set: 
    persona_init_pos[p.replace(" ","_")] = init_prep[p]["movement"]
  all_movement[step] = init_prep

  # Finish loading <all_movement>
  for int_key in range(step+1, len(raw_all_movement.keys())): 
    all_movement[int_key] = raw_all_movement[str(int_key)]

  context = {"sim_code": sim_code,
             "step": step,
             "persona_names": persona_names,
             "persona_init_pos": json.dumps(persona_init_pos), 
             "all_movement": json.dumps(all_movement), 
             "start_datetime": start_datetime,
             "sec_per_step": sec_per_step,
             "play_speed": play_speed,
             "mode": "demo"}
  template = "demo/demo.html"

  return render(request, template, context)


def UIST_Demo(request): 
  return demo(request, "March20_the_ville_n25_UIST_RUN-step-1-141", 2160, play_speed="3")


def home(request):
  f_curr_sim_code = "temp_storage/curr_sim_code.json"
  f_curr_step = "temp_storage/curr_step.json"

  if not check_if_file_exists(f_curr_step): 
    context = {}
    template = "home/error_start_backend.html"
    return render(request, template, context)

  with open(f_curr_sim_code) as json_file:  
    sim_code = json.load(json_file)["sim_code"]
  
  with open(f_curr_step) as json_file:  
    step = json.load(json_file)["step"]

  os.remove(f_curr_step)

  persona_names = []
  persona_names_set = set()
  for i in find_filenames(f"storage/{sim_code}/personas", ""): 
    x = i.split("/")[-1].strip()
    if x[0] != ".": 
      persona_names += [[x, x.replace(" ", "_")]]
      persona_names_set.add(x)

  persona_init_pos = []
  file_count = []
  for i in find_filenames(f"storage/{sim_code}/environment", ".json"):
    x = i.split("/")[-1].strip()
    if x[0] != ".": 
      file_count += [int(x.split(".")[0])]
  curr_json = f'storage/{sim_code}/environment/{str(max(file_count))}.json'
  with open(curr_json) as json_file:  
    persona_init_pos_dict = json.load(json_file)
    for key, val in persona_init_pos_dict.items(): 
      if key in persona_names_set: 
        persona_init_pos += [[key, val["x"], val["y"]]]

  context = {"sim_code": sim_code,
             "step": step, 
             "persona_names": persona_names,
             "persona_init_pos": persona_init_pos,
             "mode": "simulate"}
  template = "home/home.html"
  return render(request, template, context)


def replay(request, sim_code, step): 
  sim_code = sim_code
  step = int(step)

  persona_names = []
  persona_names_set = set()
  for i in find_filenames(f"storage/{sim_code}/personas", ""): 
    x = i.split("/")[-1].strip()
    if x[0] != ".": 
      persona_names += [[x, x.replace(" ", "_")]]
      persona_names_set.add(x)

  persona_init_pos = []
  file_count = []
  for i in find_filenames(f"storage/{sim_code}/environment", ".json"):
    x = i.split("/")[-1].strip()
    if x[0] != ".": 
      file_count += [int(x.split(".")[0])]
  curr_json = f'storage/{sim_code}/environment/{str(max(file_count))}.json'
  with open(curr_json) as json_file:  
    persona_init_pos_dict = json.load(json_file)
    for key, val in persona_init_pos_dict.items(): 
      if key in persona_names_set: 
        persona_init_pos += [[key, val["x"], val["y"]]]

  context = {"sim_code": sim_code,
             "step": step,
             "persona_names": persona_names,
             "persona_init_pos": persona_init_pos, 
             "mode": "replay"}
  template = "home/home.html"
  return render(request, template, context)


def replay_persona_state(request, sim_code, step, persona_name): 
  sim_code = sim_code
  step = int(step)

  persona_name_underscore = persona_name
  persona_name = " ".join(persona_name.split("_"))
  memory = f"storage/{sim_code}/personas/{persona_name}/bootstrap_memory"
  if not os.path.exists(memory): 
    memory = f"compressed_storage/{sim_code}/personas/{persona_name}/bootstrap_memory"

  with open(memory + "/scratch.json") as json_file:  
    scratch = json.load(json_file)

  with open(memory + "/spatial_memory.json") as json_file:  
    spatial = json.load(json_file)

  with open(memory + "/associative_memory/nodes.json") as json_file:  
    associative = json.load(json_file)

  a_mem_event = []
  a_mem_chat = []
  a_mem_thought = []

  for count in range(len(associative.keys()), 0, -1): 
    node_id = f"node_{str(count)}"
    node_details = associative[node_id]

    if node_details["type"] == "event":
      a_mem_event += [node_details]

    elif node_details["type"] == "chat":
      a_mem_chat += [node_details]

    elif node_details["type"] == "thought":
      a_mem_thought += [node_details]
  
  context = {"sim_code": sim_code,
             "step": step,
             "persona_name": persona_name, 
             "persona_name_underscore": persona_name_underscore, 
             "scratch": scratch,
             "spatial": spatial,
             "a_mem_event": a_mem_event,
             "a_mem_chat": a_mem_chat,
             "a_mem_thought": a_mem_thought}
  template = "persona_state/persona_state.html"
  return render(request, template, context)


def path_tester(request):
  context = {}
  template = "path_tester/path_tester.html"
  return render(request, template, context)


def process_environment(request): 
  """
  <FRONTEND to BACKEND> 
  This sends the frontend visual world information to the backend server. 
  It does this by writing the current environment representation to 
  "storage/environment.json" file. 

  ARGS:
    request: Django request
  RETURNS: 
    HttpResponse: string confirmation message. 
  """
  # f_curr_sim_code = "temp_storage/curr_sim_code.json"
  # with open(f_curr_sim_code) as json_file:  
  #   sim_code = json.load(json_file)["sim_code"]

  data = json.loads(request.body)
  step = data["step"]
  sim_code = data["sim_code"]
  environment = data["environment"]

  with open(f"storage/{sim_code}/environment/{step}.json", "w") as outfile:
    outfile.write(json.dumps(environment, indent=2))

  return HttpResponse("received")


def update_environment(request): 
  """
  <BACKEND to FRONTEND> 
  This sends the backend computation of the persona behavior to the frontend
  visual server. 
  It does this by reading the new movement information from 
  "storage/movement.json" file.

  ARGS:
    request: Django request
  RETURNS: 
    HttpResponse
  """
  # f_curr_sim_code = "temp_storage/curr_sim_code.json"
  # with open(f_curr_sim_code) as json_file:  
  #   sim_code = json.load(json_file)["sim_code"]

  data = json.loads(request.body)
  step = data["step"]
  sim_code = data["sim_code"]

  response_data = {"<step>": -1}
  if (check_if_file_exists(f"storage/{sim_code}/movement/{step}.json")):
    with open(f"storage/{sim_code}/movement/{step}.json") as json_file: 
      response_data = json.load(json_file)
      response_data["<step>"] = step

  return JsonResponse(response_data)


def path_tester_update(request): 
  """
  Processing the path and saving it to path_tester_env.json temp storage for 
  conducting the path tester. 

  ARGS:
    request: Django request
  RETURNS: 
    HttpResponse: string confirmation message. 
  """
  data = json.loads(request.body)
  camera = data["camera"]

  with open(f"temp_storage/path_tester_env.json", "w") as outfile:
    outfile.write(json.dumps(camera, indent=2))

  return HttpResponse("received")

# A partir de aquí, las vistas implementadas por nosotros
def crear_simulacion(request):
  context = {}
  template = "home/crear_simulacion.html"
  return render(request, template, context)

def ver_simulacion(request):
  def obtener_info_demos_disponibles():
    demos_disponibles = dirs_from('compressed_storage')
    
    info_demos = []
    for demo in demos_disponibles:
      simu_f = f"./compressed_storage/{demo}"
      meta_f = f"{simu_f}/meta.json"
      with open(meta_f) as meta_content:
        simu_meta = json.load(meta_content)
        print(simu_meta)
        # Indicar que no hay resumen disponible si no se ha podido generar
        if (not 'summary' in simu_meta.keys() or simu_meta['summary'] == None or not simu_meta['summary']):
          simu_meta['summary'] = "No hay resumen disponible para esta simulación"

        if (simu_meta['fork_sim_code'] == None or not simu_meta['fork_sim_code']):
          simu_meta['fork_sim_code'] = "No disponible"
        
        start_time = datetime.datetime.strptime(simu_meta['start_date'] + ", 00:00:00", '%B %d, %Y, %H:%M:%S')
        curr_time = datetime.datetime.strptime(simu_meta['curr_time'], "%B %d, %Y, %H:%M:%S")
        diff_time = curr_time - start_time

        demo_dict = {"sim_code": demo,
                     "max_step": simu_meta['step'],
                     "sim_code": simu_meta['sim_code'],
                     "fork_sim_code": simu_meta['fork_sim_code'],
                     "start_time": simu_meta['start_date'],
                     "curr_time": simu_meta['curr_time'],
                     "duration": f"{diff_time.days} dias, {diff_time.seconds // 3600} horas, {diff_time.seconds % 3600} segundos",
                     "summary": simu_meta['summary']}
        info_demos.append(demo_dict)
    return info_demos
  
  print("request ver simulación: ", request.GET.dict())
  # Esperamos a que se genere la simulacion que queremos
  time.sleep(2)
  context = {"demos": obtener_info_demos_disponibles()}
  template = "home/ver_simulacion.html"
  return render(request, template, context)

def continuar_simulacion(request):
  def obtener_info_simulaciones_disponibles():
    simulaciones_disponibles = dirs_from('storage')
    
    info_simulaciones = []

    for simu in simulaciones_disponibles:
      simu_f = f"./storage/{simu}"
      meta_f = f"{simu_f}/reverie/meta.json"
      with open(meta_f) as meta_content:
        simu_meta = json.load(meta_content)
        
        start_time = datetime.datetime.strptime(simu_meta['start_date'] + ", 00:00:00", '%B %d, %Y, %H:%M:%S')
        curr_time = datetime.datetime.strptime(simu_meta['curr_time'], "%B %d, %Y, %H:%M:%S")
        diff_time = curr_time - start_time

        simu_dict = {"sim_code": simu,
                     "step": simu_meta['step'],
                     "fork_sim_code": simu_meta['fork_sim_code'],
                     "start_time": simu_meta['start_date'],
                     "curr_time": simu_meta['curr_time'],
                     "duration": f"{diff_time.days} dias, {diff_time.seconds // 3600} horas, {diff_time.seconds % 3600} segundos" }
        info_simulaciones.append(simu_dict)
    return info_simulaciones
  
  context = {"simulaciones": obtener_info_simulaciones_disponibles()}
  template = "home/fork_simulacion.html"
  return render(request, template, context)

def guia_usuario(request):
  context = {}
  template = "home/guia_usuario.html"
  return render(request, template, context)

# A esta función llegan llamadas tanto de crear simulación como de continuar y fork. Se distinguirá por casos y se redirigirá a la vista correspondiente
def simulacion(request):
  sim_code = generar_back(request.POST.dict())
  context = generar_context(sim_code)
  template = "home/home.html"
  return render(request, template, context)

# Manejador de ruta para los botones que gestionan la simulación (play, pause, guardar...)
def manejador_acciones_simulacion(request):
  if request.method == 'POST':
      json_dict = json.load(request)
      action = json_dict['action']
      json_dict = json_dict['values']

      # TODO: Procesar la acción correspondiente
      if action == 'play':
          # ... Lógica del "play" (hacer un run)
          steps = json_dict['steps']
          rc = ReverieComm()
          rc.run(steps)
          pass 
      elif action == 'pause':
          # ... Lógica del "pause"
          pass
      elif action == 'guardar_ver':
          sim_code = json_dict['sim_code']
          # ... Lógica del "guardar_ver"
          rc = ReverieComm()
          rc.sum_up()
          rc.save()
          compress(sim_code)
          rc.finish()
          # Compress -> Emplaza la simulacion comprimida en compressed_storage
      elif action == 'guardar_salir':
          # ... Lógica del "guardar_continuar"
          rc = ReverieComm()
          rc.finish()
          
      elif action == 'salir':
          rc = ReverieComm()
          rc.exit()
          # La eliminacion de este proceso se deberia hacer desde ReverieComm.py

      elif action == 'chat':
          # ... Lógica del "chat" (también se recibirá el id o nombre del personaje con el que se quiere chatear)
          pass
      elif action == 'susurro':
          # ... Lógica del "susurro" (también se recibirá el id o nombre del personaje al que quiere susurrar)
          pass

      return JsonResponse({'success': True})
  else:
      return HttpResponse('Request method must be POST.')

def comenzar_demo_simulacion(request):
  if request.method == 'POST':
    datos = request.POST.dict()
    print("datos de la simulacion", datos)
    sim_code = datos['sim_code']
    step = int(datos['step-select'])
    speed = datos['speed-select']
    return demo(request, sim_code, step, speed)

    # ... Lógica de la redirección

    return redirect('http://localhost:8000/demo/July1_the_ville_isabella_maria_klaus-step-3-20/1/3/')
  else:
    return HttpResponse('Request method must be POST.')
