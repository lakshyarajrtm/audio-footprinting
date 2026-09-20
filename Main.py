
from Parser import *
import sys


if __name__ == '__main__':
    filepath = "songs/"
    filepath += sys.argv[1]
    audio = WavParser(filepath)
    print(audio.samples)
    
    
    

    


