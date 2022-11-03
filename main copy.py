import math
from math import sqrt
import PySimpleGUI as sg
from cv2 import destroyAllWindows
import imageio
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib
import imageio.v2 as imageio
from matplotlib.pyplot import figure

gif = sg.DEFAULT_BASE64_LOADING_GIF

matplotlib.use('TkAgg')

def resolvente(A,B,C):
    if ((B**2)-4*A*C) < 0:
        print("La solución de la ecuación es con números complejos")
    else:
        return (-B-sqrt(B**2-(4*A*C)))/(2*A)

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)

class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)

#PySimpleGui
sg.theme('Dark Grey 13')

layout = [
    [sg.Text("Resolvedor para la expo")],
    [sg.Text("Altura inicial:                           "), sg.InputText()],
    [sg.Text("Velocidad inicial:                     "), sg.InputText()],
    [sg.Text("Ángulo respecto a la horizontal:"),sg.InputText()],
    [sg.Button("CALCULAR",pad=(200, 0))],
    [sg.Text("Vox:"),sg.Text(key="k_vox")],
    [sg.Text("Voy:"),sg.Text(key="k_voy")],
    [sg.Text("Tiempo Ymax:"),sg.Text(key="k_TYmax")],
    [sg.Text("Ymax:"),sg.Text(key="k_Ymax")],
    [sg.Text("Tiempo Xmax:"),sg.Text(key="k_TXmax")],
    [sg.Text("Xmax:"),sg.Text(key="k_Xmax")],
    [sg.Canvas(key="controls_cv")],
    [sg.Canvas(key='canvas', size=(600, 700)), sg.Image(data=sg.DEFAULT_BASE64_LOADING_GIF, key='-GIF-')]
     ]

window = sg.Window("Resolvedor para la expo - rocopolas", layout,size=(1300,850))

 

#------------

g = 9.81

while True:
    event, values = window.read(timeout=100)

    if event == "CALCULAR":
        try:
            altura = float(values[0])
            Vo = float(values[1])
            grados = float(values[2])
        except:
            sg.Popup("Datos mal ingresados", keep_on_top=True)
            altura = 0
            Vo = 0
            grados = 0
        
        plt.cla()
        Voy = Vo * math.sin(math.radians(grados))
        Vox = Vo * math.cos(math.radians(grados))
        T_Ymax = Voy/g
        Ymax = altura + Voy * T_Ymax - 4.905 * T_Ymax

        T_Xmax = resolvente(-4.905,Voy,altura)
        Xmax = Vox * T_Xmax

        window["k_vox"].update(f"{Vox}m/s")
        window["k_voy"].update(f"{Voy}m/s")
        window["k_TYmax"].update(f"{T_Ymax}s")
        window["k_Ymax"].update(f"{Ymax}m")
        window["k_TXmax"].update(f"{T_Xmax}s")
        window["k_Xmax"].update(f"{Xmax}m")

        x = [Vox * 0]
        y = [altura + (Voy * 0) - ((0.5*g)*(0**2))*2]
        t = 1   #lo q me costo hacer esta mierda de graficar el tiro parabolico no tiene sentido, chupenme la pija tutoriales de youtube lo hice con mi 🧠🧠🧠
        filenames = []
        while y[-1] > -1:
            y.append((altura + (Voy * t) - ((0.5*g)*(t**2)))*2)
            x.append(Vox * t)
            t += 1
            nombres = f"gifs/{t}.png"

            plt.plot(x,y,'ro')
            plt.ylabel("y (m)")
            plt.xlabel("x (m)")

            filenames.append(nombres)
            plt.savefig(nombres)
            plt.cla()

        gif = f"gif {T_Xmax} {T_Ymax}.gif"
        with imageio.get_writer(gif, mode='I') as writer:
            for nombres in filenames:
                image = imageio.imread(nombres)
                writer.append_data(image)
        
        plt.plot(x,y,'b')
        plt.ylabel("y (m)")
        plt.xlabel("x (m)")
        
        fig = plt.gcf() 
        draw_figure_w_toolbar(window['canvas'].TKCanvas, fig, window['controls_cv'].TKCanvas)

    if event == sg.WIN_CLOSED:
        break
    elif event == sg.TIMEOUT_EVENT:
        window['-GIF-'].update_animation(gif, time_between_frames=100)

window.close()