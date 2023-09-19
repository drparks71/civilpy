import PySimpleGUI as sg
from pathlib import Path
from io import BytesIO
from PIL import Image

test_init = True


def update_listbox(listbox_element, folder, extension, substring):
    path = Path(folder)
    filter_ = substring.lower()
    lst = []
    if folder != '' and path.is_dir():
        files = list(path.glob("*.*"))
        lst = [file for file in files if file.suffix.lower() in extension
               and filter_ in str(file).lower() and file.is_file()]
    listbox_element.update(lst)


def update_image(image_element, filename):
    im = Image.open(filename)
    w, h = size_of_image
    scale = max(im.width / w, im.height / h)
    if scale <= 1:
        image_element.update(filename=filename)
    else:
        im = im.resize((int(im.width / scale), int(im.height / scale)),
                       resample=Image.CUBIC)
        with BytesIO() as output:
            im.save(output, format="PNG")
            data = output.getvalue()
        image_element.update(data=data)


sg.theme('Dark')
sg.set_options(font=('Courier New', 11))

w, h = size_of_image = (700, 600)

layout_top = [
    [sg.InputText(enable_events=True, key='-FOLDER-'),
     sg.FolderBrowse('Browse', size=(7, 1), enable_events=True)],
    [sg.InputText(enable_events=True, key='-FILTER-'),
     sg.Button('Search', size=(7, 1))],
]
layout_bottom = [
    [sg.Listbox([], size=(52, 30), enable_events=True,
                select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, key='-LISTBOX-')],
]
layout_left = [
    [sg.Column(layout_top, pad=(0, 0))],
    [sg.Column(layout_bottom, pad=(0, 0))],
]
layout_right = [[sg.Image(background_color='green', key='-IMAGE-')]]
layout = [
    [sg.Column(layout_left), sg.Column(layout_right, pad=(0, 0),
                                       size=(w + 15, h + 15), background_color='blue', key='-COLUMN-')],
]

window = sg.Window("Plan Viewer", layout, finalize=True)
window['-IMAGE-'].Widget.pack(fill='both', expand=True)
window['-IMAGE-'].Widget.master.pack(fill='both', expand=True)
window['-IMAGE-'].Widget.master.master.pack(fill='both', expand=True)
window['-COLUMN-'].Widget.pack_propagate(False)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    # print(event, values)
    if event in ('-FOLDER-', '-FILTER-', 'Search'):
        update_listbox(window['-LISTBOX-'], values['-FOLDER-'],
                       ('.png', '.gif', '.jpg', '.tif'), values['-FILTER-'])
    elif event == '-LISTBOX-':
        lst = values['-LISTBOX-']
        if lst:
            update_image(window['-IMAGE-'], values['-LISTBOX-'][0])

window.close()
