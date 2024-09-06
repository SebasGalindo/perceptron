import random

# Definicion del bias
X_0 = -1
# Definicion de la tasa de aprendizaje
alpha = 0.5
# Diccionario para los datos de la grafica
datos_grafica = {
    'epoca': [],
    'errores': {
      'patron_1': [],
      'patron_2': [],
      'patron_3': [],
      'patron_4': []
    }
  }


def generar_pesos():
  return [round(random.random(),2) for i in range(3)]

def regenerar_valores():
  errores = [random.randint(1,5) for i in range(4)]
  pesos = generar_pesos()
  iterador = 0
  return errores, pesos, iterador

def entrenamiento_normal(entradas,pesos,salidas,errores,epoca):
  # Calculando el numero de patrones que se tienen
  global datos_grafica
  if epoca == 0:
    datos_grafica = {
      'epoca': [],
      'errores': {
        'patron_1': [],
        'patron_2': [],
        'patron_3': [],
        'patron_4': []
      },
      'pesos': {
        'w0': [],
        'w1': [],
        'w2': []
      }
    }

  num_patrones = len(entradas[0])

  datos_grafica['epoca'].append(epoca)
  datos_grafica['errores']['patron_1'].append(errores[0])
  datos_grafica['errores']['patron_2'].append(errores[1])
  datos_grafica['errores']['patron_3'].append(errores[2])
  datos_grafica['errores']['patron_4'].append(errores[3])
  datos_grafica['pesos']['w0'].append(pesos[0])
  datos_grafica['pesos']['w1'].append(pesos[1])
  datos_grafica['pesos']['w2'].append(pesos[2])

  # Validando si hay algun error diferente a 0 en la matriz de errores, si hay algun error diferente a 0 se sigue entrenando
  while(any(valor != 0 for valor in errores)):
    #imprimir datos relevantes sobre la epoca
    epoca += 1
    print("------------------------------------ \n")
    print("Epoca  #" + str(epoca))
    print("Pesos:  " + str(pesos))
    print("Errores:  " + str(errores))

    # Haciendo el proceso por cada patron
    for i in range(num_patrones):

      # Armando el patron de la forma -> [X_0, X_1, X_2] donde X_0 es el bias (puede ser hasta X_n)
      patron = []
      patron.append(X_0)
      for j in range(len(entradas)):
        # Agregando las entradas de cada X_i al patron
        patron.append(entradas[j][i])

      # Imprimiendo el patron
      print(f"Patron #{i+1} {patron}")

      # Realizando la sumatoria de los pesos por las entradas
      sumatoria = 0
      for k in range(len(pesos)):
        sumatoria += pesos[k]*patron[k]

      # Verificacion de la sumatoria para obtener el resultado
      salida_obtenida = 1 if sumatoria > 0 else 0

      # Calculando el error con la formula de => error = salida_deseada - salida_obtenida
      nuevo_error = salidas[i] - salida_obtenida

      # Actualizando la matriz de errores
      errores[i] = nuevo_error
      print(f'\n Errores finales del patron # {i+1} { errores }\n')

      # Si el error es diferente de 0 se actualizan los pesos y se llama de forma recursiva a la funcion de entrenamiento
      # para empezar otra epoca de entrenamiento
      if(nuevo_error != 0):
        # Formula de actualizacion de pesos => pesos[i] = W_i + alpha (tasa de aprendizaje) * error(en el patron) * X_i
        for j in range(len(pesos)):
          pesos[j] = pesos[j] + alpha*nuevo_error*patron[j]
          
        # Llamado recursivo
        pesos, datos_grafica = entrenamiento_normal(entradas,pesos,salidas,errores,epoca)
        return pesos, datos_grafica

  datos_grafica['epoca'].append(epoca)  
  datos_grafica['errores']['patron_1'].append(errores[0])
  datos_grafica['errores']['patron_2'].append(errores[1])
  datos_grafica['errores']['patron_3'].append(errores[2])
  datos_grafica['errores']['patron_4'].append(errores[3])
  datos_grafica['pesos']['w0'].append(pesos[0])
  datos_grafica['pesos']['w1'].append(pesos[1])
  datos_grafica['pesos']['w2'].append(pesos[2])

  return pesos, datos_grafica

# not implemented yet
def entrenamiento_xor(entradas):
  xor = [[0,1,0,0],[0,0,1,0],[0,1,1,0]]
  pesos_finales = []
  datos_grafica = {}
  datos_grafica_final = {}
  for i in range(3):
    errores, pesos, iterador = regenerar_valores()
    pesos, datos_grafica = entrenamiento_normal(entradas,pesos,xor[i],errores,iterador) if i < 2 else entrenamiento_normal([xor[0],xor[1]],pesos,xor[2],errores,iterador)
    pesos_finales.append(pesos)
    datos_grafica_final[f"entramiento{i+1}"] = datos_grafica
  return pesos_finales, datos_grafica_final

def aplicacion_normal(patrones,pesos):

  X_0 = -1
  
  patrones = [[X_0] + patron for patron in patrones]
  
  # Realizando la sumatoria de los pesos por las entradas
  respuestas = []
  salida_obtenidas = []
  for patron in patrones:
    sumatoria = 0
    for k in range(len(pesos)):
      sumatoria += pesos[k]*patron[k]

    # Verificacion de la sumatoria para obtener el resultado
    salida_obtenida = 1 if sumatoria > 0 else 0
    respuesta = f"\n------------------------------------\nPatron {patrones.index(patron) + 1} forma -> [X_0,X_1,X_2] {patron} -> suma {sumatoria} -> salida obtenida es: {salida_obtenida}"
    respuestas.append(respuesta)
    salida_obtenidas.append(salida_obtenida)
  return salida_obtenidas, respuestas


# not implemented yet
def aplicacion_xor(patrones,pesos):
  y_1, _ = aplicacion_normal(patrones,pesos[0])
  y_2, _ = aplicacion_normal(patrones,pesos[1])
  patrones_final = [[y_1[i],y_2[i]] for i in range(len(y_1))]
  resultado_xor, respuestas = aplicacion_normal(patrones_final,pesos[2])
  return resultado_xor, respuestas

# not implemented yet
def graficar_errores_entrenamiento():
  pass

def imprimir_respuestas(respuestas):
  for respuesta in respuestas:
    print(respuesta)
