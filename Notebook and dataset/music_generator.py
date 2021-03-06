import pickle
import torch

from music21 import *
from generator import Generator


device = 'cuda' if torch.cuda.is_available() == True else 'cpu'
PATH = './model/0.01lr_5E_16BS_pokemon.pth'
model = Generator().to(device)
model.load_state_dict(torch.load(PATH, map_location=device))

class MusicGeneratorUtility:
    """A class that wraps the GAN model and offers utilities to generate melodies."""
    def __init__(self):
        #Initializer that initializes GAN model and mappings of notes to int
        self.model = model
        
        with open('mappings.pickle','rb') as file:
            self.mappings = pickle.load(file)
    
    def random_noise(self):
        min = -1
        max = 1
        # torch.rand(batch_size,1 ,vocab_size)
        inputs = (max-min)*torch.rand((2, 1,100)) + min
        return inputs.to(device).float()
    
    def normalize(self, nums, notes):
        # normalize within the range of the length of notes
        result = []
        max_d = torch.topk(nums,1).values
        min_d = torch.topk(nums,1, largest=False).values
        max = len(notes) -1
        min = 0
        for num in nums:
            x = (num-min_d) *(max-min)/(max_d-min_d) + min
            result.append(x)
        return result

    def generate_music(self):
        # convert the predictions into notes
        predictions = self.model(self.random_noise())
        boundary = int(len(self.mappings) / 2)
        pred_nums = [x * boundary + boundary for x in predictions[0][0]]
        pred_nums = torch.Tensor(pred_nums)
        notes = [key for key in self.mappings]
        pred_nums = self.normalize(pred_nums, notes)
        pred_notes = [notes[int(x)] for x in pred_nums]
        return pred_notes

    def save_music(self, filename='music.mp3'):
        """ convert the output from the prediction to notes and create a midi file
        from the notes """
        offset = 0
        midi_stream = stream.Stream()
        prediction_output = self.generate_music()
        # create note and chord objects based on the values generated by the model
        for pattern in prediction_output:
            # rest
            if pattern == 'R':
                midi_stream.append(note.Rest())
            # chord
            elif ('.' in pattern) or pattern.isdigit():
                notes_in_chord = pattern.split('.')
                notes = []
                for current_note in notes_in_chord:
                    new_note = note.Note(current_note)
                    new_note.storedInstrument = instrument.Piano()
                    notes.append(new_note)
                new_chord = chord.Chord(notes)
                new_chord.offset = offset
                midi_stream.append(new_chord)
            # note
            else:
                new_note = note.Note(pattern)
                new_note.offset = offset
                new_note.storedInstrument = instrument.Piano()
                midi_stream.append(new_note)

            # increase offset each iteration so that notes do not stack
            offset += 0.5

        midi_stream.write('midi', filename)

if __name__=='__main__':
    mg = MusicGeneratorUtility()
    mg.save_music('./result/0.01lr_5E_16BS_pokemon.mid')
