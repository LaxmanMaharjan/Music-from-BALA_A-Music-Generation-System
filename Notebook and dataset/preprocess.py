from MIDI import MIDI
import pickle
midi = MIDI(seq_length=100)
datapath = './dataset/PokemonMIDI'    
midi.parser(datapath)
dataset_array = midi.prepare_sequences()

with open('./dataset_pickle/pokemon.pickle','wb') as file:
    pickle.dump(dataset_array, file)

with open('./dataset_pickle/pokemonobj.pickle','wb') as file:
    pickle.dump(midi, file)
