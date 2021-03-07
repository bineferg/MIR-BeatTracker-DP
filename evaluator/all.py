# Evaluate all audio
import subprocess
from os import walk
import fileinput
import mir_eval
import matplotlib.pyplot as plt


def calc_score(ref, est):
    reference_beats = mir_eval.io.load_events(ref)
    estimated_beats = mir_eval.io.load_events(est)
    return mir_eval.beat.evaluate(reference_beats, estimated_beats)

annotation_map={}
genre_avg_f_score={}
genre_avg_p_score={}
file_list="../BallroomData/allBallroomFiles"

# Should only be run initially, if not detecting downbeat
def strip_downbeat(files):
    for f in files:
        with fileinput.FileInput(f, inplace = True, backup ='.bak') as f:
            for line in f:
                print(line[:-3])


def make_comp_dict():
    f = open(file_list, 'r')
    lines = f.readlines()
    for line in lines:
        fline=line.strip("./")
        # Get rid of .wav and \n
        refline = fline[:-5]
        fname = refline.split("/")[1]
        annotation_map["../output/"+refline+".estimate"] = "../BallroomAnnotations/"+fname+".beats"


class stat:
    def __init__(self, genre):
        self.genre=genre
        self.pvals=[]
        self.f_measure=[]
        self.cont=[]

    def add_p(self,num):
        self.pvals.append(num)
    def add_f(self, num):
        self.f_measure.append(num)
    def add_c(self, num):
        self.cont.append(num)
    def len_f(self):
        return len(self.f_measure)
    def len_p(self):
        return len(self.pvals)
    def len_c(self):
        return len(self.cont)

jive=stat("Jive")
chacha=stat("ChaChaCha")
quickstep=stat("Quickstep")
tango=stat("Tango")
samba=stat("Samba")
waltz=stat("Waltz")
r_misc=stat("Rumba-Misc")
r_american=stat("Rumba-American")
r_international=stat("Rumba-International")
vien_waltz=stat("VienneseWaltz")


def get_genre(path):
        l_path=path.split("/")
        return l_path[2]

def evaluate_all():
    for est, ref in annotation_map.items():
        score = calc_score(est, ref)
        if get_genre(est) == "Jive":
            jive.add_p(score["P-score"])
            jive.add_f(score["F-measure"])
            jive.add_c(score["Any Metric Level Continuous"])
        if get_genre(est) == "Samba":
            samba.add_p(score["P-score"])
            samba.add_f(score["F-measure"])
            samba.add_c(score["Any Metric Level Continuous"])
        if get_genre(est) == "Waltz":
            waltz.add_p(score["P-score"])
            waltz.add_f(score["F-measure"])
            waltz.add_c(score["Any Metric Level Continuous"])
        if get_genre(est) == "Quickstep":
            quickstep.add_p(score["P-score"])
            quickstep.add_f(score["F-measure"])
            quickstep.add_c(score["Any Metric Level Continuous"])
        if get_genre(est) == "VienneseWaltz":
            vien_waltz.add_p(score["P-score"])
            vien_waltz.add_f(score["F-measure"])
            vien_waltz.add_c(score["Any Metric Level Continuous"])
        if get_genre(est) == "Rumba-Misc":
            r_misc.add_p(score["P-score"])
            r_misc.add_f(score["F-measure"])
            r_misc.add_c(score["Any Metric Level Continuous"])
        if get_genre(est) == "Rumba-American":
            r_american.add_p(score["P-score"])
            r_american.add_f(score["F-measure"])
            r_american.add_c(score["Any Metric Level Continuous"])
        if get_genre(est) == "Rumba-International":
            r_international.add_p(score["P-score"])
            r_international.add_f(score["F-measure"])
            r_international.add_c(score["Any Metric Level Continuous"])
        if get_genre(est) == "Tango":
            tango.add_p(score["P-score"])
            tango.add_f(score["F-measure"])
            tango.add_c(score["Any Metric Level Continuous"])
        if get_genre(est) == "ChaChaCha":
            chacha.add_p(score["P-score"])
            chacha.add_f(score["F-measure"])
            chacha.add_c(score["Any Metric Level Continuous"])


labels = ["Jive", "ChaChaCha", "Tango", "Waltz", "Rumba-International", "Rumba-American","Rumba-Misc","Samba", "Quickstep", "VienneseWaltz"]
def plot_box_f():
    plt.box
    box_plot_data=[jive.f_measure,chacha.f_measure,tango.f_measure,waltz.f_measure,r_international.f_measure,r_american.f_measure, r_misc.f_measure, samba.f_measure, quickstep.f_measure, vien_waltz.f_measure]
    plt.boxplot(box_plot_data, vert=0, patch_artist=True, labels=labels)
    plt.title('F-measure')
    plt.xlabel('Score')
    plt.show(block=True)

def plot_box_p():
    plt.box
    box_plot_data=[jive.pvals,chacha.pvals,tango.pvals,waltz.pvals,r_international.pvals,r_american.pvals, r_misc.pvals, samba.pvals, quickstep.pvals, vien_waltz.pvals]
    plt.boxplot(box_plot_data, vert=0, patch_artist=True, labels=labels)
    plt.title('P-score')
    plt.xlabel('Score')
    plt.show(block=True)

def plot_box_c():
    plt.box
    box_plot_data=[jive.cont,chacha.cont,tango.cont,waltz.cont,r_international.cont,r_american.cont, r_misc.cont, samba.cont, quickstep.cont, vien_waltz.cont]
    plt.boxplot(box_plot_data, vert=0, patch_artist=True, labels=labels)
    plt.title('Continuity')
    plt.xlabel('Score')
    plt.show(block=True)

def print_avgs():
    f_measure = (sum(jive.f_measure) +sum(chacha.f_measure)+sum(waltz.f_measure)+sum(quickstep.f_measure)+sum(vien_waltz.f_measure)+sum(r_misc.f_measure)+sum(r_international.f_measure)+sum(r_american.f_measure)+sum(samba.f_measure)+sum(tango.f_measure))/(jive.len_f()+chacha.len_f()+waltz.len_f()+quickstep.len_f()+vien_waltz.len_f()+r_misc.len_f()+r_international.len_f()+r_american.len_f()+samba.len_f()+tango.len_f())
    print(f_measure)

    pvals = (sum(jive.pvals) +sum(chacha.pvals)+sum(waltz.pvals)+sum(quickstep.pvals)+sum(vien_waltz.pvals)+sum(r_misc.pvals)+sum(r_international.pvals)+sum(r_american.pvals)+sum(samba.pvals)+sum(tango.pvals))/(jive.len_p()+chacha.len_p()+waltz.len_p()+quickstep.len_p()+vien_waltz.len_p()+r_misc.len_p()+r_international.len_p()+r_american.len_p()+samba.len_p()+tango.len_p())
    print(pvals)
    cont = (sum(jive.cont) +sum(chacha.cont)+sum(waltz.cont)+sum(quickstep.cont)+sum(vien_waltz.cont)+sum(r_misc.cont)+sum(r_international.cont)+sum(r_american.cont)+sum(samba.cont)+sum(tango.cont))/(jive.len_c()+chacha.len_c()+waltz.len_c()+quickstep.len_c()+vien_waltz.len_c()+r_misc.len_c()+r_international.len_c()+r_american.len_c()+samba.len_c()+tango.len_c())
    print(cont)
make_comp_dict()
evaluate_all()
#plot_box_c()
print_avgs()
