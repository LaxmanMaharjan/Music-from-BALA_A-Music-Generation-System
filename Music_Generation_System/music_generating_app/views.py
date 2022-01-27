import os

from django.shortcuts import render
from django.views import View

from .music_generator import MusicGeneratorUtility
from midi2audio import FluidSynth
# Create your views here.

class MusicGeneratorView(View):
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PATH = os.path.join(BASE_DIR, 'media/musics/')
     
    def __init__(self):
        self.mg = MusicGeneratorUtility()

    def get(self, request):
        music_name_midi = self.PATH +'music.mid'
        music_name_wav = self.PATH + 'music.wav'
        self.mg.save_music(music_name_midi)
        FluidSynth().midi_to_audio(music_name_midi, music_name_wav)
        print(type(music_name_midi))
        print(music_name_midi)
        return render(request, 'music.html',{'path':str(music_name_midi)})

def index(request):
    return render(request, 'index.html')
