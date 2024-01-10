#Aquí importo todas las librerías necesarias para hacer todos los cálculos necesarios
import PySimpleGUI as sg
import math
from statistics import mode, median, variance, pvariance
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



#Defino la interfaz de la calculadora de operaciones básicas
calculator_layout = [ 
    [sg.Input(size=(20, 1), key='DISPLAY', justification="right")],
    [sg.Button("rad", size=(4, 2), button_color=('black', 'green')), sg.Button("sin", size=(4, 2), button_color=('black', 'green')),
     sg.Button("cos", size=(4, 2), button_color=('black', 'green')), sg.Button("tan", size=(4, 2), button_color=('black', 'green'))],
    [sg.Button("log", size=(4, 2), button_color=('black', 'blue')), sg.Button("ln", size=(4, 2), button_color=('black', 'blue')),
     sg.Button("(", size=(4, 2), button_color=('black', 'blue')), sg.Button(")", size=(4, 2), button_color=('black', 'blue'))],
    [sg.Button("AC", size=(4, 2), button_color=('black', 'red')), sg.Button("√", size=(4, 2), button_color=('black', 'red')),
     sg.Button("^", size=(4, 2), button_color=('black', 'red')), sg.Button("/", size=(4, 2), button_color=('black', 'red'))],
    [sg.Button("1", size=(4, 2)), sg.Button("2", size=(4, 2)), sg.Button("3", size=(4, 2)), sg.Button("*", size=(4, 2))],
    [sg.Button("4", size=(4, 2)), sg.Button("5", size=(4, 2)), sg.Button("6", size=(4, 2)), sg.Button("-", size=(4, 2))],
    [sg.Button("7", size=(4, 2)), sg.Button("8", size=(4, 2)), sg.Button("9", size=(4, 2)), sg.Button("+", size=(4, 2))],
    [sg.Button("π", size=(4, 2)), sg.Button("0", size=(4, 2)), sg.Button(".", size=(4, 2)), sg.Button("=", size=(4, 2), button_color=('black', 'orange'))],
]
#Defino la interfaz de la calculadora de datos estadísticos a través de un archivo excel
statistics_layout = [
    [sg.Text('Data Analytics', font=('Helvetica', 15))],
    [sg.Text('Select an Excel file:'), sg.InputText(key='FILE'), sg.FileBrowse()],
    [sg.Text('Average:', size=(10, 1)), sg.Text('', size=(20, 1), key='AVERAGE')],
    [sg.Text('Median:', size=(10, 1)), sg.Text('', size=(20, 1), key='MEDIAN')],
    [sg.Text('Mode:', size=(10, 1)), sg.Text('', size=(20, 1), key='MODE')],
    [sg.Text('Variance (S^2):', size=(15, 1)), sg.Text('', size=(20, 1), key='VARIANCE')],
    [sg.Text('Typical desviation (s^2):', size=(17, 1)), sg.Text('', size=(20, 1), key='TYPICAL DESVIATION')],
    [sg.Button('Calculate')]

]
#Defino la interfaz de la parte de la calculadora que te pinta gráficas polinómicas
plot_function_layout = [

    [sg.Text('Plot Function', font=('Helvetica', 15))],
    [sg.Text('Enter a polinomical function:'), sg.InputText(key='FUNCTION_INPUT')],
    [sg.Button('Plot')],
    [sg.Graph(canvas_size=(600, 400), graph_bottom_left=(-10,-10), graph_top_right=(10,10), key='-PLOT-')],


]
#Aquí defino la interfaz que aparecerá cuando inicies el programa 
layout = [
    [sg.Menubar([['Menu',['Calculator','Data Analytics','Plot Function']]])],
    [sg.Column(calculator_layout, key='-CALCULATOR-', visible=False), sg.Column(statistics_layout, key='-DATA_ANALYTICS-', visible=False),sg.Column(plot_function_layout, key='-PLOT_FUNCTION-', visible=False)]
]

window = sg.Window("Ultra calculadora", layout, size = (600,400))

calculator_appearance = False
statistics_appearance = False
plot_function_appearance = False
display = ''    #Inicializo la barra de la calculadora para que se pueda escribir sobre ella 
# Aquí inicializo la pantalla
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
# Dependiendo de la opción que eliges sobre el menú aparecerá una opción u otra    
    if event == 'Calculator':
        calculator_appearance = True
        statistics_appearance = False
        plot_function_appearance = False
    
    elif event == 'Data Analytics':
        calculator_appearance = False
        statistics_appearance = True
        plot_function_appearance = False
    elif event == 'Plot Function':
        calculator_appearance = False
        statistics_appearance = False
        plot_function_appearance = True

# Esta parte está para que cuando pulses una opción del menú se actualice la pantalla con la calculadora correspondiente
    window['-CALCULATOR-'].update(visible=calculator_appearance)
    window['-DATA_ANALYTICS-'].update(visible=statistics_appearance)
    window['-PLOT_FUNCTION-'].update(visible=plot_function_appearance)

# Cuando pulses una tecla en la calculadora, dependiendo de la tecla pulsada, se mostrará en la pantalla o te mostrará el resultado directamente
    
    if calculator_appearance:

        if event in "1234567890.":
            display = display + event
        elif event in ("+","-","*","/"):
            display = display + event
        elif event == "AC":
            display = ''
        elif event == '^':
            display = display + '**'
        elif event == '=':
            try:
                result = eval(display)  # Este comando permite evaluar la operación que hay en la pantalla de la calculadora 
                display = str(result)
            except Exception as e:
                display = 'ERROR'       # Si hay alguna operación que no se pueda calcular mostrará la palabra error en vez de cerrar el programa
            
        elif event == 'log':
            display = math.log10(float(display))
        elif event == 'ln':
            display = math.log(float(display))
        elif event == 'rad':
            display = math.radians(float(display))
        elif event == 'sin':
            display = math.sin(float(display))
        elif event == '√':
            display = math.sqrt(float(display))
        elif event == 'π':
            display = display + str(math.pi)
        elif event == '(':
            display = display + event
        elif event == ')':
            display = display + event
# Esta es la parte del código que tiene que ver con la calculadora de estadística 
    elif statistics_appearance:
        if event == 'Calculate':
            file_path = values['FILE'] 
            try:
                if file_path.endswith('.xlsx'):# Analiza el tipo de archivo para procurar que sea un excel
                    df = pd.read_excel(file_path) # Transforma los el archivo excel a un DataFrame
                    numbers = df.iloc[:,0].tolist() # Recoge los números de la primera columna y los almacena en una variable
                    if numbers:
# Se calcula todos los datos necesarios a través de la librería statistic
                        average_val = sum(numbers) / len(numbers)
                        median_val = median(numbers)
                        mode_val = mode(numbers)
                        var_val = variance(numbers)
                        pvar_val = pvariance(numbers)
                        window['AVERAGE'].update(f'{average_val:.2f}')
                        window['MEDIAN'].update(f'{median_val:.2f}')
                        window['MODE'].update(f'{mode_val}')
                        window['VARIANCE'].update(f'{var_val:.2f}')
                        window['TYPICAL DESVIATION'].update(f'{pvar_val}')
                    else:
                        sg.popup_error('No numbers found in the file.') # En el caso de que haya un error te aparecerá un mensaje de error en la pantalla dependiendo del tipo de error
                        
            except FileNotFoundError:
                sg.popup_error('File not found.')
            except Exception as e:
                sg.popup_error(f'An error ocurred: {str(e)}')
# Esta es la parte de la calculadora que está relacionada con pintar funciones 
    elif plot_function_appearance:
        if event == 'Plot':
            try: 
                func = values['FUNCTION_INPUT']
                x_vals = np.linspace(-10, 10, 1000) # Esto significa que hay 1000 valores de x comprendidos entre el -10 y el 10
                y_vals = eval(func, {'x': x_vals}) # Dependiendo de la función que le hayamos pasado, a cada valor de x se le asignará una y correspondiente
                plt.figure()
                plt.plot(x_vals, y_vals)
                plt.xlabel('X')
                plt.ylabel('Y')
                plt.title('Plot of ' + func)
                plt.grid()
                plt.axhline(0, color='black',linewidth=0.5)
                plt.axvline(0, color='black',linewidth=0.5)
                plt.show()
            except Exception as e: # En este caso también tiene una parte que se encarga de los errores 
                sg.popup_error(f'An error occurred: {str(e)}')
        





    window['DISPLAY'].update(display) # Esto es para que se actualice la pantalla de la calculadora básica
    

    




window.close()

