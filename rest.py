import json
import os
import random
import time

import playsound
from psychopy import clock, core, event, logging, prefs, sound, visual

# ERROR, WARNING, DATA, EXP, INFO and DEBUG
# logging.console.setLevel(logging.EXP)
logging.console.setLevel(logging.DATA)

from psychopy_experiment_helpers.experiment_info import (
    display_eeg_info,
    get_participant_info,
)
from psychopy_experiment_helpers.save_data import DataSaver
from psychopy_experiment_helpers.screen import create_win

display_eeg_info()
participant_info, experiment_version = get_participant_info(False)

blocks = ["open", "open", "open", "open", "closed", "closed", "closed", "closed"]
random.shuffle(blocks)
for i in range(len(blocks) - 1):
    b1 = blocks[i]
    b2 = blocks[i + 1]
    if b1[-4:] == b2[-4:]:
        blocks[i + 1] = "keep_" + b2
print(blocks)

# save blocks
dir_name = os.path.join("results", "rest")
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
filename = os.path.join("results", "rest", participant_info + ".json")
with open(filename, "w") as f:
    json.dump(blocks, f, indent=4)


win, screen_res = create_win(
    screen_color="black",
    screen_number=-1,
)

fixation = visual.TextStim(
    win=win,
    text="+",
    color="white",
    height=0.087,
    name="fixation",
)

fixation.draw()
win.flip()


block_time = 60
start_time = time.time()
for i, block in enumerate(blocks):
    sound_file = os.path.join("messages", f"{block}.wav")
    playsound.playsound(sound_file, block=True)

    block_end = start_time + block_time * (i + 1)
    time.sleep(block_end - time.time())

msg = visual.TextStim(
    text="Koniec.\nZaczekaj na eksperymentatora.\n\n(Naciśnij spację, aby wyjść.)",
    win=win,
    antialias=True,
    font="Arial",
    height=0.087,
    # wrapWidth=screen_width,
    color="white",
    alignText="center",
    pos=(0, 0),
)
msg.draw()
win.flip()

sound_file = os.path.join("messages", f"end.wav")
playsound.playsound(sound_file, block=True)

event.waitKeys(keyList=["f7", "return", "space"])

# play it with psychopy
# sound = sound.Sound(sound_file)
# sound.play()

# core.wait(3)

# from pprint import pprint
# import psychtoolbox.audio
# pprint(psychtoolbox.audio.get_devices())
# set  prefs.hardware[‘audioDevice’]
# to 0
# prefs.hardware["audioDevice"] = "HDA Intel PCH: ALC285 Analog (hw:0,0)"
# prefs.hardware["audioLib"] = "sounddevice"
# prefs.hardware["audioLatencyMode"] = 0
# print(prefs.hardware["audioDevice"])
