import PySimpleGUI as sg
import json
from os.path import isfile

# jugadores = {'fede': {'nivel':3,'puntaje':4,'tiempo':200},
#     'belen': {'nivel':4,'puntaje':6,'tiempo':300},
#     'juan': {'nivel':5,'puntaje':7,'tiempo':400}}

jugadores = {'ada':{'Nivel': 7, 'Puntaje': 7, 'Tiempo': 7}}

nombre_archivo = 'jugadores.json'
jug = {}

def datos_jugadores(nombre_archivo):
    if isfile(nombre_archivo):
        return cargar_jugadores(nombre_archivo)
    else:
        sg.Popup('Todavia no hay jugadores cargados', no_titlebar=True)

def guardar_datos(nombre_archivo, jugadores):
    with open(nombre_archivo, 'w') as f:
        json.dump(jugadores,f)

def cargar_jugadores(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        jugadores = json.load(f)
    return jugadores

def actualizar_listado (listbox,lista):
     listbox.Update(map(lambda x: "{} - {} ".format(x[0],x[1]),lista))

def modificoDatos(nombre_archivo):
    try:
        dic = cargar_jugadores(nombre_archivo)
        dic[values['nombre']]={'nivel': int(values['nivel']),'puntaje': int(values['puntaje']), 'tiempo': int(values['tiempo'])}
    except (FileNotFoundError):
        Boton = sg.PopupYesNo('Error','Este archivo no existe, ¿Quiere crearlo?')
        if Boton == 'Yes':
            dic = {}
            dic[values['nombre']]={'nivel': int(values['nivel']),'puntaje': int(values['puntaje']), 'tiempo': int(values['tiempo'])}
            guardar_datos(nombre_archivo,dic)
        else:
            sg.Popup('Error','El archivo '+nombre_archivo+' no existe')


colum = [[sg.Text('Crear jugador: ')],[sg.Text('Nombre: '), sg.Input(key='nombre')],[sg.Text('Nivel: '), sg.Input(key='nivel')],
[sg.Text('Puntaje: '), sg.Input(key='puntaje')],[sg.Text('Tiempo: '),sg.Input(key='tiempo')]]

colum2 = [[sg.Text('Datos del jugador que se seleccione')],[sg.Text('Jugador')],[sg.Listbox(values=list(jug.keys()), key='jugador', size=(20,1))],
[sg.Listbox(values=[], key='Datos', size=(60,10))]]

layout = [
    [sg.Column(colum), sg.Column(colum2)],
    [sg.Button('Añadir'), sg.Button('Mostrar')]
    ]

window = sg.Window('Datos de jugador').Layout(layout).Finalize()
lista = []

while True:
    event,values = window.Read()
    if event is None:
        break
    elif event is 'Añadir':
        modificoDatos(nombre_archivo)
        jug = datos_jugadores(nombre_archivo)
        window.Element('jugador').Update(list(jug.keys()))
    elif event == 'Mostrar':
        if values['jugador'] != []:
            lista.append((values['jugador'][0],jug[values['jugador'][0]]))
            actualizar_listado(window.FindElement('Datos'),lista)
        else:
            sg.Popup('No seleccionaste ningun jugador', no_titlebar=True)

window.Close()
