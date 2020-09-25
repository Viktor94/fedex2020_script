import psutil
import time
import requests


def getListOfProcessSortedByMemory():
    '''
    Get list of running process sorted by Memory Usage
    '''
    list_of_proc_objects = []
    # Iterate over the list
    for proc in psutil.process_iter():
        try:
            # Fetch process details as dict
            pinfo = proc.as_dict(attrs=['name'])
            pinfo['memory'] = int(proc.memory_info().rss / (1024 * 1024))
            # Append dict to list
            list_of_proc_objects.append(pinfo)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    # Sort list of dict by key vms i.e. memory usage
    list_of_proc_objects = sorted(list_of_proc_objects, key=lambda procObj: procObj['memory'], reverse=True)
    return list_of_proc_objects


def getListOfPrecessesSortedByProcessorUsage():
    # Get list of running processes sorted by CPU usage
    list_of_process_objects = []
    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=['name'])
            process_info['cpuUsage'] = process.cpu_percent(0.1)
            # Append dict to list
            list_of_process_objects.append(process_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

        return sorted(list_of_process_objects, key=lambda proc_obj: proc_obj['cpuUsage'], reverse=True)


def send_data_to_server(list_of_memory_consumers, list_of_cpu_consumers):
    API_ENDPOINT = "https://fedex-backend.herokuapp.com/script-management/scripts"
    # data to be sent to api

    student_data = {'firstName': 'mi fasz van', 'lastName': 'megint?', 'scriptCode': 'picsaba mar!'}

    request_body = {'cpuUsageDTO': list_of_cpu_consumers, 'programDTOList': list_of_memory_consumers,
                    'studentDTO': student_data}

    # data = {'programDTOList':  [{'programName': 'Crysis','usedMemory': 9000}], 'studentDTO': {'firstName': 'string','lastName': 'string','scriptCode': 'string'}}

    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, json=request_body)

    # extracting response text
    pastebin_url = r.text
    #print("The pastebin URL is:%s" % pastebin_url)
    #print(request_body)



def main():
    while True:
        # get top memory consumers
        number_of_highest_memory_consumers = 10
        processor_using_apps = getListOfProcessSortedByMemory()

        # get top CPU consumers
        number_of_highest_cpu_consumers = 10
        memory_using_apps = getListOfPrecessesSortedByProcessorUsage()

        send_data_to_server(processor_using_apps[:number_of_highest_memory_consumers],
                            memory_using_apps[:number_of_highest_cpu_consumers])
        time.sleep(25)


if __name__ == '__main__':
    main()
