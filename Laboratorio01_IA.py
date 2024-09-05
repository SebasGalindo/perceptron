import random

def generar_pesos():
  return [round(random.random(),2) for i in range(3)]

def regenerar_valores():
  errores = [random.randint(1,5) for i in range(4)]
  pesos = generar_pesos()
  iterador = 0
  return errores, pesos, iterador

def entrenamiento_normal(entradas,pesos,salidas,errores,epoca):
  # Calculando el numero de patrones que se tienen
  num_patrones = len(entradas[0])
  

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
        pesos = entrenamiento_normal(entradas,pesos,salidas,errores,epoca)
        return pesos
    
  return pesos

# not implemented yet
def entrenamiento_xor(entradas):
  xor = [[0,1,0,0],[0,0,1,0],[0,1,1,0]]
  pesos_finales = []
  for i in range(3):
    errores, pesos, iterador = regenerar_valores()
    pesos = entrenamiento_normal(entradas,pesos,xor[i],errores,iterador) if i < 2 else entrenamiento_normal([xor[0],xor[1]],pesos,xor[2],errores,iterador)
    pesos_finales.append(pesos)
  return pesos_finales

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

if __name__ == "__main__":

  # Definicion de las entradas
  entradas = [[0,1,0,1],[0,0,1,1]]
  # Definicion del bias
  X_0 = -1
  # Definicion de la tasa de aprendizaje
  alpha = 0.5
  # Definicion de las salidas [OR, AND, NAND]
  salidas = [[0,1,1,1],[0,0,0,1],[1,1,1,0]]
  
  # Generando los valores iniciales para OR
  errores, pesos, iterador = regenerar_valores()
  print(f"Proceso de entrenamiento para la logica OR")
  pesos_OR = entrenamiento_normal(entradas,pesos,salidas[0],errores,iterador)

  # Generando los valores iniciales para AND
  errores, pesos, iterador = regenerar_valores()
  print(f"Proceso de entrenamiento para la logica AND")
  pesos_AND = entrenamiento_normal(entradas,pesos,salidas[1],errores,iterador)

  # Generando los valores iniciales para NAND
  errores, pesos, iterador = regenerar_valores()
  print(f"Proceso de entrenamiento para la logica NAND")
  pesos_NAND = entrenamiento_normal(entradas,pesos,salidas[2],errores,iterador)  

  ## Generando los valores iniciales para XOR
  print(f"Proceso de entrenamiento para la logica XOR")
  pesos_XOR = entrenamiento_xor(entradas)

  print("------------------------------------ \n")
  print(f"Los pesos finales para la logica OR son: {pesos_OR}")
  print(f"Los pesos finales para la logica AND son: {pesos_AND}")
  print(f"Los pesos finales para la logica NAND son: {pesos_NAND}")
  print(f"Los pesos finales para la logica XOR son: {pesos_XOR}")

  opcion = 0
  menu = """
          1. Probar la solucion de la logica OR
          2. Probar la solucion de la logica AND
          3. Probar la solucion de la logica NAND
          4. Probar la solucion de la logica XOR
          5. Salir
  """

  while opcion != 5:

    # Se Guardan los valores de la forma [X_1, X_2] para cada patron es decir [[X_1],[X_2],etc] 
    patrones = []

    opcion = int(input(menu))
    if opcion > 0 and opcion < 5:
      # numero_entradas = int(input("Ingrese el numero de entradas: ")) # not implemented yet because it is fixed to 2
      numero_patrones = int(input("Ingrese el numero de patrones: "))
      for i in range(numero_patrones):
        print(f"Patron # {i+1}")
        # patrones.append([int(input(f"Ingrese la entrada # {j+1} ")) for j in range(numero_entradas)]) # not implemented yet because it is fixed to 2
        patron = ([int(input(f"Ingrese la entrada # {j+1} ")) for j in range(2)])
        patrones.append(patron)


    if opcion == 1:
      _ , respuestas = aplicacion_normal(patrones,pesos_OR)
      imprimir_respuestas(respuestas)
    elif opcion == 2:
      _ , respuestas = aplicacion_normal(patrones,pesos_AND)
      imprimir_respuestas(respuestas)
    elif opcion == 3:
      _ , respuestas = aplicacion_normal(patrones,pesos_NAND)
      imprimir_respuestas(respuestas)
    elif opcion == 4:
      _ , respuestas = aplicacion_xor(patrones,pesos_XOR)
      imprimir_respuestas(respuestas)
