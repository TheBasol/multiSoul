import pytube
from os import remove
import moviepy.editor as mp
import urllib.request
from lxml import etree
import re
from pathlib import Path
import argparse

parser = argparse.ArgumentParser(description= 'V - Descargar video.\n' +
                                              "A - Descargar y convertir video a mp3. \n" +
                                              "S - Busqueda y descarga de videos. \n" +
                                              "info - informacion del video.\n" +
                                              "Si se quiere descargar en la ruta actual solo ponga unas comillas vacias ' ' ")
parser.add_argument("-opc", dest="opc", help="Opcion a realizar")
parser.add_argument("-url", dest="url", help="url del video")
parser.add_argument("-search", dest="search", help="Video a buscar y descargar")
parser.add_argument("-path", dest="path", help="Ruta en donde se va a descargar el contenido")                    

params = parser.parse_args()

def videosDownload(url,path): 
    yt = pytube.YouTube(url)
    print("¡¡Descargando!!")
    yt.streams.first().download(path)


def videosToMusic(url,path):
    yt = pytube.YouTube(url)
    print("¡¡Descargando!!")
    yt.streams.first().download(path)
    
    name = str(path)+ "/" + yt.title + ".mp4" 

    try:
        clip = mp.VideoFileClip(name)
        clip.audio.write_audiofile(str(path) + "/" + yt.title + ".mp3", bitrate="320k")
        remove(name)
    except:
        remove(name)
        print("Error en crear el archivo mp3")
        exit()

    



def info(url):
    yt = pytube.YouTube(url)
    print("Titulo .........: " + yt.title)
    print("Duracion (seg)..: " + str(yt.length))
    print("Descripcion.....: " +  yt.description)


def busqueda(search_keyword,path):

    search_keyword = search_keyword.replace(" ", "") 

    print("Buscando...")

    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    video_ids = video_ids[0:20]

    num=[]
    linksVideo = []
    video_title = []

    for links in range(len(video_ids)):#
        youtube = etree.HTML(urllib.request.urlopen("https://www.youtube.com/watch?v=" + video_ids[links]).read()) 
        linksVideo.append("https://www.youtube.com/watch?v=" + video_ids[links])
        video_title.append(youtube.xpath('//meta[@name="title"]/@content'))


    for x in range(len(video_ids)):#
        num.append(str(x+1))

    videos = dict(zip(num,video_title)) 
    numVideosLinks = dict(zip(num,linksVideo))
 
    for video in videos:
        print(str(video) + " : " + str(videos[video]))

    opcLink = str(input('¿Cual de todos Quieres descargar?\n'))
    opcVideo = str((input('¿En que formato lo Quieres descargar?\n'+
                       '1 = mp4\n'+
                       '2 = mp3\n')))

    if opcVideo == "1":
        videosDownload(numVideosLinks[opcLink],path)
    elif opcVideo == "2":
        videosToMusic(numVideosLinks[opcLink],path)
    


if __name__ == "__main__":
    if params.opc == "V":
        if (params.path).strip() == "":
            ruta = Path("").resolve()
            videosDownload(params.url,ruta)
        else:
            videosDownload(params.url,params.path)
    elif params.opc == "A":
        if (params.path).strip() == "":
            ruta = Path("").resolve()
            videosToMusic(params.url,ruta)
        else:
            videosToMusic(params.url,params.path)
    elif params.opc == "S":
        search = (params.search).strip()

        if (params.path).strip() == "":     
            ruta = Path("").resolve()
            busqueda(search,ruta)
        else:
            busqueda(search,params.path)    
    elif params.opc == "info":
        info(params.url)

    print('listo!!!')