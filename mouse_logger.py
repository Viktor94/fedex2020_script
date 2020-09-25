from pynput import mouse
import pynput
import time
import requests


def send_data_to_server(number_of_mouse_acivities):
    API_ENDPOINT = "https://fedex-backend.herokuapp.com/script-management/mu"
    # data to be sent to api

    student_data = {'firstName': 'test', 'lastName': 'user?', 'scriptCode': 'mouse info'}

    request_body = {'buttonsPressed': number_of_mouse_acivities, 'cursorTravelDistance': 'null',
                     'scrollWheelActivity': 'sry','studentDTO': student_data, }

    # data = {'programDTOList':  [{'programName': 'Crysis','usedMemory': 9000}], 'studentDTO': {'firstName': 'string','lastName': 'string','scriptCode': 'string'}}

    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, json=request_body)

    # extracting response text
    pastebin_url = r.text
    print("The pastebin URL is:%s" % pastebin_url)
    print(request_body)

def main():
    while True:
        time_offset = 30
        with mouse.Events() as events:
            counter = 0
            future = time.time() + time_offset
            # Block at most one second
            for event in events:
                if event is pynput.mouse.Events.Click:
                    print('Click!')
                if time.time() < future:
                    counter += 1
                    #print('event happened')
                else:
                    print(counter)
                    send_data_to_server(counter)
                    counter = 0
                    future = time.time() + time_offset
            event = events.get(time_offset)
            if event is None:
                print('nope')



if __name__ == '__main__':
 main()

