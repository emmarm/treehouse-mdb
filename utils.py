def return_error_or_data(res):
    json = res.json()
    error = ''
    if res.status_code != 200:
        error = json['errors'][0] if 'errors' in json else json['status_message']
    if error:
        return (error, None)
    return (None, json)
