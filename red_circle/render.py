from p5 import *
import sounddevice # for microphone
import mido # for midi
import threading # for system
import numpy as np
import sounddevice as sd

# Global variables
x_pos = 0
y_pos = 0
x_size = 0
y_size = 0

transparency = 255  # opacity

move_pos = 5

midi_port = None
midi_in = None
audio_stream = None

############################################################################################
# Set up for p5
def setup():
    global x_pos, y_pos, x_size, y_size, midi_in, audio_stream
    size(400, 400)  # initial starting size
    background(255)

    # inital size
    x_pos = width / 2
    y_pos = height / 2
    x_size = width / 4
    y_size = width / 4

    # Open MIDI port
    global midi_port
    midi_port = 'nanoPAD2 PAD' # device name
    midi_in = mido.open_input(midi_port)

    # Start a thread for MIDI input
    midi_thread = threading.Thread(target=midi_listener)
    midi_thread.daemon = True  # This allows the thread to exit when the main program exits
    midi_thread.start()

    # Set up audio stream
    audio_thread = threading.Thread(target=audio_listener)
    audio_thread.daemon = True
    audio_thread.start()

# p5 will continously loop through this
def draw():
    global x_pos, y_pos, x_size, y_size, transparency
    background(255)  # Clear the background each frame

    # Draw the red ellipse at the current position
    fill(255, 0, 0, transparency)
    ellipse((x_pos, y_pos), x_size, y_size)
############################################################################################

# Used to listen to midi port for mido
def midi_listener():
    global x_pos, y_pos, x_size, y_size, move_pos
    note_states = {}  # Dictionary to track the state of each note

    # Hold midi to take effect
    while True:
        for msg in midi_in.iter_pending():
            if msg.type == 'note_on':
                # Update note state to 'on'
                note_states[msg.note] = True
            elif msg.type == 'note_off':
                # Update note state to 'off'
                note_states[msg.note] = False
                if msg.note in note_states:
                    del note_states[msg.note]

        # Apply movement based on current note states
        if 36 in note_states and note_states[36]:
            x_pos -= move_pos  # Move circle left
        if 40 in note_states and note_states[40]:
            x_pos += move_pos  # Move circle right
        if 39 in note_states and note_states[39]:
            y_pos -= move_pos  # Move circle up
        if 38 in note_states and note_states[38]:
            y_pos += move_pos  # Move circle down
        if 37 in note_states and note_states[37]:
            x_size -= move_pos  # Make circle smaller
            y_size -= move_pos
        if 41 in note_states and note_states[41]:
            x_size += move_pos  # Make circle bigger
            y_size += move_pos
        if 51 in note_states and note_states[51]:
            reset_position()  # Reset circle position

        # Sleep to avoid high CPU usage
        time.sleep(0.01)

# Reset circle position
def reset_position():
    global x_pos, y_pos
    x_pos = width / 2
    y_pos = height / 2

# Used to listen to microphone
def audio_listener():
    # less crackling noise the closer the volume is to device's internal setting
    with sd.Stream(callback=microphone_volume, samplerate=44100, channels=1, blocksize=1024):
        while True:
            sd.sleep(0)  # Keep the stream running

# Record microphone volume and assign transparency 
def microphone_volume(indata, outdata, frames, time, status):
    global transparency
    volume_norm = np.linalg.norm(indata)*100 # * 100 to get color with microphone lvel
    transparency = int(np.clip(volume_norm, 0, 255)) 


if __name__ == '__main__':
    run()