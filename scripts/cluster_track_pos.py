#Get cluster size distribution from gsd file

from SAASH import analyze
from SAASH.util import observer as obs
import sys

def setup_observer(gsd_file, run_type, observables = None, jump=1):

    #init an observables with the file and run type
    observer = obs.Observer(gsd_file, run_type, jump = jump)
    observer.set_focus_list([12]) #get capsid bond info
    observer.set_ngrid_cutoff(2.2)

    if observables is not None:
        for observable in observables:
            observer.add_observable(observable)

    return observer


if __name__ == "__main__":

    #get command line args for gsd_file, ixn_file, and number of frames to jump
    try:
        gsd_file = sys.argv[1]
        ixn_file = sys.argv[2]
        jump     = int(sys.argv[3])
    except:
        print("Usage: %s <gsd_file> <ixn_file> <frame_skip>" % sys.argv[0])
        raise

    #do a bulk analysis run - tracks number of clusters of each size every jump frames
    observables = ['num_bodies','bonds','positions']
    observer = setup_observer(gsd_file, 'cluster', jump=jump,observables=observables)
    analyze.run_analysis(gsd_file, ixn_file=ixn_file, observer=observer)

