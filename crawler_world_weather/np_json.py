import numpy, json, math
import pandas as pd

class NumpyEncoder(json.JSONEncoder):
    def __init__(self, *args, **kwargs):
        if('allow_nan' not in kwargs):
            kwargs['allow_nan'] = False
        return super(NumpyEncoder, self).__init__(*args, **kwargs)

    def default(self, obj):
        if obj != obj:
            return None
        if isinstance(obj, pd.Timestamp):
            return obj.strftime('%F %T')
        elif isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            if obj != obj:
                return None
            if not numpy.isfinite(obj):
                return None
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(NumpyEncoder, self).default(obj)
