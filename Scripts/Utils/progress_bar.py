import time
from tracemalloc import start

#Bar de progrès
def progressBar(total, iterable, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iterable    - Required  : iterable object (Iterable)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    # Progress Bar Printing Function
    def printProgressBar (iteration, timespent):
        percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
        filledLength = int(length * iteration // total)
        bar = fill * filledLength + '-' * (length - filledLength)
        print(f'\r{prefix} |{bar}| {percent}% {suffix} ({iteration}/{total}) - {timespent:.2f}s.', end = printEnd)
    # Initial Call
    printProgressBar(0, 0)
    start_time = time.time()
    # Update Progress Bar
    for i, item in enumerate(iterable):
        yield item
        curr_time = time.time()
        printProgressBar(i + 1, curr_time-start_time)
    
    # Print New Line on Complete
    print()