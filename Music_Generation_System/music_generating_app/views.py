import os

from django.shortcuts import render
from django.views import View

from .music_generator import MusicGeneratorUtility
# Create your views here.

class MusicGeneratorView(View):
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PATH = os.path.join(BASE_DIR, 'Musics/')
     
    def __init__(self):
        self.mg = MusicGeneratorUtility()

    def get(self, request):
        music_name = self.PATH +'first.mp3'
        self.mg.save_music(music_name)
        return render(request, 'index.html')
