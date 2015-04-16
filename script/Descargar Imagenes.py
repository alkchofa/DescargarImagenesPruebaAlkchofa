#############################################################
## Autor: Cantarell Maximiliano				#####
## Version: 1.0 					#####
## Descripcion: Descargar imagenes de un sitio web 	#####
#############################################################

import urllib
import os
from bs4 import BeautifulSoup

urlInicial=input("Url: ")

class DownloaderImages:        
    def __init__(self,url):
        self.url = url
        self.sizeOk = (10)*1024                  #Si la imagen pesa menos de eso (Kbytes*1024) se elimina
        self.soup   =  BeautifulSoup (urllib.urlopen(url)) 
        self.a      =  self.soup.find_all("img")
        self.path   =  os.getcwd() + '\\' + url[7:]    #String que contiene la direccion y le agrega el dominio de la pagina
        self.echo =True

        if not os.path.exists(self.path):
            os.makedirs(self.path )
        else:
            self.echo = False

    def extraerImagenes(self):
        if self.echo:
            archivoConDireccionesDeImagenes= open(self.path + "\\Imagenes.txt", "wb")
            print "Van a descargarse " + str(len (self.a)) + " imagenes."
            for i in range (len (self.a) ):

                nombreDeImagen= self.a[i].attrs['src']
                if nombreDeImagen[0]=='/':
                    nombreDeImagen = self.url + nombreDeImagen[1:]

                try:
                    nombreImagen = (self.path + '\\' + 'Imagen(' + str(i)+').jpg')
                    self.fichero = file (nombreImagen,"wb")
                    self.fichero.write(urllib.urlopen(nombreDeImagen).read())
                    self.fichero.close()
                    
                    if self.sizeOk > os.stat(nombreImagen).st_size:             #Si el archivo pesa menos de lo especificado arriba lo elimina 
                        os.remove(nombreImagen)
                        print "Imagen ("+str(i)+") eliminada por tamaño insuficiente."
                    
                    print "(" + str(i+1) + ")" + " Imagen descargada con exito."
                except:
                    print "(" + str(i+1) + ")" + "Error en descargar imagen."
                    archivoConDireccionesDeImagenes.write( nombreDeImagen+'\n' )
                    archivoConDireccionesDeImagenes.flush()

            archivoConDireccionesDeImagenes.close()

class RecolectorDeLinksClase:
    def __init__(self,nombreArchivoDeTexto,primerURL):
        self.url    = primerURL
        self.path   =  os.getcwd() + '\\' + nombreArchivoDeTexto
        self.soup   = BeautifulSoup (urllib.urlopen(primerURL))
        self.links  = self.soup.find_all("a")

    def criteriosParaGuardarLink(self,link):
        if link[:7] != 'http://':
            return False
        if link[-4:] == '.jpg' or link[-4:] == '.png':
            return False
        return True
                
    
    def recolectarLinks(self):
        archivoDeTextoConLinks = open (self.path,"a")
        for i in range (len (self.links)):
            if self.links[i].has_attr('href'):
                nombreLink = self.links[i].attrs['href']
                if nombreLink != "":
                    if nombreLink[0] == '/':
                        nombreLink = self.url + nombreLink[1:]
                    if self.criteriosParaGuardarLink(nombreLink):
                        archivoDeTextoConLinks.write(nombreLink+'\n')
                        archivoDeTextoConLinks.flush()
        archivoDeTextoConLinks.close()

def ponerHTTPsiNoLoTiene(url):
       if url[0:7] != 'http://':
           return  'http://' + url
       else:
           return url

class Spider:
    def __init__(self,url,nombreArchivo):
        self.url=url
        self.NombreTxt = nombreArchivo

    def SurfearTelaSpider(self):
        DownloaderImages(self.url).extraerImagenes()
        RecolectorDeLinksClase (self.NombreTxt,self.url).recolectarLinks()
        
        for j in range(1000000):
            archivos = open (self.NombreTxt,'r')
            self.linea=''
            for i in range(j):
                self.linea=archivos.readline()
            archivos.close()
            if self.linea != '':
                DownloaderImages(self.linea).extraerImagenes()
                RecolectorDeLinksClase (self.NombreTxt,self.linea).recolectarLinks()


#Procesa el link para agregar el 'http://' si es que no la tiene
url = ponerHTTPsiNoLoTiene(urlInicial)

#Spider(url,"Links.txt").SurfearTelaSpider()


#Descarga las imagenes del link que le pasan
downloader = DownloaderImages(url)
downloader.extraerImagenes()


#Crea una clase para recopilar links
link = RecolectorDeLinksClase ("Links.txt",url)
link.recolectarLinks()
