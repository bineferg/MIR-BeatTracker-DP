"""
Eva Fineberg 2021
ECS7006P Music Informatics
Coursework 1: Beat Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
File: Entry point for the beat tracker
Command: beats = beatTracker(path_to_audio_file)

Inspiration Paper(s) and Resources:
https://www.ee.columbia.edu/~dpwe/pubs/Ellis07-beattrack.pdf
"""

import os.path
import sys
import librosa
import processor.beats as proc
import processor.preprocess as prec

# set hop_size to half the window length for stft
hop_size=512

def beatTracker(audio_input):
    pFlag=False
    if not os.path.isfile(audio_input):
        sys.exit("Audio file not found!")

    # Calculate ODF According to Audio Labs Erlangen
    # Can update should_plot to produce/save figures
    odf, sr = prec.calculate_odf(audio_input, hop_size, should_plot=False)
    
    # Estimate tempo (Default using librosa) in bpm  
    tempo_bpm = librosa.beat.tempo(onset_envelope=odf, sr=sr)
    
    # Convert tempo to samples per beat
    tempo_fpb = (60 * (sr/hop_size)) / tempo_bpm
    beats = proc.find_beats(odf, tempo_fpb, sr)
    print(beats)
    return beats
    
