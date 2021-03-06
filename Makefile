#
# Makefile for beat tracker
#

# Can be set on the cmdline if you just want to test 1 file
AUDIO_FILE ?= './BallroomData/ChaChaCha/Albums-I_Like_It2-01.wav'
BEAT_ESTIMATE ?= "estimates.txt"
BEAT_GROUND_TRUTH ?= "truth.txt"

track-beat: data-check beat-tracker

data-check:
	if [ ! -d ./BallroomData ] ; then curl http://mtg.upf.edu/ismir2004/contest/tempoContest/data1.tar.gz --output ./data1.tar.gz; tar -xf data1.tar.gz; fi 

beat-tracker:
	python3 -c "from beat_tracker import beatTracker;beatTracker($(AUDIO_FILE))"

track-all: data-check beat-tracker-all
	
beat-tracker-all:
	python3 run-all.py

play:
	ffplay $(AUDIO_FILE)

eval-one:
	python3 evaluator/one-off.py -e $(BEAT_ESTIMATE) -t $(BEAT_GROUND_TRUTH)

eval-all:
	python3 evaluator/all.py

clean-all: clean-plots

clean-plots:
	rm -rf ./plots

.PHONY: track-beat play eval-one clean-all clean-plots
