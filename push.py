from os import system
from platform import system
from win10toast import ToastNotifier
def push(title, message):
    plt = system()
    if plt == "Darwin":
        command = f'''
        osascript -e 'display notification "{message}" with title "{title}"'
        '''
    elif plt == "Linux":
        command = f'''
        notify-send "{title}" "{message}"
        '''
    elif plt == "Windows":
        ToastNotifier().show_toast(title, message)
        return
    else:
        return
    system(command)