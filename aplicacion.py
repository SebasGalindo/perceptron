import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.gridspec as gridspec
from tkinter import PhotoImage
from PIL import Image, ImageTk

import os
import json
from entrenamiento import entrenamiento_normal, entrenamiento_xor, aplicacion_normal, aplicacion_xor, regenerar_valores

# Variables globales para la creacion de pesos
# Definicion de las entradas
entradas = [[0,1,0,1],[0,0,1,1]]
# Definicion de las salidas [OR, AND, NAND]
salidas = [[0,1,1,1],[0,0,0,1],[1,1,1,0]]

# Variables globales para la interfaz grafica
ventana_principal = None
titulo = None
participantes = None
sidebar = None
descripcion = None
logo_UdeC = None
canvas = None
frame_principal = None
seleccion = None
valores_pesos = None
x1_entry, x2_entry = None, None
w0_entry, w1_entry, w2_entry, w3_entry, w4_entry, w5_entry, w6_entry, w7_entry, w8_entry = None, None, None, None, None, None, None, None, None
label_resultado = None

def frame_graficas():
    global canvas, frame_principal

    if canvas is not None:
        canvas.get_tk_widget().grid_forget()

    frame_principal = ctk.CTkFrame(master=ventana_principal, corner_radius=0, fg_color="#1D3F23" )
    frame_principal.grid(row=0, column=1, sticky="nsew")

    frame_principal.grid_rowconfigure(0, weight=0)
    frame_principal.grid_columnconfigure(0, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)
    frame_principal.grid_columnconfigure(2, weight=1)
    frame_principal.grid_rowconfigure(4, weight=2)


    # Creación de un label con los pesos de la compuerta OR
    titulo_or = ctk.CTkLabel(master=frame_principal, text="Pesos de la compuerta OR", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    titulo_or.grid(row=0, column=0, pady=5, padx=5, sticky="ew")

    valores_or = ctk.CTkLabel(master=frame_principal, text=f"W0: {pesos_json['or'][0]:.2f} - W11: {pesos_json['or'][1]:.2f} - W12: {pesos_json['or'][2]:.2f} ", font=("Arial", 14), text_color="white", anchor="center")
    valores_or.grid(row=1, column=0, pady=5, padx=5, sticky="ew")

    # Creación de un label con los pesos de la compuerta AND
    titulo_and = ctk.CTkLabel(master=frame_principal, text="Pesos de la compuerta AND", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    titulo_and.grid(row=0, column=1,  pady=5, padx=5, sticky="ew")

    valores_and = ctk.CTkLabel(master=frame_principal, text=f"W0: {pesos_json['and'][0]:.2f} - W11: {pesos_json['and'][1]:.2f} - W12: {pesos_json['and'][2]:.2f} ", font=("Arial", 14), text_color="white", anchor="center")
    valores_and.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

    # Creación de un label con los pesos de la compuerta NAND
    titulo_nand = ctk.CTkLabel(master=frame_principal, text="Pesos de la compuerta NAND", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    titulo_nand.grid(row=0, column=2, pady=5, padx=5, sticky="ew")

    valores_nand = ctk.CTkLabel(master=frame_principal, text=f"W0: {pesos_json['nand'][0]:.2f} - W11: {pesos_json['nand'][1]:.2f} - W12: {pesos_json['nand'][2]:.2f} ", font=("Arial", 14), text_color="white", anchor="center")
    valores_nand.grid(row=1, column=2, pady=5, padx=5, sticky="ew")

    # Creación de un label con los pesos de la compuerta XOR
    titulo_xor = ctk.CTkLabel(master=frame_principal, text="Pesos de la compuerta XOR", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    titulo_xor.grid(row=2, column=0, columnspan=3 ,  pady=2, padx=5, sticky="ew")

    valores_xor = ctk.CTkLabel(master=frame_principal, text=f"W00: {pesos_json['xor'][0][0]:.2f} - W1: {pesos_json['xor'][0][1]:.2f} - W2: {pesos_json['xor'][0][2]:.2f} "+
                               f" - W01: {pesos_json['xor'][1][0]:.2f} - W3: {pesos_json['xor'][1][1]:.2f} - W4: {pesos_json['xor'][1][2]:.2f}"+
                               f" - W02: {pesos_json['xor'][2][0]:.2f} - W5: {pesos_json['xor'][2][1]:.2f} - W6: {pesos_json['xor'][2][2]:.2f}", font=("Arial", 14), text_color="white", anchor="center")
    valores_xor.grid(row=3, column=0, columnspan=3, pady=5, padx=5, sticky="ew")

    # Creación de la gráfica de la compuerta OR
    figura = plt.Figure(dpi=100)
    gs = gridspec.GridSpec(4, 3, height_ratios=[1, 1, 1, 0.5], width_ratios=[1, 1, 1])

    grafica_or = graficas_json['or']
    ax_or = figura.add_subplot(gs[0, :])
    ax_or.plot(grafica_or['epoca'], grafica_or['errores']['patron_1'], label="Patron 1", color="red", marker="o")
    ax_or.plot(grafica_or['epoca'], grafica_or['errores']['patron_2'], label="Patron 2", color="blue", marker="*")
    ax_or.plot(grafica_or['epoca'], grafica_or['errores']['patron_3'], label="Patron 3", color="green", marker="x")
    ax_or.plot(grafica_or['epoca'], grafica_or['errores']['patron_4'], label="Patron 4", color="purple", marker="s")
    
    ax_or.set_xlabel("Epocas")
    ax_or.set_ylabel("Errores")
    ax_or.set_title("Errores por epoca - Compuerta OR")
    ax_or.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Creación de la gráfica de la compuerta AND
    grafica_and = graficas_json['and']
    ax_and = figura.add_subplot(gs[1, :])
    ax_and.plot(grafica_and['epoca'], grafica_and['errores']['patron_1'], label="Patron 1", color="red", marker="o")
    ax_and.plot(grafica_and['epoca'], grafica_and['errores']['patron_2'], label="Patron 2", color="blue", marker="*")
    ax_and.plot(grafica_and['epoca'], grafica_and['errores']['patron_3'], label="Patron 3", color="green", marker="x")
    ax_and.plot(grafica_and['epoca'], grafica_and['errores']['patron_4'], label="Patron 4", color="purple", marker="s")

    ax_and.set_xlabel("Epocas")
    ax_and.set_ylabel("Errores")
    ax_and.set_title("Errores por epoca - Compuerta AND")

    grafica_nand = graficas_json['nand']
    ax_nand = figura.add_subplot(gs[2, :])
    ax_nand.plot(grafica_nand['epoca'], grafica_nand['errores']['patron_1'], label="Patron 1", color="red", marker="o")
    ax_nand.plot(grafica_nand['epoca'], grafica_nand['errores']['patron_2'], label="Patron 2", color="blue", marker="*")
    ax_nand.plot(grafica_nand['epoca'], grafica_nand['errores']['patron_3'], label="Patron 3", color="green", marker="x")
    ax_nand.plot(grafica_nand['epoca'], grafica_nand['errores']['patron_4'], label="Patron 4", color="purple", marker="s")

    ax_nand.set_xlabel("Epocas")
    ax_nand.set_ylabel("Errores")
    ax_nand.set_title("Errores por epoca - Compuerta NAND")

    # Creación de las 3 graficas de la compuerta XOR
    grafica_xor_1 = graficas_json['xor']['entramiento1']
    grafica_xor_2 = graficas_json['xor']['entramiento2']
    grafica_xor_3 = graficas_json['xor']['entramiento3']

    ax_xor1 = figura.add_subplot(gs[3, 0])
    ax_xor1.plot(grafica_xor_1['epoca'], grafica_xor_1['errores']['patron_1'], label="Patron 1", color="red", marker="o")
    ax_xor1.plot(grafica_xor_1['epoca'], grafica_xor_1['errores']['patron_2'], label="Patron 2", color="blue", marker="*")
    ax_xor1.plot(grafica_xor_1['epoca'], grafica_xor_1['errores']['patron_3'], label="Patron 3", color="green", marker="x")
    ax_xor1.plot(grafica_xor_1['epoca'], grafica_xor_1['errores']['patron_4'], label="Patron 4", color="purple", marker="s")

    ax_xor1.set_ylabel("Errores")
    ax_xor1.set_title("XOR 1er train (AND) ")

    ax_xor2 = figura.add_subplot(gs[3, 1])
    ax_xor2.plot(grafica_xor_2['epoca'], grafica_xor_2['errores']['patron_1'], label="Patron 1", color="red", marker="o")
    ax_xor2.plot(grafica_xor_2['epoca'], grafica_xor_2['errores']['patron_2'], label="Patron 2", color="blue", marker="*")
    ax_xor2.plot(grafica_xor_2['epoca'], grafica_xor_2['errores']['patron_3'], label="Patron 3", color="green", marker="x")
    ax_xor2.plot(grafica_xor_2['epoca'], grafica_xor_2['errores']['patron_4'], label="Patron 4", color="purple", marker="s")

    ax_xor2.set_xlabel("Epocas")
    ax_xor2.set_title("XOR 2do train (AND) ")

    ax_xor3 = figura.add_subplot(gs[3, 2])
    ax_xor3.plot(grafica_xor_3['epoca'], grafica_xor_3['errores']['patron_1'], label="Patron 1", color="red", marker="o")
    ax_xor3.plot(grafica_xor_3['epoca'], grafica_xor_3['errores']['patron_2'], label="Patron 2", color="blue", marker="*")
    ax_xor3.plot(grafica_xor_3['epoca'], grafica_xor_3['errores']['patron_3'], label="Patron 3", color="green", marker="x")
    ax_xor3.plot(grafica_xor_3['epoca'], grafica_xor_3['errores']['patron_4'], label="Patron 4", color="purple", marker="s")

    ax_xor3.set_title("XOR 3er train (OR) ")

    figura.subplots_adjust(left=0.08, right=0.88, top= 0.94 ,bottom=0.08, wspace=0.1, hspace=0.8)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(figura, master=frame_principal)
    canvas.draw()
    canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, rowspan=2,  sticky="nsew", pady = 5, padx = 15)

def pruebas():
    global canvas, valores_pesos, seleccion, x1_entry, x2_entry, label_resultado,w0_entry, w1_entry, w2_entry, w3_entry, w4_entry, w5_entry, w6_entry, w7_entry, w8_entry

    if canvas is not None:
        canvas.get_tk_widget().grid_forget()

    frame_principal = ctk.CTkFrame(master=ventana_principal, corner_radius=0, fg_color="#1D3F23" )
    frame_principal.grid(row=0, column=1, sticky="nsew")

    frame_principal.grid_rowconfigure(0, weight=0)
    frame_principal.grid_rowconfigure(1, weight=0)
    frame_principal.grid_rowconfigure(3, weight=0)
    frame_principal.grid_rowconfigure(5, weight=0)
    frame_principal.grid_columnconfigure(0, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)
    frame_principal.grid_columnconfigure(2, weight=1)
    frame_principal.grid_columnconfigure(3, weight=1)
    frame_principal.grid_columnconfigure(4, weight=1)
    frame_principal.grid_columnconfigure(5, weight=1)
    frame_principal.grid_columnconfigure(6, weight=1)
    frame_principal.grid_columnconfigure(7, weight=1)
    frame_principal.grid_columnconfigure(8, weight=1)

    # Creación de un label sobre las opciones logicas a probar
    titulo_opciones = ctk.CTkLabel(master=frame_principal, text="Seleccione una opción logica", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    titulo_opciones.grid(row=0, column=0, pady=15, padx=5, sticky="ew",columnspan = 9)

    # Creación de una lista desplegable para poner las posibles selecciones
    opciones = ["or", "and", "nand", "xor"]
    seleccion = ctk.CTkComboBox(master=frame_principal, values=opciones, width=200, font=("Arial", 14, "bold"), state="readonly", command= actualizar_pesos,
                                fg_color="#fbe122", text_color="#0F1010", button_color="#FB9222", button_hover_color="#F3B677", border_color= "#FB9222",
                                dropdown_fg_color="#fbe122", dropdown_text_color="#0F1010", dropdown_hover_color="#FB9222") 
    seleccion.set("or")
    seleccion.grid(row=1, column=0, pady=5, padx=25,columnspan = 9)

    #titulo del calculo de los pesos
    label_pesos = ctk.CTkLabel(master=frame_principal, text="Se calculará el resultado NO personalizado con los pesos: ", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    label_pesos.grid(row=7, column=0, pady=5, padx=5, sticky="ew",columnspan = 9)

    # Creación de un label con los pesos de la logica seleccionada
    pesos = pesos_json[seleccion.get()]
    valores_pesos = ctk.CTkLabel(master=frame_principal, text=f"W0: {pesos[0]:.2f} - W11: {pesos[1]:.2f} - W12: {pesos[2]:.2f} ", font=("Arial", 14), text_color="white", anchor="center")
    valores_pesos.grid(row=8, column=0, pady=5, padx=5, sticky="ew",columnspan = 9)

    # Inputs para recibir x1 y x2
    label_x1 = ctk.CTkLabel(master=frame_principal, text="Ingrese el valor de x1", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    label_x1.grid(row=2, column=0, pady=15, padx=25, sticky="ew", columnspan = 9)
    x1_entry = ctk.CTkEntry(master=frame_principal, placeholder_text = '0 o 1', placeholder_text_color = "#181717", font=("Arial", 14, "bold"), fg_color="#fbe122", text_color="#0F1010", border_color= "#FB9222")
    x1_entry.grid(row=3, column=0, pady=2, padx=25,columnspan = 9)
    label_x2 = ctk.CTkLabel(master=frame_principal, text="Ingrese el valor de x2", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    label_x2.grid(row=4, column=0, pady=15, padx=25, sticky="ew",columnspan = 9)
    x2_entry = ctk.CTkEntry(master=frame_principal, placeholder_text = '0 o 1', placeholder_text_color = "#181717" , font=("Arial", 14, "bold"), fg_color="#fbe122", text_color="#0F1010", border_color= "#FB9222")
    x2_entry.grid(row=5, column=0, pady=2, padx=25,columnspan = 9)

    # label diciendo que el input debe ser 0 o 1
    label_advertencia = ctk.CTkLabel(master=frame_principal, text="Los valores de x1 y x2 deben ser 0 o 1", font=("Arial", 15, "bold"), text_color="#C7600D", anchor="center")
    label_advertencia.grid(row=6, column=0, pady=15, padx=25, sticky="ew",columnspan = 9)

    # Boton para probar la logica seleccionada
    boton_probar = ctk.CTkButton(master=frame_principal, height=50, width= 120 ,text="Probar", 
                                 fg_color="#fbe122", font=("Arial", 14, "bold"), hover_color="#E2B12F", 
                                 text_color="#0F1010", command= calcular_resultado, anchor="center")
    boton_probar.grid(row=9, column=0, pady=15, padx=15,columnspan = 4)

    # Lable para mostrar el resultado de la logica
    titulo_resultado = ctk.CTkLabel(master=frame_principal, text="Resultado de la logica:", font=("Arial", 20, "bold"), text_color="#fbe122", anchor="center")
    titulo_resultado.grid(row=10, column=0, pady=15, padx=25, sticky="ew", columnspan = 9)
    # Label para mostrar el resultado de la logica
    label_resultado = ctk.CTkLabel(master=frame_principal, text="-", font=("Arial", 25, "bold"), text_color="#3EC13E", anchor="center")
    label_resultado.grid(row=11, column=0, pady=15, padx=25, sticky="ew", columnspan = 9)

    # boton para probar con pesos personalizados
    boton_personalizado = ctk.CTkButton(master=frame_principal, height=50, width= 120 ,text="Probar con pesos personalizados",
                                    fg_color="#fbe122", font=("Arial", 14, "bold"), hover_color="#E2B12F", 
                                    text_color="#0F1010", command= lambda: calcular_resultado(2), anchor="center")
    boton_personalizado.grid(row=9, column=4, pady=15, padx=15,columnspan = 4)

    # 9 inputs para los pesos personalizados desactivados
    label_pesos_personalizados = ctk.CTkLabel(master=frame_principal, text="Ingrese los pesos personalizados", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    label_pesos_personalizados.grid(row=13, column=0, pady=15, padx=25, sticky="ew", columnspan = 9)

    label_w0 = ctk.CTkLabel(master=frame_principal, text="W0", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    label_w0.grid(row=14, column=0, pady=15, padx=5, sticky="ew")
    w0_entry = ctk.CTkEntry(master=frame_principal, placeholder_text = 'peso', placeholder_text_color = "#181717", font=("Arial", 14, "bold"), fg_color="#fbe122", text_color="#0F1010", border_color= "#FB9222")
    w0_entry.grid(row=15, column=0, pady=2, padx=5)
    label_w1 = ctk.CTkLabel(master=frame_principal, text="W1", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    label_w1.grid(row=14, column=1, pady=15, padx=5, sticky="ew")
    w1_entry = ctk.CTkEntry(master=frame_principal, placeholder_text = 'peso', placeholder_text_color = "#181717", font=("Arial", 14, "bold"), fg_color="#fbe122", text_color="#0F1010", border_color= "#FB9222")
    w1_entry.grid(row=15, column=1, pady=2, padx=5)
    label_w2 = ctk.CTkLabel(master=frame_principal, text="W2", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    label_w2.grid(row=14, column=2, pady=15, padx=5, sticky="ew")
    w2_entry = ctk.CTkEntry(master=frame_principal, placeholder_text = 'peso', placeholder_text_color = "#181717", font=("Arial", 14, "bold"), fg_color="#fbe122", text_color="#0F1010", border_color= "#FB9222")
    w2_entry.grid(row=15, column=2, pady=2, padx=5)
    label_w3 = ctk.CTkLabel(master=frame_principal, text="W01", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    label_w3.grid(row=14, column=3, pady=15, padx=5, sticky="ew")
    w3_entry = ctk.CTkEntry(master=frame_principal, state = "disabled", placeholder_text = 'peso', placeholder_text_color = "#181717", font=("Arial", 14, "bold"), fg_color="#fbe122", text_color="#0F1010", border_color= "#FB9222")
    w3_entry.grid(row=15, column=3, pady=2, padx=5)
    label_w4 = ctk.CTkLabel(master=frame_principal, text="W4", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    label_w4.grid(row=14, column=4, pady=15, padx=5, sticky="ew")
    w4_entry = ctk.CTkEntry(master=frame_principal, state = "disabled", placeholder_text = 'peso', placeholder_text_color = "#181717", font=("Arial", 14, "bold"), fg_color="#fbe122", text_color="#0F1010", border_color= "#FB9222")
    w4_entry.grid(row=15, column=4, pady=2, padx=5)
    label_w5 = ctk.CTkLabel(master=frame_principal, text="W5", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    label_w5.grid(row=14, column=5, pady=15, padx=5, sticky="ew")
    w5_entry = ctk.CTkEntry(master=frame_principal, state = "disabled", placeholder_text = 'peso', placeholder_text_color = "#181717", font=("Arial", 14, "bold"), fg_color="#fbe122", text_color="#0F1010", border_color= "#FB9222")
    w5_entry.grid(row=15, column=5, pady=2, padx=5)
    label_w6 = ctk.CTkLabel(master=frame_principal, text="W02", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    label_w6.grid(row=14, column=6, pady=15, padx=5, sticky="ew")
    w6_entry = ctk.CTkEntry(master=frame_principal, state = "disabled", placeholder_text = 'peso', placeholder_text_color = "#181717", font=("Arial", 14, "bold"), fg_color="#fbe122", text_color="#0F1010", border_color= "#FB9222")
    w6_entry.grid(row=15, column=6, pady=2, padx=5)
    label_w7 = ctk.CTkLabel(master=frame_principal, text="W7", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    label_w7.grid(row=14, column=7, pady=15, padx=5, sticky="ew")
    w7_entry = ctk.CTkEntry(master=frame_principal, state = "disabled", placeholder_text = 'peso', placeholder_text_color = "#181717", font=("Arial", 14, "bold"), fg_color="#fbe122", text_color="#0F1010", border_color= "#FB9222")
    w7_entry.grid(row=15, column=7, pady=2, padx=5)
    label_w8 = ctk.CTkLabel(master=frame_principal, state = "disabled", text="W8", font=("Arial", 16, "bold"), text_color="#fbe122", anchor="center")
    label_w8.grid(row=14, column=8, pady=15, padx=5, sticky="ew")
    w8_entry = ctk.CTkEntry(master=frame_principal, state = "disabled", placeholder_text = 'peso', placeholder_text_color = "#181717", font=("Arial", 14, "bold"), fg_color="#fbe122", text_color="#0F1010", border_color= "#FB9222")
    w8_entry.grid(row=15, column=8, pady=2, padx=5)

def calcular_resultado(op = 1):
    global label_resultado, x1_entry, x2_entry, seleccion,w0_entry, w1_entry, w2_entry,  w3_entry, w4_entry, w5_entry, w6_entry, w7_entry, w8_entry
    opcion = seleccion.get()
    x1 = x1_entry.get()
    x2 = x2_entry.get()
    if x1 == '' or x2 == '':
        label_resultado.configure(text="MAL")
        return
    if x1 != '0' and x1 != '1':
        label_resultado.configure(text="MAL")
        return
    if x2 != '0' and x2 != '1':
        label_resultado.configure(text="MAL")
        return
    
    x1 = int(x1)
    x2 = int(x2)
    pesos = []

    try: 
        if op == 1:
            pesos = pesos_json[opcion]
        elif op == 2 and opcion != 'xor':
                pesos = [float(w0_entry.get()), float(w1_entry.get()), float(w2_entry.get())]
        elif op == 2 and opcion == 'xor':
                pesos = [[float(w0_entry.get()), float(w1_entry.get()), float(w2_entry.get())],
                         [float(w3_entry.get()), float(w4_entry.get()), float(w5_entry.get())],
                         [float(w6_entry.get()), float(w7_entry.get()), float(w8_entry.get())]]
    except ValueError as e:
                label_resultado.configure(text="MAL")
                print(e)
                return


    if opcion != 'xor':
        resultado, _ = aplicacion_normal([[x1,x2]], pesos)
        label_resultado.configure(text=f"{resultado[0]}")
    else:
        resultado, _ = aplicacion_xor([[x1,x2]], pesos)
        label_resultado.configure(text=f"{resultado[0]}")

def actualizar_pesos(opcion):
    global valores_pesos
    # Actualización directa de la propiedad text
    pesos = pesos_json[opcion]
    if opcion != 'xor':
        valores_pesos.configure(text=f"W0: {pesos[0]:.2f} - W11: {pesos[1]:.2f} - W12: {pesos[2]:.2f}")
        w3_entry.configure(state = "disabled")
        w4_entry.configure(state = "disabled")
        w5_entry.configure(state = "disabled")
        w6_entry.configure(state = "disabled")
        w7_entry.configure(state = "disabled")
        w8_entry.configure(state = "disabled")

    else:
        valores_pesos.configure(text=f"W00: {pesos[0][0]:.2f} - W1: {pesos[0][1]:.2f} - W2: {pesos[0][2]:.2f} "+
                               f" - W01: {pesos[1][0]:.2f} - W3: {pesos[1][1]:.2f} - W4: {pesos[1][2]:.2f}"+
                               f" - W02: {pesos[2][0]:.2f} - W5: {pesos[2][1]:.2f} - W6: {pesos[2][2]:.2f}")
        w3_entry.configure(state = "normal")
        w4_entry.configure(state = "normal")
        w5_entry.configure(state = "normal")
        w6_entry.configure(state = "normal")
        w7_entry.configure(state = "normal")
        w8_entry.configure(state = "normal")      

def actualizar_pesos_frame():
    global valores_pesos, canvas, pesos_json, graficas_json

    if canvas is not None:
        canvas.get_tk_widget().grid_forget()
    
    frame_principal = ctk.CTkFrame(master=ventana_principal, corner_radius=0, fg_color="#1D3F23" )
    frame_principal.grid(row=0, column=1, sticky="nsew")
    frame_principal.grid_rowconfigure(0, weight=0)
    frame_principal.grid_rowconfigure(11, weight=3)
    frame_principal.grid_columnconfigure(0, weight=1)
    frame_principal.grid_columnconfigure(1, weight=1)
    frame_principal.grid_columnconfigure(2, weight=1)

    # Titulo de pesos antiguos
    titulo_pesos_antiguos = ctk.CTkLabel(master=frame_principal, text="Pesos antiguos", font=("Arial", 18, "bold"), text_color="#fbe122", anchor="center")
    titulo_pesos_antiguos.grid(row=0, column=0, pady=3, padx=5, sticky="ew", columnspan = 3)
    
    # Creación de un label con los pesos de la compuerta OR
    
    titulo_or_antiguo = ctk.CTkLabel(master=frame_principal, text="Pesos de la compuerta OR", font=("Arial", 15, "bold"), text_color="#fbe122", anchor="center")
    titulo_or_antiguo.grid(row=1, column=0, pady=0, padx=5, sticky="ew")

    valores_or_antiguo = ctk.CTkLabel(master=frame_principal, text=f"W0: {pesos_json['or'][0]:.2f} - W11: {pesos_json['or'][1]:.2f} - W12: {pesos_json['or'][2]:.2f} ", font=("Arial", 14), text_color="white", anchor="center")
    valores_or_antiguo.grid(row=2, column=0, pady=0, padx=5, sticky="ew")

    # Creación de un label con los pesos de la compuerta AND
    titulo_and_antiguo = ctk.CTkLabel(master=frame_principal, text="Pesos de la compuerta AND", font=("Arial", 15, "bold"), text_color="#fbe122", anchor="center")
    titulo_and_antiguo.grid(row=1, column=1,  pady=0, padx=5, sticky="ew")

    valores_and_antiguo = ctk.CTkLabel(master=frame_principal, text=f"W0: {pesos_json['and'][0]:.2f} - W11: {pesos_json['and'][1]:.2f} - W12: {pesos_json['and'][2]:.2f} ", font=("Arial", 14), text_color="white", anchor="center")
    valores_and_antiguo.grid(row=2, column=1, pady=0, padx=5, sticky="ew")

    # Creación de un label con los pesos de la compuerta NAND
    titulo_nand_antiguo = ctk.CTkLabel(master=frame_principal, text="Pesos de la compuerta NAND", font=("Arial", 15, "bold"), text_color="#fbe122", anchor="center")
    titulo_nand_antiguo.grid(row=1, column=2, pady=0, padx=5, sticky="ew")

    valores_nand_antiguo = ctk.CTkLabel(master=frame_principal, text=f"W0: {pesos_json['nand'][0]:.2f} - W11: {pesos_json['nand'][1]:.2f} - W12: {pesos_json['nand'][2]:.2f} ", font=("Arial", 14), text_color="white", anchor="center")
    valores_nand_antiguo.grid(row=2, column=2, pady=0, padx=5, sticky="ew")

    # Creación de un label con los pesos de la compuerta XOR
    titulo_xor_antiguo = ctk.CTkLabel(master=frame_principal, text="Pesos de la compuerta XOR", font=("Arial", 15, "bold"), text_color="#fbe122", anchor="center")
    titulo_xor_antiguo.grid(row=3, column=0, columnspan=3 , pady = 0, padx=5, sticky="ew")

    valores_xor_antiguo = ctk.CTkLabel(master=frame_principal, text=f"W00: {pesos_json['xor'][0][0]:.2f} - W1: {pesos_json['xor'][0][1]:.2f} - W2: {pesos_json['xor'][0][2]:.2f} "+
                               f"W01: {pesos_json['xor'][1][0]:.2f} - W3: {pesos_json['xor'][1][1]:.2f} - W4: {pesos_json['xor'][1][2]:.2f}"+
                               f"W02: {pesos_json['xor'][2][0]:.2f} - W5: {pesos_json['xor'][2][1]:.2f} - W6: {pesos_json['xor'][2][2]:.2f}", font=("Arial", 14), text_color="white", anchor="center")
    valores_xor_antiguo.grid(row=4, column=0, columnspan=3, pady=0, padx=5, sticky="ew")

    pesos_json, graficas_json = creacion_pesos()
    # Se guardan los pesos
    with open(ruta_pesos_json, 'w') as file:
        json.dump(pesos_json, file)
    with open(ruta_graficas_json, 'w') as file:
        json.dump(graficas_json, file)

        # Titulo de pesos antiguos
    titulo_pesos_nuevos = ctk.CTkLabel(master=frame_principal, text="Pesos Nuevos", font=("Arial", 18, "bold"), text_color="#fbe122", anchor="center")
    titulo_pesos_nuevos.grid(row=6, column=0, pady=3, padx=5, sticky="ew", columnspan = 3)
    
    # Creación de un label con los pesos de la compuerta OR
    
    titulo_or = ctk.CTkLabel(master=frame_principal, text="Pesos de la compuerta OR", font=("Arial", 15, "bold"), text_color="#fbe122", anchor="center")
    titulo_or.grid(row=7, column=0, pady=0, padx=5, sticky="ew")

    valores_or = ctk.CTkLabel(master=frame_principal, text=f"W0: {pesos_json['or'][0]:.2f} - W11: {pesos_json['or'][1]:.2f} - W12: {pesos_json['or'][2]:.2f} ", font=("Arial", 14), text_color="white", anchor="center")
    valores_or.grid(row=8, column=0, pady=0, padx=5, sticky="ew")

    # Creación de un label con los pesos de la compuerta AND
    titulo_and = ctk.CTkLabel(master=frame_principal, text="Pesos de la compuerta AND", font=("Arial", 15, "bold"), text_color="#fbe122", anchor="center")
    titulo_and.grid(row=7, column=1,  pady=0, padx=5, sticky="ew")

    valores_and = ctk.CTkLabel(master=frame_principal, text=f"W0: {pesos_json['and'][0]:.2f} - W11: {pesos_json['and'][1]:.2f} - W12: {pesos_json['and'][2]:.2f} ", font=("Arial", 14), text_color="white", anchor="center")
    valores_and.grid(row=8, column=1, pady=0, padx=5, sticky="ew")

    # Creación de un label con los pesos de la compuerta NAND
    titulo_nand = ctk.CTkLabel(master=frame_principal, text="Pesos de la compuerta NAND", font=("Arial", 15, "bold"), text_color="#fbe122", anchor="center")
    titulo_nand.grid(row=7, column=2, pady=0, padx=5, sticky="ew")

    valores_nand = ctk.CTkLabel(master=frame_principal, text=f"W0: {pesos_json['nand'][0]:.2f} - W11: {pesos_json['nand'][1]:.2f} - W12: {pesos_json['nand'][2]:.2f} ", font=("Arial", 14), text_color="white", anchor="center")
    valores_nand.grid(row=8, column=2, pady=0, padx=5, sticky="ew")

    # Creación de un label con los pesos de la compuerta XOR
    titulo_xor = ctk.CTkLabel(master=frame_principal, text="Pesos de la compuerta XOR", font=("Arial", 15, "bold"), text_color="#fbe122", anchor="center")
    titulo_xor.grid(row=9, column=0, columnspan=3 , pady = 0, padx=5, sticky="ew")

    valores_xor = ctk.CTkLabel(master=frame_principal, text=f"W00: {pesos_json['xor'][0][0]:.2f} - W1: {pesos_json['xor'][0][1]:.2f} - W2: {pesos_json['xor'][0][2]:.2f} "+
                               f"W01: {pesos_json['xor'][1][0]:.2f} - W3: {pesos_json['xor'][1][1]:.2f} - W4: {pesos_json['xor'][1][2]:.2f}"+
                               f"W02: {pesos_json['xor'][2][0]:.2f} - W5: {pesos_json['xor'][2][1]:.2f} - W6: {pesos_json['xor'][2][2]:.2f}", font=("Arial", 14), text_color="white", anchor="center")
    valores_xor.grid(row=10, column=0, columnspan=3, pady=0, padx=5, sticky="ew")

       # Creación de la gráfica de la compuerta OR
    figura = plt.Figure(dpi=100)

    grafica_or = graficas_json['or']
    ax_or = figura.add_subplot(311)
    ax_or.plot(grafica_or['epoca'], grafica_or['pesos']['w0'], label="w0", color="red", marker="o")
    ax_or.plot(grafica_or['epoca'], grafica_or['pesos']['w1'], label="w1", color="blue", marker="*")
    ax_or.plot(grafica_or['epoca'], grafica_or['pesos']['w2'], label="w2", color="green", marker="x")
    
    ax_or.set_ylabel("Pesos")
    ax_or.set_title("Pesos por epoca - Compuerta OR")
    ax_or.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Creación de la gráfica de la compuerta AND
    grafica_and = graficas_json['and']
    ax_and = figura.add_subplot(312)
    ax_and.plot(grafica_and['epoca'], grafica_and['pesos']['w0'], label="w0", color="red", marker="o")
    ax_and.plot(grafica_and['epoca'], grafica_and['pesos']['w1'], label="w1", color="blue", marker="*")
    ax_and.plot(grafica_and['epoca'], grafica_and['pesos']['w2'], label="w2", color="green", marker="x")

    ax_and.set_ylabel("Pesos")
    ax_and.set_title("Pesos por epoca - Compuerta AND")

    grafica_nand = graficas_json['nand']
    ax_nand = figura.add_subplot(313)
    ax_nand.plot(grafica_nand['epoca'], grafica_nand['pesos']['w0'], label="w0", color="red", marker="o")
    ax_nand.plot(grafica_nand['epoca'], grafica_nand['pesos']['w1'], label="w1", color="blue", marker="*")
    ax_nand.plot(grafica_nand['epoca'], grafica_nand['pesos']['w2'], label="w2", color="green", marker="x")

    ax_nand.set_xlabel("Epocas")
    ax_nand.set_ylabel("Pesos")
    ax_nand.set_title("Pesos por epoca - Compuerta NAND")

    figura.subplots_adjust(left=0.08, right=0.88, top= 0.94 ,bottom=0.08, wspace=0.1, hspace=0.5)
    plt.tight_layout()
    canvas = FigureCanvasTkAgg(figura, master=frame_principal)
    canvas.draw()
    canvas.get_tk_widget().grid(row=11, column=0, columnspan=3, rowspan=2,  sticky="nsew", pady = 5, padx = 15)

def creacion_GUI():
    global ventana_principal, titulo, descripcion, logo_UdeC

    # Creación de la ventana principal
    ventana_principal = ctk.CTk()
    ventana_principal.title("Inteligencia Artificial - Perceptron")
    ventana_principal.geometry("1200x800")
    ventana_principal.resizable(False, False)
    ventana_principal.iconbitmap("Resources/brand_logo.ico")
    ventana_principal.attributes('-topmost', True)
    ventana_principal.lift()
    ventana_principal.grid_columnconfigure(1, weight=1)  # Permite que la columna se expanda
    ventana_principal.grid_rowconfigure(0, weight=1)  

    # Creación del sidebar
    sidebar = ctk.CTkFrame(master=ventana_principal, width=200, fg_color="#11371A", corner_radius=0)
    sidebar.grid(row=0, column=0, sticky="nsew")

    # Separador vertical
    ctk.CTkFrame(master=ventana_principal, width=2, fg_color="#0B2310").grid(row=0, column=1, sticky="ns")

    # Creación del logo de la UdeC
    logo_UdeC = Image.open("Resources/logo_UdeC.png")
    logo_UdeC = ctk.CTkImage(dark_image=logo_UdeC, size=(60, 90))

    # Creación del título
    titulo = ctk.CTkLabel(master=sidebar, text="  Perceptron Monocapa", image=logo_UdeC, font=("Arial", 18), compound="left")
    titulo.grid(row=0, column=0, pady=10, sticky="n")

    # Separador horizontal
    ctk.CTkFrame(master=sidebar, height=2, fg_color="#0B2310").grid(row=1, column=0, sticky="ew", pady=5)

    # Creación de los autores
    participantes = ctk.CTkLabel(master=sidebar, text="Autores: \nJohn Sebastián Galindo Hernández \nMiguel Ángel Moreno Beltrán", font=("Arial", 16))
    participantes.grid(row=2, column=0, pady=10, padx=5, sticky="n")

    # Separador horizontal
    ctk.CTkFrame(master=sidebar, height=2, fg_color="#0B2310").grid(row=3, column=0, sticky="ew", pady=5)

    # Creación de la descripción
    descripcion_txt = ("Para ver todos los pesos de las compuertas de abajo junto con su gráfica "
                       "seleccione 'ver pesos y entrenamiento', si quiere entrenar de nuevo seleccione "
                       "'entrenar de nuevo', si quiere probar las soluciones (OR,AND,NAND,XOR) seleccione "
                       "probar soluciones'")
    descripcion = ctk.CTkLabel(master=sidebar, text=descripcion_txt, font=("Arial", 13), justify="left", width=190, wraplength=190)
    descripcion.grid(row=4, column=0, pady=10, padx=5, sticky="n")

    # Separador horizontal
    ctk.CTkFrame(master=sidebar, height=2, fg_color="#0B2310").grid(row=5, column=0, sticky="ew", pady=5)

    # Creación de los botones
    boton_mostrar_pesos = ctk.CTkButton(master=sidebar, text="Ver Pesos y Entrenamiento", fg_color="#fbe122", width=180, height=40, font=("Arial", 13, "bold"), hover_color="#E2B12F", text_color="#0F1010", command=frame_graficas)
    boton_mostrar_pesos.grid(row=6, column=0, pady=10, sticky="n")

    boton_entrenar_nuevo = ctk.CTkButton(master=sidebar, text="Entrenar de Nuevo", fg_color="#fbe122", width=180, height=40, font=("Arial", 13, "bold"), hover_color="#E2B12F", text_color="#0F1010", command=actualizar_pesos_frame)
    boton_entrenar_nuevo.grid(row=7, column=0, pady=10, sticky="n")

    boton_pruebas = ctk.CTkButton(master=sidebar, text="Probar soluciones", fg_color="#fbe122", width=180, height=40, font=("Arial", 13, "bold"), hover_color="#E2B12F", text_color="#0F1010", command=pruebas)
    boton_pruebas.grid(row=8, column=0, pady=10, sticky="n")

    # Creación del botón para graficar los errores
    frame_graficas()
    ventana_principal.mainloop()

def creacion_pesos():
    errores, pesos, iterador = regenerar_valores()
    print(f"Proceso de entrenamiento para la logica OR")
    pesos_OR, grafica_or = entrenamiento_normal(entradas,pesos,salidas[0],errores,iterador)

    errores, pesos, iterador = regenerar_valores()
    print(f"Proceso de entrenamiento para la logica AND")
    pesos_AND, grafica_and = entrenamiento_normal(entradas,pesos,salidas[1],errores,iterador)

    errores, pesos, iterador = regenerar_valores()
    print(f"Proceso de entrenamiento para la logica NAND")
    pesos_NAND, grafica_xand = entrenamiento_normal(entradas,pesos,salidas[2],errores,iterador)  

    print(f"Proceso de entrenamiento para la logica XOR")
    pesos_XOR, grafica_xor = entrenamiento_xor(entradas)

    pesos_json = {
            'or': pesos_OR,
            'and': pesos_AND,
            'nand': pesos_NAND,
            'xor': pesos_XOR
        }

    graficas_json = {
        'or': grafica_or,
        'and': grafica_and,
        'nand': grafica_xand,
        'xor': grafica_xor
    }

    return pesos_json, graficas_json

if __name__ == "__main__":
    # Acceso a los archivos de pesos
    ruta_pesos_json = os.path.join(os.getcwd(), 'Data/pesos.json')
    ruta_graficas_json = os.path.join(os.getcwd(), 'Data/graficas.json')
    pesos_json = {}
    graficas_json = {}
    # Verificando si el archivo de pesos existe
    if os.path.isfile(ruta_pesos_json) or os.path.isfile(ruta_graficas_json):
        # Si existe, se cargan los pesos
        with open(ruta_pesos_json, 'r') as file:
            pesos_json = json.load(file)
        with open(ruta_graficas_json, 'r') as file:
            graficas_json = json.load(file)
    else:
        # Si no existe, se crean los pesos
        pesos_json, graficas_json = creacion_pesos()
        # Se guardan los pesos
        with open(ruta_pesos_json, 'w') as file:
            json.dump(pesos_json, file)
        with open(ruta_graficas_json, 'w') as file:
            json.dump(graficas_json, file)

    # Creacion del GUI
    creacion_GUI()
