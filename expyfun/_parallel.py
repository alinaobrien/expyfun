# -*- coding: utf-8 -*-
"""Parallel util functions
"""

# Adapted from mne-python with permission

import warnings


def parallel_func(func, n_jobs):
    """Return parallel instance with delayed function

    Util function to use joblib only if available

    Parameters
    ----------
    func: callable
        A function
    n_jobs: int
        Number of jobs to run in parallel

    Returns
    -------
    parallel: instance of joblib.Parallel or list
        The parallel object
    my_func: callable
        func if not parallel or delayed(func)
    n_jobs: int
        Number of jobs >= 0
    """
    # for a single job, we don't need joblib
    if n_jobs == 1:
        n_jobs = 1
        my_func = func
        parallel = list
        return parallel, my_func, n_jobs

    try:
        from joblib import Parallel, delayed
    except ImportError:
        try:
            from sklearn.externals.joblib import Parallel, delayed
        except ImportError:
            warnings.warn('joblib not installed. Cannot run in parallel.')
            n_jobs = 1
            my_func = func
            parallel = list
            return parallel, my_func, n_jobs

    # create keyword arguments for Parallel
    n_jobs = _check_n_jobs(n_jobs)
    parallel = Parallel(n_jobs, verbose=0)
    my_func = delayed(func)
    return parallel, my_func, n_jobs


def _check_n_jobs(n_jobs):
    """Check n_jobs in particular for negative values

    Parameters
    ----------
    n_jobs : int
        The number of jobs.

    Returns
    -------
    n_jobs : int
        The checked number of jobs. Always positive.
    """
    if not isinstance(n_jobs, int):
        raise ValueError('n_jobs must be an integer')
    elif n_jobs <= 0:
        try:
            import multiprocessing
            n_cores = multiprocessing.cpu_count()
            n_jobs = min(n_cores + n_jobs + 1, n_cores)
            if n_jobs <= 0:
                raise ValueError('If n_jobs has a negative value it must not '
                                 'be less than the number of CPUs present. '
                                 'You\'ve got %s CPUs' % n_cores)
        except ImportError:
            # only warn if they tried to use something other than 1 job
            if n_jobs != 1:
                warnings.warn('multiprocessing not installed. Cannot run in '
                              'parallel.')
                n_jobs = 1
    return n_jobs
