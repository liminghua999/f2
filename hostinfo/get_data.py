import models

def get_all_hostlist():
    return models.HostInfo.objects.all().order_by('IP')

def get_service_name_data():
    return models.Services.objects.values_list('service_name',flat=True)
def get_type_data():
    return models.HostInfo.type_choices