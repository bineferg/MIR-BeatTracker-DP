# Beat Tracking

Coursework 1 : Music Informatics (2021) Queen Mary University of London

Dynamic Programming implementation and evaluation of Dan Ellis (2007) Beat Tracking algorithm [[1]](https://www.ee.columbia.edu/~dpwe/pubs/Ellis07-beattrack.pdf).

## Requirements
* python3
* librosa
* mir_eval

## Runing 

To run the program against a single file:
```
$ make track-beat AUDIO_FILE=<path-to-audio-file>
```
The program is also callable from a python environment as follows:
```
beats = beatTracker(<path-to-audio-file>)
```

To run the program against the entire Ballroom dataset:
```
make track-all
```

## Evaluation

To evaluate a single run you must have your estimates and your ground truth sequences in local files and the evaluator can be evoked by running:

```
$ make eval-one BEAT_ESTIMATE=<path-to-estimate-sequence> BEAT_GROUND_TRUTH=<path-to-ground-truth>   
```

To evaluate all outputs in the given dataset and produce relevant box plots:

```
$ make eval-all
```

## References
[[1]](https://www.audiolabs-erlangen.de/resources/MIR/FMP/C6/C6S3_BeatTracking.html)[[2]](https://www.audiolabs-erlangen.de/resources/MIR/FMP/C6/C6S1_NoveltySpectral.html)[[3]](https://www.ee.columbia.edu/~dpwe/pubs/Ellis07-beattrack.pdf)
