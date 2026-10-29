def get_query_param(request, *names, default=None):
    lower_map = {k.lower(): v for k, v in request.query_params.items()}
    for name in names:
        if name in request.query_params:
            return request.query_params.get(name)
        if name.lower() in lower_map:
            return lower_map[name.lower()]
    return default

