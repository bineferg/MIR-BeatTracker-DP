"""
Eva Fineberg 2021
ECS7006P Music Informatics
Coursework 1: Beat Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
File: Beat tracking implimentation of Dan Ellis (2007) 
using Dynamic Programming

Inspiration Paper(s) and Resources:
https://www.ee.columbia.edu/~dpwe/pubs/Ellis07-beattrack.pdf
https://www.audiolabs-erlangen.de/resources/MIR/FMP/C6/C6S3_BeatTracking.html
"""

import numpy as np
import librosa

def peanalise(N, beat_ref):
    t = np.arange(1, N) / beat_ref
    penalty = -np.square(np.log2(t))
    t = np.concatenate((np.array([0]), t))
    penalty = np.concatenate((np.array([0]), penalty))
    return penalty

def forward_calc(N, max_data, acc_score, penalty, onset_func):
    for n in range(2, N+1):
        m_indices = np.arange(1,n)
        scores = acc_score[m_indices] + penalty[n-m_indices]
        maximum = np.max(scores)
        if maximum <= 0:
            acc_score[n] = onset_func[n]
            max_data[n] = 0
        else:
            acc_score[n] = onset_func[n] + maximum
            max_data[n] = np.argmax(scores) + 1
    return max_data, acc_score 

def backwards_calc(N, acc_score, max_data):
    frame_beat_seq = np.zeros(N, dtype=int)
    idx = 0
    frame_beat_seq[idx] = np.argmax(acc_score)
    while(max_data[frame_beat_seq[idx]]!=0 ):
        idx = idx+1
        frame_beat_seq[idx] = max_data[frame_beat_seq[idx-1]]
        
    frame_beat_seq = frame_beat_seq[0:idx+1]
    frame_beat_seq = frame_beat_seq[::-1]
    frame_beat_seq = frame_beat_seq - 1
    return frame_beat_seq

# Entry point for Ellis (2007) dynamic programming approach
def find_beats(novelty, tempo_f, sr):
    
    N = len(novelty)
    
    # Get penalty/confidence function
    penalty = peanalise(N, tempo_f)
    
    # Create onset_func vector of same size
    onset_func = np.concatenate((np.array([0]), novelty))
    
    # Initialise accumulative score vector 
    acc_score = np.zeros(N+1)

    # Initalise running maximisation data vector 
    max_data = np.zeros(N+1, dtype=int) 
    
    # Set the first score to be the first value of the onset_func
    acc_score[1] = onset_func[1]
    
    # Set the first maximisation point to 0
    max_data[1] = 0  
    
    # Calculate forward
    max_data, acc_score = forward_calc(N, max_data, acc_score, penalty, onset_func)

    # Calculate backwards
    beats_by_frames = backwards_calc(N, acc_score, max_data)
    
    # Return the beat sequence list in terms of time not frames via librosa
    return librosa.frames_to_time(beats_by_frames, sr=sr)
