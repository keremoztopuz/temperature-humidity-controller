def api_getdata(device_id):
    return "api_getdata:" + " " + str(device_id)

def api_setdata(device_id , temperature):
    return "api_setdata:" + str(device_id) + " " + str(temperature)

def api_getdevicelist(getdevlist):
    return "api_getdevicelist:" + " " + str(getdevlist)

def api_setdevicename(device_id , name):
    return "api_setdevicename:" + " " + str(device_id) + " " + name

def api_getgraph(device_id):
    return "api_getgraph:" + " " + str(device_id)

def api_getgraphfull(device_id, start_date, end_date):
    return "api_getgraphfull:" + " " + str(device_id) + " " + str(start_date) + " " + str(end_date)