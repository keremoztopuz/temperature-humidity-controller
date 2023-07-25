def api_getdata(device_id):
    return "api_getdata:" + " " + str(device_id)

def api_setdata(device_id , temperature):
    return "api_setdata:" + str(device_id) + " " + str(temperature)

def api_setdevicelist(setdevlist):
    return "api_setdevicelist:" + " " + str(setdevlist)

