import os, tkinter, re, ctypes, time, threading
from chat_gpt import request_gpt
from push import push
import platform
import pyperclip

# Настройки
output_file = 'assets/run.py'
enable_auto_save = True
auto_save_delay = 60

# Не трогать
x = 0
y = 0

# код (чуствителен к раскладке клавиатуры)

def copyright():
    '''Bloom Editor Copyright'''
    print('https://github.com/your-github-username/bloom-editor')
    print('Free licence for all!')
    print('Logs')

    pass

def execute(event=None):
    with open(output_file, 'w', encoding='UTF-8') as f:
        f.write(editArea.get('1.0', 'end'))
    
    plt = platform.system()
    if plt == "Linux":
        os.system(f"gnome-terminal -e 'bash -c \"python3 {output_file}; sleep 5\" '")
    elif plt == "Windows":
        os.system(f'start cmd /K "python {output_file}"')
    return event


def changes(event=None):
    global previousText

    if editArea.get('1.0', 'end') == previousText:
        return event

    for tag in editArea.tag_names():
        editArea.tag_remove(tag, '1.0', 'end')

    i = 0
    for pattern, color in repl:
        for start, end in search_re(pattern, editArea.get('1.0', 'end')):
            editArea.tag_add(f'{i}', start, end)
            editArea.tag_config(f'{i}', foreground=color)
            i += 1

    previousText = editArea.get('1.0', 'end')

    return event

def save_file(event=None):
    try:
        text_content = editArea.get('1.0', 'end-1c')
        print("Text successfully fetched from editor.")

        with open(output_file, 'w', encoding='UTF-8') as f:
            f.write(text_content)
        print("Text successfully saved to file.")

        # Выполняем push в отдельном потоке
        threading.Thread(target=push, args=('Bloom Editor', f'Code saved in {output_file}')).start()
        print("Notification sent in separate thread.")

    except Exception as e:
        print(f"Error while saving file: {e}")
        threading.Thread(target=push, args=('Bloom Editor', f"Error saving file: {e}")).start()

    return event


def check_code_on_errors(event=None):
    try:
        answer = request_gpt('Find errors, mistake and return repaired code (without text and only code): ' + editArea.get('1.0', 'end'), 'gpt-3.5-turbo')
        # answer = request_gpt('Find errors, mistake and return repaired code (without text only code): ' + editArea.get('1.0', 'end'), 'gpt-3.5-turbo')
    except Exception as e:
        push('Bloom Editor', f"Error checking code: {e}")
        return event
    else:
        pyperclip.copy(answer)
        push('Bloom Editor', f"Repaired code saved to clipboard!")
        return event

# def copy_code(event=None):
#     # editArea.get('insert', 'end')
#     pyperclip.copy(editArea.selection_get())

# def paste_code(event=None):
#     editArea.insert('insert', pyperclip.paste())

def copy(event=None):
    # The argument to 'args' must be a tuple, so the comma ensures it's treated as such
    threading.Thread(target=pyperclip.copy, args=(editArea.selection_get(),)).start()
    return event

def paste(event=None):
    threading.Thread(target=editArea.insert, args=('insert', pyperclip.paste())).start()
    changes()
    return event

def popup(event=None):
    global x, y
    x = event.x
    y = event.y

    menu.post(event.x_root, event.y_root)
    return event

def search_re(pattern, text):
    matches = []
    text = text.splitlines()

    for i, line in enumerate(text):
        for match in re.finditer(pattern, line):
            matches.append((f'{i + 1}.{match.start()}', f'{i + 1}.{match.end()}'))
    return matches

def rgb(rgb):
    return '#%02x%02x%02x' % rgb


def insert_closing(event):
    """Автозакрытие кавычек и скобок"""
    char = event.char
    pairs = {
        '(': ')',
        '[': ']',
        '{': '}',
        '"': '"',
        "'": "'"
    }
    
    if char in pairs:
        editArea.insert(tkinter.INSERT, pairs[char])
        editArea.mark_set(tkinter.INSERT, f"{editArea.index(tkinter.INSERT)}-1c")
    
    changes(event)
    return event



if platform.system() == "Windows":
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Adjust DPI awareness
    except Exception as e:
        print(f"Failed to set DPI awareness: {e}")


root = tkinter.Tk()
root.geometry('700x500')
root.title('Bloom Editor')
previousText = ''

normal = rgb((234, 234, 234))
keywords = rgb((95, 234, 165))
comments = rgb((234, 95, 95))
string = rgb((234, 162, 95))
function = rgb((95, 211, 234))
background = rgb((42, 42, 42))
font = 'Consolas 15'


repl = [
    ['(^| )(False|True|None|and|as|assert|await|async|break|class|continue|def|del|elif|else|except|finally|for|from|global|if|import|in|is|lambda|nonlocal|not|or|pass|raise|return|try|while|with|yield)($| )', keywords],
    ['".*?"', string],
    ["''", string],
    ['\'[^\']*\'', string],
    ['#.*?$', comments],
    ['print', function],
]

editArea = tkinter.Text(
    root, background=background, foreground=normal, insertbackground=normal, relief='flat', borderwidth=10
)

file_path = tkinter.Entry(
    root, background=background, foreground=normal, insertbackground=normal, relief='flat', borderwidth=10
)

editArea.pack(fill='both', expand=1)
# editArea.pack(fill='top', expand=1)

editArea.bind('<KeyRelease>', changes)
editArea.bind('<KeyPress>', insert_closing)  # Use <KeyPress> instead of <Key>

editArea.bind('<Control-s>', save_file)

# editArea.bind('<Control-c>', copy_code)
# editArea.bind('<Control-v>', paste_code)

editArea.bind('<F6>', check_code_on_errors)


root.bind('<F5>', execute)
root.bind('<Button-3>', popup)

def close(event):
    # root.withdraw() # if you want to bring it back
    exit() # if you want to exit the entire thing

def restart(event):
    # root.withdraw() # if you want to bring it back
    # os.system(os.get_exec_path(os.environ) + 'main.py')

    plt = platform.system()
    if plt == "Linux":
        os.system(f"gnome-terminal -e 'bash -c \"python3 main.py; sleep 5\" '")
    elif plt == "Windows":
        os.system(f'start cmd /K "python main.py"')
    exit() # if you want to exit the entire thing

root.bind('<Escape>', close)
root.bind('<F8>', restart)

menu = tkinter.Menu(tearoff=0)

menu.add_command(label='Копировать', command=copy)
menu.add_command(label='Вставить', command=paste)

if os.path.exists(output_file):
    with open(output_file, 'r', encoding='UTF-8') as f:
        editArea.insert('1.0', f.read())
else:
    with open(output_file, 'w', encoding='UTF-8') as f:
        editArea.insert('1.0', 'print("Hello, World!")')

def auto_save(event=None):
    save_file()
    root.after(auto_save_delay * 1000, auto_save)
    return event

if enable_auto_save:
    root.after(auto_save_delay * 1000, auto_save)

changes()

root.mainloop()