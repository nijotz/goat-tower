import os
import sys
sys.path.append(os.path.abspath(os.path.join(__file__, '../..')))
from goattower import engine, init

init()
engine.handle_text(sys.argv[1], ' '.join(sys.argv[2:]))
for text in engine.get_text(sys.argv[1]):
    print text
