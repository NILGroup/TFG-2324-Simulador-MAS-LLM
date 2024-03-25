# Copy and paste your OpenAI API Key
import os
api_key = os.environ['OPENAI_API_KEY']

maze_assets_loc = "../../environment/frontend_server/static_dirs/assets"
env_matrix = f"{maze_assets_loc}/the_ville/matrix"
env_visuals = f"{maze_assets_loc}/the_ville/visuals"

fs_storage = "../../environment/frontend_server/storage"
fs_temp_storage = "../../environment/frontend_server/temp_storage"

available_personas_folder = f"{maze_assets_loc}/personas"
existing_simulations_folder = f"{fs_storage}"

collision_block_id = "32125"

# Verbose 
if ('debug' in dict(os.environ).keys() and os.environ['debug'] == 'false'):
    debug = False
else:
    debug = True
