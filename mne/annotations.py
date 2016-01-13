# Authors: Jaakko Leppakangas <jaeilepp@student.jyu.fi>
#
# License: BSD (3-clause)

import numpy as np
from datetime import datetime
import time


class Annotations(object):
    """Annotation object for annotating segments of raw data.

    Parameters
    ----------
    onset: array of float
        Annotation time onsets from the beginning of the recording.
    duration: array of float
        Durations of the annotations.
    description: array of str
        Array of strings containing description for each annotation.
    orig_time: int | instance of datetime | None
        Timestamp or a datetime determining the starting time of annotation
        acquisition. If None (default), starting time is determined from
        beginning of raw data.
    """

    def __init__(self, onset, duration, description, orig_time=None):

        if orig_time is not None:
            if isinstance(orig_time, datetime):
                orig_time = time.mktime(orig_time.timetuple())
            elif not np.isscalar(orig_time):
                orig_time = orig_time[0]
        self.orig_time = orig_time

        onset = np.array(onset)
        if len(onset.shape) != 1:
            raise RuntimeError('Onset must be a one dimensional array.')
        duration = np.array(duration)
        if len(duration.shape) != 1:
            raise RuntimeError('Duration must be a one dimensional array.')
        if not (len(onset) == len(duration) == len(description)):
            raise RuntimeError('Onset, duration and description must be '
                               'equal in sizes.')
        # sort the segments by start time
        order = onset.argsort(axis=0)
        self.onset = onset[order]
        self.duration = duration[order]
        self.description = np.array(description)[order]
