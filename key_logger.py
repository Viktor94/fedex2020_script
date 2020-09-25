from pynput import keyboard
import time
import requests

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(key))

def on_release(key):
    print('{0} released'.format(key))

def send_data_to_server(number_of_keyboard_acivities):
    API_ENDPOINT = "https://fedex-backend.herokuapp.com/script-management/kppm"
    # data to be sent to api

    student_data = {'firstName': 'test', 'lastName': 'user?', 'scriptCode': 'keyboard info'}

    request_body = {'keypressed': number_of_keyboard_acivities, 'studentDTO': student_data, }

    # sending post request and saving response as response object
    r = requests.post(url=API_ENDPOINT, json=request_body)

    # extracting response text
    pastebin_url = r.text
    print("The pastebin URL is:%s" % pastebin_url)
    print(request_body)


def main():
    while True:
        time_offset = 30
        with keyboard.Events() as events:
            counter = 0
            future = time.time() + time_offset
            # Block at most one second
            for event in events:
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

