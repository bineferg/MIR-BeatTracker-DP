"""
Eva Fineberg 2021
ECS7006P Music Informatics
Coursework 1: Beat Tracking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
File: Preporcessing step to compute an onset strength envelope
Inspiration Paper(s) and Resources:
https://www.audiolabs-erlangen.de/resources/MIR/FMP/C6/C6S1_NoveltySpectral.html
"""

import numpy as np
import librosa
import matplotlib.pyplot as plt
import madmom.audio.spectrogram as madspec
import madmom.features.onsets as madset
import madmom.io.audio as madsig
import madmom.audio.stft as madsf


def plot(spec, fname):
    plt.figure()
    plt.plot(spec, 'r--')
    plt.savefig('./plots/' + fname + '.jpg')


def local_average(novelty):
    # Use window size 10
    M_window=10
    N = len(novelty)
    m_avg = np.zeros(N)
    for m in range(N):
        a = max(m - M_window, 0)
        b = min(m + M_window + 1, N)
        m_avg[m] = (1 / (2 * M_window + 1)) * np.sum(novelty[a:b])

    return m_avg

# Find novelty peaks
def enhance_novelties(stft, gamma_factor):
    X = np.log(1 + gamma_factor * np.abs(stft))
    # First order difference
    X_diff = np.diff(X)
    # Take the positive differences and zero out energe drops
    X_diff[X_diff < 0] = 0

    # Sum up the positive differences in a column-wise fashion
    novelty = np.sum(X_diff, axis=0)
    novelty = np.concatenate((novelty, np.array([0.0])))
    return novelty

def calculate_odf(audio_input, hop_size, should_plot):

    # Process the audio file for the sample rate
    sig, sr = librosa.load(audio_input)
    
    # Use 1024 samples for the stft
    frame_N=1024
    # Set gamma factor for logarithmic compression high
    gamma_factor=100
    
    # Calculte the STFT using librosa
    stft = librosa.stft(sig, window='hanning', hop_length=hop_size, win_length=frame_N)
    # Enhance peaks via novelty curve
    novelty_peaks = enhance_novelties(stft, gamma_factor) 
    
    # Further by taking the local avg and zeroing out the rest
    m_avg = local_average(novelty_peaks) 

    # Take the difference from the original novel peaks
    m_avg = novelty_peaks - m_avg
    
    # Zero out all values less than 1 (half-wave correction)
    m_avg[m_avg < 0] = 0.0
    
    # Normalise
    m_avg = m_avg/m_avg.max()
    
    # If the flag is set save the plots
    if should_plot:
        # filename to write peak plot to
        plot_fname = audio_input.split("/")[-1].strip(".wav") 
        plot(m_avg, plot_fname)
    return m_avg, sr
