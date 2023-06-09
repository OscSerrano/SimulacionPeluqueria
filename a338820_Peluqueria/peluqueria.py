
import pygame
import sys
import random
import csv

#Cosas que es mejor no cambiar
ALTO = 600
ANCHO = 800
ESCALA = 60

#Cosas que se pueden cambiar para alterar un poco la simulacion
FPS = 60 #ticks por segundo
VELOCIDAD = 5
SEGUNDOS_ENTRADA_MIN = 1
SEGUNDOS_ENTRADA_MAX = 3
SEGUNDOS_ATENDER_MIN = 3
SEGUNDOS_ATENDER_MAX = 9
MOSTRAR_CLIENTES_FALTANTES = True
REPETIR_AUTOMATICAMENTE = False
PRIMERO_RANDOM_TAMBIEN = False
GUARDAR_EN_SEGUNDOS = True #False guarda ticks de la simulacion
DECIMALES = 3 #Solo afecta si se mide en segundos
#Solo hay que asegurarse de que min es menor o igual a Max, sino ni va a correr.
TICKSXINPUT = 8

#Cosas de prueba, pero ps no hay que cambiarlas porque son muy especificas
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)


class Cliente:
    def __init__(self, x, y):
        #Posicion inicial 
        self.x = x
        self.y = y
        #Velocidad inicial
        self.vel_x = 0
        self.vel_y = 0
        #A donde mira el sujeto
        self.sentido = 2
        #Donde se va a formar y su lugar en la fila
        self.fila = 0
        self.lugar = 0
        self.sentado = False
        self.formado = False
        #El diccionario para guardar los tiempos de todos
        self.tiempos = {'Tiempo de llegada': 0, 'Tiempo en formarse': 0, 'Tiempo formado': 0, 'Tiempo siendo atendido': 0, 'Tiempo de salida': 0, 'Tiempo pasado en la tienda': 0}

        #cosa extra
        self.checkpoint = False
        self.atendido = False
        #dibujitos
        self.imgs_baja = [[],[]] #Sentido 0 "Sur" 
        self.imgs_baja[0].append(pygame.image.load("imgs/cliente1baja1.png"))
        self.imgs_baja[0].append(pygame.image.load("imgs/cliente1baja.png"))
        self.imgs_baja[0].append(pygame.image.load("imgs/cliente1baja2.png"))
        #self.imgs_baja_quieto = pygame.image.load("imgs/cliente1baja.png")
        self.imgs_baja[1].append(pygame.image.load("imgs/cliente1afro_baja1.png"))
        self.imgs_baja[1].append(pygame.image.load("imgs/cliente1afro_baja.png"))
        self.imgs_baja[1].append(pygame.image.load("imgs/cliente1afro_baja2.png"))
        self.imgs_sube = [[],[]] #Sentido 1 "Norte"
        self.imgs_sube[0].append(pygame.image.load("imgs/cliente1sube1.png"))
        self.imgs_sube[0].append(pygame.image.load("imgs/cliente1sube.png"))
        self.imgs_sube[0].append(pygame.image.load("imgs/cliente1sube2.png"))
        #self.imgs_sube_quieto = pygame.image.load("imgs/cliente1sube.png")
        self.imgs_sube[1].append(pygame.image.load("imgs/cliente1afro_sube1.png"))
        self.imgs_sube[1].append(pygame.image.load("imgs/cliente1afro_sube.png"))
        self.imgs_sube[1].append(pygame.image.load("imgs/cliente1afro_sube2.png"))
        self.imgs_der = [[],[]] #Sentido 2 "Este"
        self.imgs_der[0].append(pygame.image.load("imgs/cliente1der1.png"))
        self.imgs_der[0].append(pygame.image.load("imgs/cliente1der.png"))
        self.imgs_der[0].append(pygame.image.load("imgs/cliente1der2.png"))
        #self.imgs_der_quieto = pygame.image.load("imgs/cliente1der.png")
        self.imgs_der[1].append(pygame.image.load("imgs/cliente1afro_der1.png"))
        self.imgs_der[1].append(pygame.image.load("imgs/cliente1afro_der.png"))
        self.imgs_der[1].append(pygame.image.load("imgs/cliente1afro_der2.png"))
        self.imgs_izq = [[],[]] #Sentido 3 "Oeste"
        self.imgs_izq[0].append(pygame.image.load("imgs/cliente1izq1.png"))
        self.imgs_izq[0].append(pygame.image.load("imgs/cliente1izq.png"))
        self.imgs_izq[0].append(pygame.image.load("imgs/cliente1izq2.png"))
        #self.imgs_izq_quieto = pygame.image.load("imgs/cliente1izq.png")
        self.imgs_izq[1].append(pygame.image.load("imgs/cliente1afro_izq1.png"))
        self.imgs_izq[1].append(pygame.image.load("imgs/cliente1afro_izq.png"))
        self.imgs_izq[1].append(pygame.image.load("imgs/cliente1afro_izq2.png"))

        self.img_actual = 0
        self.img = self.imgs_baja[1][1]
        self.img = pygame.transform.scale(self.img, (ESCALA, ESCALA))
        self.rect = pygame.Rect(self.x, self.y, ESCALA, ESCALA)

    def mover(self, direccion):
        #Actualizar velocidad
        if direccion == 0: #abajo
            self.vel_x = 0
            self.vel_y = VELOCIDAD
            self.sentido = 0
        elif direccion == 1: #arriba
            self.vel_x = 0
            self.vel_y = -VELOCIDAD
            self.sentido = 1
        elif direccion == 2: #derecha
            self.vel_x = VELOCIDAD
            self.vel_y = 0
            self.sentido = 2
        elif direccion == 3: #izquierda
            self.vel_x = -VELOCIDAD
            self.vel_y = 0
            self.sentido = 3

        #Actualizar posicion
        self.x += self.vel_x
        self.y += self.vel_y

    def detener(self, tiempo):
        self.vel_x = 0
        self.vel_y = 0
        if not self.formado:
            self.tiempos['Tiempo en formarse'] = tiempo - self.tiempos['Tiempo de llegada']
            self.formado = True

    def mirar(self, direccion):
        self.sentido = direccion

    def dibujar(self, ventana):
        #Hacemos doble comprobacion de donde mira el cliente
        #Luego dependiendo de la velocidad escogemos una animacion
        if self.sentido == 0: #abajjo
            if self.vel_y == 0:
                if self.atendido:
                    self.img = self.imgs_baja[0][1]
                else:
                    self.img = self.imgs_baja[1][1]
            else:
                self.img_actual += 0.1
                if self.img_actual >= len(self.imgs_baja):
                    self.img_actual = 0
                if self.atendido:
                    self.img = self.imgs_baja[0][int(self.img_actual)]
                else:
                    self.img = self.imgs_baja[1][int(self.img_actual)]
        elif self.sentido == 1: #arriba
            if self.vel_y == 0:
                if self.atendido:
                    self.img = self.imgs_sube[0][1]
                else:
                    self.img = self.imgs_sube[1][1]
            else:
                self.img_actual += 0.1
                if self.img_actual >= len(self.imgs_sube):
                    self.img_actual = 0
                if self.atendido:
                    self.img = self.imgs_sube[0][int(self.img_actual)]
                else:
                    self.img = self.imgs_sube[1][int(self.img_actual)]
        elif self.sentido == 2: #derecha
            if self.vel_x == 0:
                if self.atendido:
                    self.img = self.imgs_der[0][1]
                else:
                    self.img = self.imgs_der[1][1]
            else:
                self.img_actual += 0.1
                if self.img_actual >= len(self.imgs_der):
                    self.img_actual = 0
                if self.atendido:
                    self.img = self.imgs_der[0][int(self.img_actual)]
                else:
                    self.img = self.imgs_der[1][int(self.img_actual)]
        elif self.sentido == 3: #izquierda
            if self.vel_x == 0:
                if self.atendido:
                    self.img = self.imgs_izq[0][1]
                else:
                    self.img = self.imgs_izq[1][1]
            else:
                self.img_actual += 0.1
                if self.img_actual >= len(self.imgs_izq):
                    self.img_actual = 0
                if self.atendido:
                    self.img = self.imgs_izq[0][int(self.img_actual)]
                else:
                    self.img = self.imgs_izq[1][int(self.img_actual)]
        
        self.img = pygame.transform.scale(self.img, (ESCALA, ESCALA))
        self.rect = pygame.Rect(self.x, self.y, ESCALA, ESCALA)

        ventana.blit(self.img, self.rect)

    def elegirFila(self, peluqueras):
        #Guardamos la cantidad de gente formada en la primera fila de forma temporal
        filaTemp = peluqueras[0].fila
        filasTemp = []
        #Comparamos con el resto de filas para encontrar la menor cantidad de gente formada por fila
        for peluquera in peluqueras:
            if filaTemp > peluquera.fila:
                filaTemp = peluquera.fila
        #Checamos si hubo varias filas con el mismo numero de clientes formados
        for peluquera in peluqueras:    
            if filaTemp == peluquera.fila:
                filasTemp.append(peluqueras.index(peluquera)) #y lo añadimos a un arreglo
        #De ese arreglo seleccionamos una fila al 'azar'
        self.fila = random.choice(filasTemp)
        self.lugar = filaTemp
        #Esto no hacia falta pero ps aca lo puse y ya me dio hueva moverle aqui y a llegaCliente()
        return self.fila
        
    def formarse(self, peluqueras, tiempo):
        #primera silla 50px, 60px masomenos pa sentarse
        #primera silla 100px, 50px masomenos pa ponerse al lado
        #separacion entre sillas es de 130px aprox
        #0.Abajo, 1.Arriba, 2.Derecha, 3.Izquierda
        for i in range(len(peluqueras)):
            if not self.atendido and not self.sentado:
                #Verificamos que el cliente no haya sido o este siendo atendido
                #Luego movemos por el eje 'x'a los clientes hasta estar en su fila
                #cuando llegan se mueven en el eje 'y' para formarse hasta sentarse
                if self.fila == i:
                    if self.x < 50 + 130*i:
                        self.mover(2)
                    elif self.x > 50 + 130*i:
                        self.mover(3)
                    else:
                        if self.y > 60 + self.lugar*70:
                            self.mover(1)
                        elif self.y < 60 + self.lugar*70:
                            self.mover(0)
                        else:
                            if GUARDAR_EN_SEGUNDOS:
                                tiempo /= FPS
                                tiempo = round(tiempo,DECIMALES)
                            self.detener(tiempo)
                            if self.y == 60:
                                self.mirar(0)
                                self.sentado = True
                                self.tiempos['Tiempo formado'] = tiempo - (self.tiempos['Tiempo en formarse']+self.tiempos['Tiempo de llegada'])
                            else:
                                self.mirar(1)
                    #Por aca abajo decimos que si el cliente ya encontró su fila ya no hace falta checar el resto            
                    break 

    def salir(self, tiempo):
        #Hacemos un movimiento similar al hecho en formarse(), pero ponemos un punto por el que debe pasar
        #para disminuir un poco la superposicion de los clientes a la hora de dirigirse a la salida
        if self.atendido:
            if self.checkpoint:
                if self.x < 0:
                    self.mover(2)
                elif self.x > 0:
                    self.mover(3)
                else:
                    if GUARDAR_EN_SEGUNDOS:
                        tiempo /= FPS
                        tiempo = round(tiempo,DECIMALES)
                    self.tiempos['Tiempo de salida'] = tiempo
                    self.tiempos['Tiempo pasado en la tienda'] = tiempo - self.tiempos['Tiempo de llegada']
                    return True
            else:
                if self.x < 130*self.fila:
                    self.mover(2)
                elif self.x > 130*self.fila:
                    self.mover(3)
                else:
                    #La puerta de salida anda por los 410px en y
                    if self.y > 410:
                        self.mover(1)
                    elif self.y < 410:
                        self.mover(0)
                    else:
                        self.detener(tiempo)
                        self.checkpoint = True
            return False

class Peluquera:
    def __init__(self, x, y):
        #Posicion inicial 
        self.x = x
        self.y = y
        #A donde mira el sujeto
        self.sentido = 0
        #Personas e espera
        self.fila = 0
        #Esta atendiendo y cuanto lleva atendiendo
        self.atendiendo = False
        self.tiempo = 0
        self.ranTiempo = 180
        #dibujitos
        self.imgs_baja = []
        self.imgs_baja.append(pygame.image.load("imgs/peluquera1baja.png"))
        self.imgs_atender = []
        self.imgs_atender.append(pygame.image.load("imgs/peluquera1izq1.png"))
        self.imgs_atender.append(pygame.image.load("imgs/peluquera1izq2.png"))

        self.img_actual = 0
        self.img = self.imgs_baja[self.img_actual]
        self.img = pygame.transform.scale(self.img, (ESCALA, ESCALA))
        self.rect = pygame.Rect(self.x, self.y, ESCALA, ESCALA)

    def mirar(self, direccion):
        self.sentido = direccion

    def dibujar(self, ventana):
        #Podria hacer una animacion para las peluqueras, pero me dio hueva
        #Tambien podria hacer una animacion de 'stand by' para todos los dibujos
        if self.atendiendo:
            self.img_actual += 0.05
            if self.img_actual >= len(self.imgs_atender):
                self.img_actual = 0
            self.img = self.imgs_atender[int(self.img_actual)]
        else:
            self.img_actual += 0.05
            if self.img_actual >= len(self.imgs_baja):
                self.img_actual = 0
            self.img = self.imgs_baja[int(self.img_actual)]

        self.img = pygame.transform.scale(self.img, (ESCALA, ESCALA))
        self.rect = pygame.Rect(self.x, self.y, ESCALA, ESCALA)

        ventana.blit(self.img, self.rect)

    def atender(self, fila, clientes, tiempoTotal):
        for cliente in clientes:
            #Recorremos la lista de clientes y revisamos si esta formado en la fila de la peluquera que pasamos como fila
            #para entenderlo ir a Tienda.actualiza()
            if cliente.fila == fila and cliente.lugar == 0:
                if cliente.sentado:
                    #Si el cliente esta sentado entonces esta siendo atendido
                    if self.tiempo < self.ranTiempo:
                        self.atendiendo = True
                        self.tiempo += 1
                    else:
                        #Cuando el cliente lleva suficiente tiempo en la silla se atiende
                        cliente.atendido = True
                        if GUARDAR_EN_SEGUNDOS:
                            tiempoTotal /= FPS
                            tiempoTotal = round(tiempoTotal,DECIMALES)
                        cliente.tiempos['Tiempo siendo atendido'] = tiempoTotal - (cliente.tiempos['Tiempo de llegada']+cliente.tiempos['Tiempo en formarse']+cliente.tiempos['Tiempo formado'])
                        for cliente in clientes:
                            if cliente.fila == fila:
                                cliente.lugar -= 1
                        #y despues cede su lugar en la fila y deja libre a la peluquera
                        self.fila -= 1
                        self.tiempo = 0
                        self.atendiendo = False
                else:
                    #Si no tiene cliente ps se pone a hacer numeros aleatorios en lo que llega uno
                    self.atendiendo = False
                    self.ranTiempo = random.randint(FPS*SEGUNDOS_ATENDER_MIN, FPS*SEGUNDOS_ATENDER_MAX) #Entre 3 y 9 segundos
                #Si ya encontramos al cliente sentado en la silla no yhace falta revisar al resto
                break
        
class Tienda:
    def __init__(self, ventana):
        #Pasamos la ventana de pygame para poder moverla desde cualquier otra funcion
        self.ventana = ventana
        self.fuente = pygame.font.Font(None, 25)
        #Basicamente aca andan las variables de la simulacion
        self.ejecutando = True
        self.pausado = False
        self.configurando = False
        self.totClientes = 0
        if PRIMERO_RANDOM_TAMBIEN:
            self.ranTiempo = random.randint(FPS*SEGUNDOS_ENTRADA_MIN, FPS*SEGUNDOS_ENTRADA_MAX)
        else:
            self.ranTiempo = 0 
        self.tiempo = 0
        self.tiempoTotal = 0
        self.ultimoInput = 0
        self.clientes = []
        self.peluqueras = []

        #Para inicializar el .csv con sus headers aka por dios que desesperantes titulos de mierda
        try:
            with open('Tiempos_Peluqieria.csv', 'w', newline='') as archivocsv:
                cliente = Cliente(0,0)
                escritor = csv.writer(archivocsv)
                escritor.writerow(cliente.tiempos.keys())
                del cliente
        except IOError:
            print("Parece que no se abrio el .csv y ps ahora no se sobre escribieron los titulos")

        #Mas dibujitos
        self.imgFondo = []
        if MOSTRAR_CLIENTES_FALTANTES:
            self.imgFondo.append(pygame.image.load("imgs/fondo7.jpg"))
        else:
            self.imgFondo.append(pygame.image.load("imgs/fondo6.jpg"))

        self.imgFondo.append(pygame.image.load("imgs/fondoBorroso.jpg"))
        
        self.imgCierres = []
        self.imgCierres.append(pygame.image.load("imgs/Fin5.png"))
        self.imgCierres.append(pygame.image.load("imgs/Fin6.png"))
        self.imgCierres.append(pygame.image.load("imgs/Fin7.png"))

        self.imgInicio = []
        self.imgInicio.append(pygame.image.load("imgs/Inicio1.png"))
        self.imgInicio.append(pygame.image.load("imgs/Inicio2.png"))
        self.imgInicio.append(pygame.image.load("imgs/Inicio3.png"))

        self.imgPausa = []
        self.imgPausa.append(pygame.image.load("imgs/Pausa1.png"))
        self.imgPausa.append(pygame.image.load("imgs/Pausa2.png"))
        self.imgPausa.append(pygame.image.load("imgs/Pausa3.png"))
        self.imgPausa.append(pygame.image.load("imgs/Pausa4.png"))

        self.imgConfig = [[],[],[],[],[],[],[]]
        self.imgConfig[0].append(pygame.image.load("imgs/Config1.png"))
        self.imgConfig[0].append(pygame.image.load("imgs/Config1.1.png"))
        self.imgConfig[1].append(pygame.image.load("imgs/Config2.png"))
        self.imgConfig[1].append(pygame.image.load("imgs/Config2.1.png"))
        self.imgConfig[2].append(pygame.image.load("imgs/Config3.png"))
        self.imgConfig[2].append(pygame.image.load("imgs/Config3.1.png"))
        self.imgConfig[3].append(pygame.image.load("imgs/Config4.png"))
        self.imgConfig[3].append(pygame.image.load("imgs/Config4.1.png"))
        self.imgConfig[3].append(pygame.image.load("imgs/Config4.2.png"))
        self.imgConfig[4].append(pygame.image.load("imgs/Config5.png"))
        self.imgConfig[4].append(pygame.image.load("imgs/Config5.1.png"))
        self.imgConfig[4].append(pygame.image.load("imgs/Config5.2.png"))
        self.imgConfig[5].append(pygame.image.load("imgs/Config6.png"))
        self.imgConfig[5].append(pygame.image.load("imgs/Config6.1.png"))
        self.imgConfig[6].append(pygame.image.load("imgs/Config7.png"))

        
        self.imgMenu_Actual = 0
        self.imgMenu_Actual2 = 0
        self.imgMenu = self.imgInicio[0]
        self.imgMenu = pygame.transform.scale(self.imgMenu, (ANCHO, ALTO))
        self.img = self.imgFondo[0]
        self.img = pygame.transform.scale(self.img, (ANCHO, ALTO))
        self.rect = pygame.Rect(0, 0, ANCHO, ALTO)

    def peluqueros(self, p):
        #primera silla 50px, 60px masomenos pa sentarse
        #primera silla 100px, 50px masomenos pa ponerse al lado
        #separacion de sillas 130px aprocs
        for i in range (p):
            peluquera = Peluquera(95+(i*130),50)
            self.peluqueras.append(peluquera)
        
    def llegaCliente(self, numClientes):
        #Revisamos si ya llegaron todos los clientes 
        if self.totClientes < numClientes:
            #Luego con ayuda de un numero random elegimos su aparicion entre 1 y 3 segundos entre cada uno
            if self.tiempo >= self.ranTiempo:
                #la puerta anda masomenos por 350px (en y)
                #al chile si deberia moverla un poco mas arriba, pero ps x
                cliente = Cliente(0,350)
                #Metemos el tiempo de llegada
                if GUARDAR_EN_SEGUNDOS:
                    cliente.tiempos['Tiempo de llegada'] = round(self.tiempoTotal/FPS,DECIMALES)
                else:
                    cliente.tiempos['Tiempo de llegada'] = self.tiempoTotal
                fila = cliente.elegirFila(self.peluqueras) 
                self.peluqueras[fila].fila += 1
                self.clientes.append(cliente) #pum cliente agregado a la lista de clientes
                self.tiempo = 0
                self.ranTiempo = random.randint(FPS*SEGUNDOS_ENTRADA_MIN, FPS*SEGUNDOS_ENTRADA_MAX) #este random 
                self.totClientes += 1
            else:
                #aca anda la cuenta de tiempo
                self.tiempo += 1
        if MOSTRAR_CLIENTES_FALTANTES and (self.clientes or self.totClientes < numClientes):
            texto = self.fuente.render("x"+str(numClientes-self.totClientes), 0, VERDE)
            texto_rect = texto.get_rect(center=(27, 586))
            self.ventana.blit(texto, texto_rect)

    def cierre(self, key):
        if REPETIR_AUTOMATICAMENTE:
            #Al tener activada la repeticion automatica, regresamos a 0 las variables de la simulacion
            self.img = self.imgFondo[0]
            self.totClientes = 0
            #Se puede hacer que el primer morro llegue en tiempo random tambien asi
            if PRIMERO_RANDOM_TAMBIEN:
                self.ranTiempo = random.randint(FPS*SEGUNDOS_ENTRADA_MIN, FPS*SEGUNDOS_ENTRADA_MAX)
            else:
                self.ranTiempo = 0
            self.tiempo = 0
            self.tiempoTotal = 0
        else:
            #Aca tenemos unos dibujitos para cuando el ultimo cliente sale de la peluqueria y 'termina la simulacion'. 
            #Metí un boton de reset y otra forma de cerrar el programa
            if self.ultimoInput > TICKSXINPUT:
                self.ultimoInput = 0
                if key[pygame.K_UP]:
                    self.ultimoInput = 0
                    if self.imgMenu_Actual > 0:
                        self.imgMenu_Actual -= 1
                    else:
                        self.imgMenu_Actual = 2
                elif key[pygame.K_DOWN]:
                    self.ultimoInput = 0
                    if self.imgMenu_Actual < 2:
                        self.imgMenu_Actual += 1
                    else:
                        self.imgMenu_Actual = 0
                elif key[pygame.K_KP_ENTER] or key[pygame.K_SPACE] or key[pygame.K_RETURN]:
                    self.ultimoInput = 0
                    if self.imgMenu_Actual == 0:
                        self.img = self.imgFondo[0]
                        self.totClientes = 0
                        if PRIMERO_RANDOM_TAMBIEN:
                            self.ranTiempo = random.randint(FPS*SEGUNDOS_ENTRADA_MIN, FPS*SEGUNDOS_ENTRADA_MAX)
                        else:
                            self.ranTiempo = 0
                        self.tiempo = 0
                        self.tiempoTotal = 0
                    elif self.imgMenu_Actual == 1:
                        self.configurando = True
                        self.imgMenu_Actual = 0
                        self.imgMenu_Actual2 = 0
                    elif self.imgMenu_Actual == 2:
                        self.ejecutando = False
                elif key[pygame.K_r]:
                    #Para los 'Resets' volvemos a inicializar las variables de la simulacion en 0 
                    self.img = self.imgFondo[0]
                    self.ultimoInput = 0
                    self.totClientes = 0
                    if PRIMERO_RANDOM_TAMBIEN:
                        self.ranTiempo = random.randint(FPS*SEGUNDOS_ENTRADA_MIN, FPS*SEGUNDOS_ENTRADA_MAX)
                    else:
                        self.ranTiempo = 0
                    self.tiempo = 0
                    self.tiempoTotal = 0
                    self.imgMenu_Actual = 0
                elif key[pygame.K_c]:
                    self.ultimoInput = 0
                    self.configurando = True
                    self.imgMenu_Actual = 0
                    self.imgMenu_Actual2 = 0
            else:
                self.ultimoInput += 1
            
            self.imgMenu = self.imgCierres[self.imgMenu_Actual]
            self.imgMenu = pygame.transform.scale(self.imgMenu, (ANCHO, ALTO))
            self.rect = pygame.Rect(0, 0, ANCHO, ALTO)
            self.ventana.blit(self.imgMenu, self.rect)

    def pausa(self, key):
        if self.ultimoInput > TICKSXINPUT:
            if key[pygame.K_UP]:
                self.ultimoInput = 0
                if self.imgMenu_Actual > 0:
                    self.imgMenu_Actual -= 1
                else:
                    self.imgMenu_Actual = 3
            elif key[pygame.K_DOWN]:
                self.ultimoInput = 0
                if self.imgMenu_Actual < 3:
                    self.imgMenu_Actual += 1
                else:
                    self.imgMenu_Actual = 0
            elif key[pygame.K_KP_ENTER] or key[pygame.K_SPACE] or key[pygame.K_RETURN]:
                self.ultimoInput = 0
                if self.imgMenu_Actual == 0:
                    #Salir del modo pausa
                    self.img = self.imgFondo[0]
                    self.pausado = False
                elif self.imgMenu_Actual == 1:
                    self.clientes.clear()
                    self.peluqueras.clear()
                    self.totClientes = 0
                    if PRIMERO_RANDOM_TAMBIEN:
                        self.ranTiempo = random.randint(FPS*SEGUNDOS_ENTRADA_MIN, FPS*SEGUNDOS_ENTRADA_MAX)
                    else:
                        self.ranTiempo = 0
                    self.tiempo = 0
                    self.tiempoTotal = 0
                    self.img = self.imgFondo[0]
                    self.pausado = False
                elif self.imgMenu_Actual == 2:
                    self.configurando = True
                    self.imgMenu_Actual = 0
                    self.imgMenu_Actual2 = 0
                elif self.imgMenu_Actual == 3:
                    self.ejecutando = False
                self.imgMenu_Actual = 0
                self.imgMenu_Actual2 = 0
            elif key[pygame.K_p]:
                #Salir del modo pausa
                self.ultimoInput = 0
                self.img = self.imgFondo[0]
                self.pausado = False
                self.imgMenu_Actual = 0
            elif key[pygame.K_r]:
                #Para los 'Resets' volvemos a inicializar las variables de la simulacion en 0 
                self.clientes.clear()
                self.peluqueras.clear()
                self.ultimoInput = 0
                self.totClientes = 0
                if PRIMERO_RANDOM_TAMBIEN:
                    self.ranTiempo = random.randint(FPS*SEGUNDOS_ENTRADA_MIN, FPS*SEGUNDOS_ENTRADA_MAX)
                else:
                    self.ranTiempo = 0
                self.tiempo = 0
                self.tiempoTotal = 0
                self.imgMenu_Actual = 0
                self.img = self.imgFondo[0]
                self.pausado = False
                self.imgMenu_Actual = 0
            elif key[pygame.K_c]:
                self.ultimoInput = 0
                self.configurando = True
                self.imgMenu_Actual = 0
                self.imgMenu_Actual2 = 0

        else:
            self.ultimoInput += 1

        self.imgMenu = self.imgPausa[self.imgMenu_Actual]
        self.imgMenu = pygame.transform.scale(self.imgMenu, (ANCHO, ALTO))
        self.rect = pygame.Rect(0, 0, ANCHO, ALTO)
        self.ventana.blit(self.imgMenu, self.rect)

    def configurar(self, key):
        if self.ultimoInput > TICKSXINPUT:
            if self.imgMenu_Actual2 == 0:
                if key[pygame.K_UP]:
                    self.ultimoInput = 0
                    if self.imgMenu_Actual > 0:
                        self.imgMenu_Actual -= 1
                    else:
                        self.imgMenu_Actual = 6
                elif key[pygame.K_DOWN]:
                    self.ultimoInput = 0
                    if self.imgMenu_Actual < 6:
                        self.imgMenu_Actual += 1
                    else:
                        self.imgMenu_Actual = 0
            if key[pygame.K_KP_ENTER] or key[pygame.K_SPACE] or key[pygame.K_RETURN]:
                self.ultimoInput = 0
                if self.imgMenu_Actual == 6:
                    self.ultimoInput = 0
                    self.configurando = False
                    self.imgMenu_Actual = 0
                    self.imgMenu_Actual2 = 0
                else:
                    print("pa despues")
            elif key[pygame.K_c]:
                self.ultimoInput = 0
                self.configurando = False
                self.imgMenu_Actual = 0
                self.imgMenu_Actual2 = 0

        else:
            self.ultimoInput += 1

        self.imgMenu = self.imgConfig[self.imgMenu_Actual][self.imgMenu_Actual2]
        self.imgMenu = pygame.transform.scale(self.imgMenu, (ANCHO, ALTO))
        self.rect = pygame.Rect(0, 0, ANCHO, ALTO)
        self.ventana.blit(self.imgMenu, self.rect)

    def actualiza(self, key, numPeluqueros, numClientes):
        #Reset del fondo de pantalla (el mapa)
        self.ventana.blit(self.img, self.rect)
        if len(self.peluqueras) < numPeluqueros:
            self.peluqueras.clear()
            self.peluqueros(numPeluqueros)
        if self.pausado and not self.configurando:
            self.pausa(key)
        elif self.configurando:
            self.configurar(key)
        else:
            if self.ultimoInput > TICKSXINPUT:
                #Le picas a la p para pausar, que original por dios
                if key[pygame.K_p]:
                    self.img = self.imgFondo[1]
                    self.pausado = True
                    self.ultimoInput = 0
            else:
                self.ultimoInput += 1

            #Llegada medio random de clientes
            self.llegaCliente(numClientes)
            
            #Cuando el arreglo de clientes este vacio se termina el programa
            if self.clientes or self.totClientes < numClientes:
                #Dibujamos a las peluqueras y les apuramos para que atiendan todo lo atendible
                for peluquera in self.peluqueras:
                    peluquera.dibujar(self.ventana)
                    peluquera.atender(self.peluqueras.index(peluquera), self.clientes, self.tiempoTotal)
                #Dibujamos a los clientes y les apuramos a formarse con su peluquera
                for cliente in self.clientes:
                    cliente.dibujar(self.ventana)
                    cliente.formarse(self.peluqueras, self.tiempoTotal)
                    if cliente.salir(self.tiempoTotal):
                        #Cuando el cliente llega a la salida, lo borramos de la existencia, pero antes guardamos sus datos
                        try:
                            with open('Tiempos_Peluqieria.csv', 'a', newline='') as archivocsv:
                                escritor = csv.DictWriter(archivocsv, fieldnames=cliente.tiempos.keys())
                                escritor.writerow(cliente.tiempos)
                        except IOError:
                            print("La neta, no se pero ps no se abrio el .csv y ps ahora no se guardaron los datos del morro que acaba de salir")
                        self.clientes.remove(cliente)
                #Vamos contando los ticks de la simulacion
                self.tiempoTotal += 1
            else:
                self.img = self.imgFondo[1]
                self.cierre(key)
                #FIN

def main():
    #Inicializacion de la ventana con pygame 
    pygame.init()
    ventana = pygame.display.set_mode((ANCHO,ALTO))
    pygame.display.set_caption("Simulacion Peluqueria")

    #Leemos los argumentos en linea de comandos
    try:
        numPeluqueros = int(sys.argv[1])
        numClientes = int(sys.argv[2])
    except Exception as e:
        numPeluqueros = 0
        numClientes = 0
        print(e)
    #y damos error si no se mete algo adecuado 
    if 0 < numPeluqueros <= 6 and 0 < numClientes <= 30:
        #Instanciamos el loocal, ponemos los peluqueros de una e inicializamos key pa evitar errores 
        tienda = Tienda(ventana)
        key = pygame.key.get_pressed()

        while tienda.ejecutando:
            #Se comprueban los fpss
            pygame.time.Clock().tick(FPS)

            #Comprobar si se cierra el programa y vemos si se presionan teclas
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    tienda.ejecutando = False
                key = pygame.key.get_pressed()
                if key[pygame.K_ESCAPE]:
                    tienda.ejecutando = False

            #Actualizar estado de la tienda
            tienda.actualiza(key, numPeluqueros, numClientes)

            #Se dibujan las cosas
            pygame.display.flip()
    else:
        print("Debes ingresar el numero de peluqueros y clientes (maximo 6 y 30 respectivamente)")

    #Parar los procesos de pygame
    pygame.quit()


if __name__ == "__main__":
    main()
