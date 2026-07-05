import time
from functools import wraps

def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        response = func(*args, **kwargs)
        end_time = time.time()
        
        if isinstance(response, tuple):
            res_data, status = response
            if status == 200:
                data = res_data.get_json()
                data['time_ms'] = round((end_time - start_time) * 1000, 2)
                response = (res_data.app.response_class(
                    response=res_data.app.json.dumps(data),
                    status=200,
                    mimetype='application/json'
                ), status)
        return response
    return wrapper