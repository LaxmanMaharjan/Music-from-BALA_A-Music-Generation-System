import os
import jsonpickle

from django.shortcuts import render
from django.views import View

from .music_generator import MusicGeneratorUtility
from midi2audio import FluidSynth
# Create your views here.

class MusicGenerator:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MIDI_PATH = os.path.join(BASE_DIR, 'media/musics/midi/')
    WAV_PATH = os.path.join(BASE_DIR, 'media/musics/wav/')

    def __init__(self):
        self.mg = MusicGeneratorUtility()
    
    def generate_save(self):
        # length is number of files in MIDI_PATH
        length = len(next(os.walk(self.MIDI_PATH))[2])

        music_name_midi = self.MIDI_PATH +f'music{length}.mid'
        music_name_wav = self.WAV_PATH + f'music{length}.wav'

        self.mg.save_music(music_name_midi)
        FluidSynth().midi_to_audio(music_name_midi, music_name_wav)
        print(type(music_name_midi))
        print(music_name_midi)

        #music_list = os.listdir(self.WAV_PATH)
        
        #music_list.reverse()

        music_list = [f'music{length}.wav',f'music{length-1}.wav',f'music{length-2}.wav']
        return music_list

class MusicGeneratorView(View):
    
    def __init__(self):
        self.music = MusicGenerator()

    def get(self, request):
        music_list = self.music.generate_save()         
        #music_list = []
        print(music_list)

        listAudio = []
        for music in music_list:
            
            file_detail = {}
            file_detail['name'] = music
            file_detail['file'] = '/media/musics/wav/'+music
            file_detail['duration'] = '00:50'

            print(file_detail)
            listAudio.append(file_detail)
            print(listAudio)
            
        print(listAudio)
        context = {'listAudio':jsonpickle.encode(listAudio)}

        return render(request, 'music.html',context)

def index(request):
    return render(request, 'index.html')
