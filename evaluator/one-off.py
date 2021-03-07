import mir_eval
import argparse
import sys
import getopt

def calc_score(ref, est):
    return mir_eval.beat.evalutate(ref, est)

def beat_performance(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--Estimate", help = "Estimated beat file")
    parser.add_argument("-t", "--Truth", help = "Ground truth beat file")
    
    args = parser.parse_args()

    if args.Estimate is None:
        sys.exit("Please enter an estimate file")
    if args.Truth is None:
        sys.exit("Please specify an estimate beat file")
    reference_beats = mir_eval.io.load_events(args.Estimate)
    estimated_beats = mir_eval.io.load_events(args.Truth)
    scores = calc_score(ref,est)
    print(scores)

beat_performance(sys.argv[1:])
