from django.apps import AppConfig
from .generator import Generator

import os
import torch
import pickle

class MusicGeneratingAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'music_generating_app'
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODEL_PATH = os.path.join(BASE_DIR, 'GAN_Model/music_generator_gan.pth')
    MAPPING_PATH = os.path.join(BASE_DIR, 'GAN_Model/mappings.pickle')

    with open(MAPPING_PATH,'rb') as file:
        mappings = pickle.load(file)
    model = Generator()
    model.load_state_dict(torch.load(MODEL_PATH, map_location= 'cpu'))

