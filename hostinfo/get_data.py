import models

def get_all_hostlist():
    return models.HostInfo.objects.all().order_by('IP')

def get_service_name_data():
    return models.Services.objects.only('service_name')
def get_type_data():
    return models.HostInfo.type_choices