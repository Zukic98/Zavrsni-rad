# img_viewer.py
import PySimpleGUI as sg
import os.path
from shapely import Polygon
import PlotPolygon
from Model import ModelSample
from shapely.ops import transform
from shapely.affinity import scale

# First the window layout in 2 columns
file_list_column = [
    [sg.Text('HUDDLE PENGUINS\n SIMULATION', enable_events=True,
             key='-TEXT-', font=('Arial Bold', 20),
             expand_x=True, justification='center')],
    [sg.Text('Name of simulation: ', key='-NAME-', font=('Arial ', 10), expand_x=True, justification='left')],
    [sg.Input('', enable_events=True, key='-NAMEINPUT-', font=('Arial Bold', 10), expand_x=True, justification='left')],
    [sg.Text('Number of penguins: ', key='-NUMBER-', font=('Arial ', 10), expand_x=True, justification='left')],
    [sg.Input('', enable_events=True, key='-NUMBERINPUT-', font=('Arial Bold', 10), expand_x=True,
              justification='left')],
    [sg.Text('Peclet\'s number: ', key='-PECLET-', font=('Arial ', 10), expand_x=True, justification='left')],
    [sg.Input('', enable_events=True, key='-PECLETINPUT-', font=('Arial Bold', 10), expand_x=True,
              justification='left')],
    [sg.Text('R: ', key='-R-', font=('Arial ', 10), expand_x=True, justification='left')],
    [sg.Input('', enable_events=True, key='-RINPUT-', font=('Arial Bold', 10), expand_x=True, justification='left')],
    [sg.Button('Set polygon of huddle', key='-SET-', font=('Arial Bold', 10)),
     sg.Button('Run simulation', key='-RUN-', font=('Arial Bold', 10))],

]

# For now will only show the name of the file that was chosen

image_viewer_column = [

    [sg.Text(text='Penguins of Madagascar',
             font=('Arial Bold', 10),
             size=25, expand_x=True,
             justification='center')],
    [sg.Image('ping.png',
              expand_x=True, expand_y=True)]
]
# ----- Full layout -----

layout = [
    [
        sg.Column(file_list_column),
        sg.VSeperator(),
        sg.Column(image_viewer_column),
    ]
]

window = sg.Window("Huddle penguins simulation", layout)

# Run the Event Loop

model = ModelSample()

while True:

    event, values = window.read()

    if event == "Exit" or event == sg.WIN_CLOSED:
        break

    # Folder name was filled in, make a list of files in the folder

    model.name = values["-NAMEINPUT-"]
    model.number = values["-NUMBERINPUT-"]
    model.Peclet = values["-PECLETINPUT-"]
    model.R = values["-RINPUT-"]

    if event == "-SET-":
        model.polygon = transform(lambda x, y: (x, y + 1000) , scale(Polygon(PlotPolygon.DrawPolygon()), yfact = -1, origin = (1, 0))).buffer(10e1,join_style = 2)
    elif event == "-RUN-":
        try:
            model.run()
        except ValueError as v:
            sg.popup(str(v))

window.close()
