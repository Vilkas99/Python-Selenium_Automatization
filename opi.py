import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
# Using Chrome to access web
driver = webdriver.Chrome()

#Valores:
usuario = ""
contra = ""


#Administrador de folders
#Directorio donde se encuentran las tareas
directorio_subir = 'C:/Users/victo/Desktop/tareas_completadas'
#Generamos una lista del mismo
lista_directorio = list(os.listdir(directorio_subir))
print(lista_directorio)

#Tupla con la cantidad de materias (En este caso, 2)
tupla_filas = [[], []]

n = 0
#Ciclo que añade los folders y sus archivos en cada espacio de las tuplas
for directorio in lista_directorio:
    lista_archivos = list(os.listdir(os.path.join(directorio_subir, directorio)))
    if(len(lista_archivos) != 0):
        tupla_filas[n] = (directorio, lista_archivos[0])
        n = n+1


#Funcion que se encarga de subir el archivo (Toma como argumento el numero del folder)
def subirArchivo(folderNum):
    #Obtenemos el nombre del folder
    print("ENTRANDO NENES")
    #Obtenemos el folders
    folder = tupla_filas[folderNum][0]
    #Obtenemos el archivo
    archivo = tupla_filas[folderNum][1]


    #Buscamos la tabla de materias
    courses_button = driver.find_element_by_id('global_nav_courses_link')
    #Se le da click
    courses_button.click()

    #Se esperan 3 segundos
    driver.implicitly_wait(3);

    #Si el folder tiene el nombre...
    if(folder == 'MA1029.1'):
        #Se encuentra a su materia correspondiente
        clase_seleccionada = driver.find_element_by_link_text("Modelación matemática intermedia (Gpo 1)");

    #Same
    elif(folder == 'EC1020.1'):
        clase_seleccionada = driver.find_element_by_link_text("Micro incentivos económicos y macro resultados (Gpo 1)")

    #Se le da click a la materia selecconada
    clase_seleccionada.click()

    #Esperamos 2 segundos...
    driver.implicitly_wait(2)
    #Encontramos el apartado de las tareas por hacer
    elementos_porHacer = driver.find_elements_by_class_name("cjUyb_bGBk.cjUyb_doqw.cjUyb_fNIu.cjUyb_eQnG")
    #Establecemos una bandera que nos indicará si ya hemos encontraado el apartado de la tarea
    encontrado = False
    #Por cada tarea por hacer...
    for elemento in elementos_porHacer:
        #Antes que nada, verificaremos que no hayamos encontrado la tarea...
        if(encontrado == True):
            #De ser así, nos salimos del cilco (No tiene caso seguir buscando si ya la encontramos)
            break

        #Si no ha sido encontrada, entonces verificaremos que el nombre del archivo y de la tarea sean los mismos
        if(elemento.text.lower() in archivo.lower()):
            #Obtenemos la URL de la página
            url1 = driver.current_url
            #Realizamos una secuencia de comados, en donde nos desplazamos a la tarea, y le hacemos click.
            ActionChains(driver).move_to_element(elemento).click().perform()
            #Verificamos que nos encontramos en otra página
            if(driver.current_url != url1):
                #Encontramos el boton de entregar tarea
                boton_entregar = driver.find_element_by_class_name("assignment-buttons")
                #Le damos click
                boton_entregar.click()
                #Encontramos el espacio para subir el archivo
                archivo_Subir = driver.find_element_by_name('attachments[0][uploaded_data]')
                #Obtenemos la ubicación del archivo a subir
                archivo_ubicacion = os.path.join(directorio_subir, folder, archivo)
                #Añadimos el archivo al apartado
                archivo_Subir.send_keys(archivo_ubicacion)

                #Encontramos el boton para subirlo
                submit_assignment = driver.find_element_by_id('submit_file_button')
                #Hacemos click en el archivo
                submit_assignent.click()

                print("Se ha cargado el archivo")
                #Establecemos que ya hemos encontrado el archivo.
                encontrado = True;
            else:
                print("Tienes que esperar")
                ## TODO: Arreglar el problema con el ciclo, no encuentra el DOM después de la primera corrida
    print("HEMOS LLEGADO AL FINAL")




#Ingresamos a la página de Tec
driver.get('https://experiencia21.tec.mx/')

#Busamos el username
id_box = driver.find_element_by_id('userNameInput')
#Añadimos al usuario
id_box.send_keys(usuario)

#Añadimos la contraseña
contra_box = driver.find_element_by_id('passwordInput')
contra_box.send_keys(contra)

#Ingresamos
boton_input = driver.find_element_by_id("submitButton")
boton_input.click()



#Creamos un ciclo que suba todos los archivos
for n in range(len(tupla_filas)):
    subirArchivo(n)

#Al final, llegamos a la zona de victoria.
driver.get('https://www.youtube.com/watch?v=04854XqcfCY')
