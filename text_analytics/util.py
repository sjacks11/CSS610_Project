import datetime

def get_bucket_name(basename=None) :
    """gets the bucket path based on the current date for data storage
        (date_level, time_level) - time_level is closest half-hour interval
    """
    d=datetime.datetime.now()

    timestr=[]
    timestr.append(lz(d.year))
    timestr.append(lz(d.month))
    timestr.append(lz(d.day))
    l1=''.join(timestr)

    timestr=[]
    timestr.append(lz(d.hour))
    timestr.append(lz(d.minute))
    timestr.append(lz(d.second))
    l2=''.join(timestr)

    return basename+'_' + l1 + '_' + l2 + '.csv'

def lz(nr=-1) :
    return ('0' if nr<9 else '') + str(nr)