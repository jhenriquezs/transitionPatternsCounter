import json


# funcion que traduce el patron, para ejemplificar en formato tikz.
# input: (patron).
# patron: lista de 12 elementos con valores 1 y 0.
# output: retorna un string que ejemplifica el patron que se desea mostrar.
def face_templates(array):
    faces = {}
    faces["front"] = array[0:4]
    faces["left"] = [array[6],array[0],array[4],array[2]]
    faces["right"] = [array[1],array[7],array[3],array[5]]
    faces["top"] = array[2:6]
    faces["back"] = [array[6],array[7],array[4],array[5]]
    faces["bottom"] = [array[6],array[7],array[0],array[1]]
    cube = """\draw[thick,fill=gray!20](3,3,0)--(0,3,0)--(0,3,3)--(3,3,3)--(3,3,0)--(3,0,0)--(3,0,3)--(0,0,3)--(0,3,3);
    \draw[thick](3,3,3)--(3,0,3);
    \draw[fill=gray!20](0,3,0)--(3,3,0)--(3,3,3)--(0,3,3)--(0,3,0);
    \draw[thick, densely dashed](3,0,0)--(0,0,0)--(0,3,0);
    \draw[thick, densely dashed](0,0,0)--(0,0,3);
"""
    for k,v in faces.items():
        nodos = v.count(1)
        if (nodos == 1):
            final_result = []
            # arreglos con las coordenadas base para el patron de 1 vertice
            infIzq = [[0,1,0],[1,1,0],[1,0,0], [1,1,0],[3,3,0]]
            infDer = [[2, 0, 0], [2, 1, 0], [3, 1, 0], [2, 1, 0], [0, 3, 0]]
            supIzq = [[0, 2, 0], [1, 2, 0], [1, 3, 0], [1, 2, 0], [3, 0, 0]]
            supDer = [[2, 3, 0], [2, 2, 0], [3, 2, 0], [0, 0, 0], [2, 2, 0]]
            if (v[0]==1):
                if(k=="top"):
                    final_result = terdimension(k,supIzq)
                elif(k=="right"):
                    final_result = terdimension(k,infDer)
                else:
                    final_result = terdimension(k, infIzq)
            elif (v[1]==1):
                if(k=="top"):
                    final_result = terdimension(k,supDer)
                elif(k=="right"):
                    final_result = terdimension(k,infIzq)
                else:
                    final_result = terdimension(k, infDer)
            elif (v[3]==1):
                if(k=="top"):
                    final_result = terdimension(k,infDer)
                elif(k=="right"):
                    final_result = terdimension(k,supIzq)
                else:
                    final_result = terdimension(k, supDer)
            else:
                if (k == "top"):
                    final_result = terdimension(k, infIzq)
                elif (k == "right"):
                    final_result = terdimension(k, supDer)
                else:
                    final_result = terdimension(k, supIzq)
            cube = translateUnNod(cube,final_result,k)
        elif (nodos == 2 and (v[1] != v[2])):
            arreglonodos=[]
            # arreglos con las coordenadas base para la plantilla de 1 arista
            dosNabajo = [[1, 0, 0], [1, 2, 0], [2, 2, 0], [2, 0, 0], [0, 3, 0], [1, 2, 0], [3, 3, 0], [2, 2, 0], [0,1,0],[3,1,0]]
            dosNderecha = [[3, 1, 0], [1, 1, 0], [1, 2, 0], [3, 2, 0], [0, 0, 0], [1, 1, 0], [0, 3, 0], [1, 2, 0],[2,0,0],[2,3,0]]
            dosNarriba = [[1, 3, 0], [1, 1, 0], [2, 1, 0], [2, 3, 0], [0, 0, 0], [1, 1, 0], [3, 0, 0], [2, 1, 0], [0,2,0],[3,2,0]]
            dosNizquierda = [[0, 2, 0], [2, 2, 0], [2, 1, 0], [0, 1, 0], [2, 2, 0], [3, 3, 0], [2, 1, 0], [3, 0, 0], [1,0,0],[1,3,0]]
            if(v[0]==v[1] and v[0]==1):
                arreglonodos=terdimension(k,dosNabajo)
            elif(v[1]==v[3] and v[3]==1):
                if (k == "right"):
                    arreglonodos = terdimension(k, dosNizquierda)
                else:
                    arreglonodos=terdimension(k,dosNderecha)
            elif(v[3]==v[2] and v[2]==1):
                if (k== "top"):
                    arreglonodos = terdimension(k, dosNabajo)
                else:
                    arreglonodos=terdimension(k,dosNarriba)
            else:
                arreglonodos=terdimension(k,dosNizquierda)
            cube = translateDosNod(cube,arreglonodos,k)
        elif (nodos == 2 and (v[1] == v[2])):
            result = []
            # arreglos con las coordenadas base para la plantilla de vertices opuestos.
            infIzqSupDer = [[1, 0, 0], [1, 2, 0], [3, 2, 0], [0, 1, 0], [2, 1, 0],[2,3,0],[0,3,0],[1,2,0],[3,0,0],[2,1,0]]
            infDerSupIzq = [[1, 3, 0], [1, 1, 0], [3, 1, 0], [0, 2, 0], [2, 2, 0],[2,0,0],[0,0,0],[1,1,0],[3,3,0],[2,2,0]]

            if (v[0] == 1):
                if(k=="right" or k=="top"):
                    result = terdimension(k,infDerSupIzq)
                else:
                    result = terdimension(k,infIzqSupDer)
            else:
                if(k=="top" or k=="right"):
                    result = terdimension(k,infIzqSupDer)
                else:
                    result = terdimension(k,infDerSupIzq)
            # en caso de querer generar 2b de la primera version de schneider
            # primer_b = [[0, 1.5, 0], [3, 1.5, 0], [1.5, 0, 0], [1.5, 3, 0]]
            # result = terdimension(k,primer_b)
            cube = translateDosB_Nod(cube,result,k)
        elif (nodos == 3):
            arreglo=[]
            # arreglos con las coordenadas base para la plantilla de aristas adyacentes.
            infIzq = [[0, 0, 0], [1, 1, 0], [3, 1, 0], [1, 1, 0], [1, 3, 0],[0,2,0],[3,2,0],[2,3,0],[2,0,0]]
            infDer = [[3, 0, 0], [2, 1, 0], [0, 1, 0], [2, 1, 0], [2, 3, 0],[1,0,0],[1,3,0],[0,2,0],[3,2,0]]
            supIzq = [[0, 3, 0], [1, 2, 0], [3, 2, 0], [1, 2, 0], [1, 0, 0],[0,1,0],[3,1,0],[2,3,0],[2,0,0]]
            supDer = [[0, 2, 0], [2, 2, 0], [3, 3, 0], [1, 3, 0], [1, 0, 0],[2,2,0],[2,0,0],[0,1,0],[3,1,0]]
            if(v[0]==v[1]==v[3]):
                if (k == "top"):
                    arreglo = terdimension(k, infIzq)
                elif (k == "right"):
                    arreglo = terdimension(k, supDer)
                else:
                    arreglo = terdimension(k, supIzq)
            elif(v[1]==v[3]==v[2]):
                if (k == "top"):
                    arreglo = terdimension(k, supIzq)
                elif (k == "right"):
                    arreglo = terdimension(k, infDer)
                else:
                    arreglo = terdimension(k, infIzq)
            elif(v[3]==v[2]==v[0]):
                if (k == "top"):
                    arreglo = terdimension(k, supDer)
                elif (k == "right"):
                    arreglo = terdimension(k, infIzq)
                else:
                    arreglo = terdimension(k, infDer)
            elif(v[2]==v[0]==v[1]):
                if (k == "top"):
                    arreglo = terdimension(k, infDer)
                elif (k == "right"):
                    arreglo = terdimension(k, supIzq)
                else:
                    arreglo = terdimension(k, supDer)
            cube = translateTresNod(cube,arreglo,k)
        elif (nodos == 4):
            # arreglos con las coordenadas base para la plantilla de 1 cara.
            arre = terdimension(k,[[0,1,0],[3,1,0], [0,2,0],[3,2,0], [1,0,0],[1,3,0], [2,0,0],[2,3,0]])
            cube = translateCuatroNod(cube,arre,k)
    return cube

# funcion que redimensiona las coordenadas segun la posicion que representan
# input: (posicion, cara).
# posicion: posicion que representa la cara dentro en el cubo.
# cara: lista de x elementos que contiene las coordenadas para ejemplificar dicho patron.
# output: retorna un string que ejemplifica la cara en formato tikz.
def terdimension(posicion,array):
    if (posicion == "front"):
        for i in range(len(array)):
            array[i][2] += 3
    elif(posicion == "bottom" or posicion == "top"):
        for i in range(len(array)):
            array[i][2], array[i][1] = array[i][1], array[i][2]
            if (posicion == "top"):
                array[i][1] +=3
    elif(posicion == "left" or posicion == "right"):
        for i in range(len(array)):
            array[i][2], array[i][0] = array[i][0], array[i][2]
            if (posicion == "right"):
                array[i][0] += 3
    return array

# funcion que actualiza el string global con la informacion para representar dicha cara como tikz.
# input: (string,coordenadas,posicion).
# string: string global que se escribira en el documento para reproducir el patron en formato tikz.
# coordenadas: lista de x elementos que contiene las coordenadas para ejemplificar dicho la cara de dicho patron.
# posicion: posicion que representa la cara dentro en el cubo.
# output: retorna un string que ejemplifica la cara de 1 vertice en formato tikz.

def translateUnNod(cube,array,k):
    options = "line width=0.4mm"
    if (k in ["left","back","bottom"] ):
        options = "line width=0.4mm,gray,densely dashed"
    primera_linea = str(tuple(array[0])) + "--" + str(tuple(array[1])) + "--" + str(tuple(array[2])) + ";"
    segunda_linea = str(tuple(array[3])) + "--" + str(tuple(array[4])) + ";"
    cube += """\draw["""+options+"""]""" + primera_linea + """
        \draw["""+options+"""]""" + segunda_linea + """
        """
    return cube

# funcion que actualiza el string global con la informacion para representar dicha cara como tikz.
# input: (string,coordenadas,posicion).
# string: string global que se escribira en el documento para reproducir el patron en formato tikz.
# coordenadas: lista de x elementos que contiene las coordenadas para ejemplificar dicho la cara de dicho patron.
# posicion: posicion que representa la cara dentro en el cubo.
# output: retorna un string que ejemplifica la cara de una arista en formato tikz.
def translateDosNod(cube,array,k):
    options = "line width=0.4mm"
    if (k in ["left", "back","bottom"]):
        options = "line width=0.4mm,gray,densely dashed"
    primera_linea = str(tuple(array[0]))+"--"+str(tuple(array[1]))+"--"+str(tuple(array[2]))+"--"+str(tuple(array[3]))+";"
    segunda_linea = str(tuple(array[4]))+"--"+str(tuple(array[5]))+";"
    tercera_linea = str(tuple(array[6]))+"--"+str(tuple(array[7]))+";"
    cuarta_linea = str(tuple(array[8])) + "--" + str(tuple(array[9])) + ";"
    cube += """\draw["""+options+"""]"""+ primera_linea +"""
    \draw["""+options+"""]"""+segunda_linea+"""
    \draw["""+options+"""]"""+tercera_linea+"""
    \draw["""+options+"""]"""+cuarta_linea+"""
    """
    return cube

# funcion que actualiza el string global con la informacion para representar dicha cara como tikz.
# input: (string,coordenadas,posicion).
# string: string global que se escribira en el documento para reproducir el patron en formato tikz.
# coordenadas: lista de x elementos que contiene las coordenadas para ejemplificar dicho la cara de dicho patron.
# posicion: posicion que representa la cara dentro en el cubo.
# output: retorna un string que ejemplifica la cara de vertices opuestos en formato tikz.
def translateDosB_Nod(cube,array,k):
    options = "line width=0.4mm"
    if (k in ["left", "back","bottom"]):
        options = "line width=0.4mm,gray,densely dashed"
    primera_linea = str(tuple(array[0])) + "--" + str(tuple(array[1])) + "--" + str(tuple(array[2])) + ";"
    segunda_linea = str(tuple(array[3])) + "--" + str(tuple(array[4])) + "--" + str(tuple(array[5])) + ";"
    tercera_linea = str(tuple(array[6])) + "--" + str(tuple(array[7])) + ";"
    cuarta_linea = str(tuple(array[8])) + "--" + str(tuple(array[9])) + ";"
    cube += """\draw["""+options+"""]""" + primera_linea + """
        \draw["""+options+"""]""" + segunda_linea + """
        \draw["""+options+"""]""" + tercera_linea + """
        \draw["""+options+"""]""" + cuarta_linea + """
        """
    return cube

# misma funcion que la de arriba pero para la primera version de schneider en el patron 2b
# def translateDosB_Nod(cube,array,k):
#     options = "line width=0.4mm"
#     if (k in ["left", "back","bottom"]):
#         options = "line width=0.4mm,gray,densely dashed"
#     primera_linea = str(tuple(array[0])) + "--" + str(tuple(array[1])) + ";"
#     segunda_linea = str(tuple(array[2])) + "--" + str(tuple(array[3])) + ";"
#     cube += """\draw["""+options+"""]""" + primera_linea + """
#         \draw["""+options+"""]""" + segunda_linea + """
#         """
#     return cube


# funcion que actualiza el string global con la informacion para representar dicha cara como tikz.
# input: (string,coordenadas,posicion).
# string: string global que se escribira en el documento para reproducir el patron en formato tikz.
# coordenadas: lista de x elementos que contiene las coordenadas para ejemplificar dicho la cara de dicho patron.
# posicion: posicion que representa la cara dentro en el cubo.
# output: retorna un string que ejemplifica la cara de aristas adyacentes en formato tikz.
def translateTresNod(cube,arreglo,k):
    options = "line width=0.4mm"
    if (k in ["left", "back","bottom"]):
        options = "line width=0.4mm,gray,densely dashed"
    primera_linea = str(tuple(arreglo[0])) + "--" + str(tuple(arreglo[1])) + "--" + str(tuple(arreglo[2])) + ";"
    segunda_linea = str(tuple(arreglo[3])) + "--" + str(tuple(arreglo[4])) + ";"
    tercera_linea = str(tuple(arreglo[5])) + "--" + str(tuple(arreglo[6])) + ";"
    cuarta_linea = str(tuple(arreglo[7])) + "--" + str(tuple(arreglo[8])) + ";"
    cube += """\draw["""+options+"""]"""+ primera_linea +"""
    \draw["""+options+"""]"""+segunda_linea+"""
    \draw["""+options+"""]"""+tercera_linea+"""
    \draw["""+options+"""]"""+cuarta_linea+"""
    """
    return cube

# funcion que actualiza el string global con la informacion para representar dicha cara como tikz.
# input: (string,coordenadas,posicion).
# string: string global que se escribira en el documento para reproducir el patron en formato tikz.
# coordenadas: lista de x elementos que contiene las coordenadas para ejemplificar dicho la cara de dicho patron.
# posicion: posicion que representa la cara dentro en el cubo.
# output: retorna un string que ejemplifica la cara de 4 aristas en formato tikz.
def translateCuatroNod(cube,array,k):
    options = "line width=0.4mm"
    if (k in ["left", "back","bottom"]):
        options = "line width=0.4mm,gray,densely dashed"
    primera_linea = str(tuple(array[0]))+"--"+str(tuple(array[1]))+";"
    segunda_linea = str(tuple(array[2]))+"--"+str(tuple(array[3]))+";"
    tercera_linea = str(tuple(array[4]))+"--"+str(tuple(array[5]))+";"
    cuarta_linea = str(tuple(array[6])) + "--" + str(tuple(array[7])) + ";"
    cube += """\draw["""+options+"""]"""+ primera_linea +"""
    \draw["""+options+"""]"""+segunda_linea+"""
    \draw["""+options+"""]"""+tercera_linea+"""
    \draw["""+options+"""]"""+cuarta_linea+"""
    """
    return cube

if __name__ == '__main__':
    # se abren los patrones obtenidos en schneider.py
    with open('schneider_patterns.json') as json_file:
        data = json.load(json_file)
    
    file1 = open("Patrones_schneider_carasnodos_b.txt","w")
    cont = 1
    for cubos in data:
        inicio_string = """{\Large{Patron """+str(cont)+"""}}
    \par
    \\begin{minipage}{.45\linewidth}
        \\textbf{Nodos:}
        """+str(cubos[1])+"""\par"""
        file1.write(inicio_string)
        for num in cubos[0]:
            if(num == "2 nodos"):
                file1.write("\\textbf{Arista (2 nodos)}\par\n")
            elif(num=="3 nodos"):
                file1.write("\\textbf{Aristas adyacentes (3 nodos)}\par\n")
            elif(num=="4 nodos"):
                file1.write("\\textbf{Cara (4 nodos)}\par\n")
            elif(num=="1 nodos"):
                file1.write("\\textbf{Vertice (1 nodo)}\par\n")
            elif(num=="2b nodos"):
                file1.write("\\textbf{Vertices opuestos (2 nodos)}\par\n")
        mid_string = """
        \end{minipage}\hfill
    \\begin{minipage}{.45\linewidth}
        \\begin{tikzpicture}
    """
        file1.write(mid_string)
        string = face_templates(cubos[1])
        # file1.write("Patron "+str(cont)+" cubo: "+str(cubos[1])+"\n ")
        file1.write(string)
        cont+=1
        end_string = """
        \end{tikzpicture}
        \end{minipage}
        \par
        
    """
        file1.write(end_string)
    file1.close()
