
import jingo
import json

@jingo.register.filter
def jsonify(obj, *args, **kwargs):
    if not obj:
        return ''
    return json.dumps(obj, *args, **kwargs)
