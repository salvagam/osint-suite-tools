#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
Copyright (c) 2019, QuantiKa14 Servicios Integrales S.L
All rights reserved.
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 
1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.
'''

#AUTHOR: JORGE WEBSEC
#Twitter: @JorgeWebsec
#WEB: www.quantika14.com

import wikipedia, requests, json, re
from bs4 import BeautifulSoup

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

#Funciones para buscar en BORME
def parserLibreborme_json(j):
    print "|----[INFO][CARGOS EN EMPRESAS ACTUALMENTE][>] "
    for cargos_actuales in j["cargos_actuales"]:
        print "    - Desde: " + cargos_actuales["date_from"] + " hasta la actualidad."
        print "    - Empresa: " + cargos_actuales["name"]
        print "    - Cargo: " + cargos_actuales["title"]

    print "|----[INFO][CARGOS EN EMPRESAS HISTORICOS][>] "
    for cargos_historicos in j["cargos_historial"]:
        print "    - Desde: " + cargos_historial["date_from"]
        print "    - Hasta: " + cargos_historial["date_to"]
        print "    - Empresa: " + cargos_historial["name"]
        print "    - Cargo: " + cargos_historial["title"]
    
    print "|----[FUENTES][BORME][>] "
    for boe in j["in_bormes"]:
        print "    - CVE: " + boe["cve"]
        print "    - URL: " + boe["url"]

def searchLibreborme(apellidos, nombre):
    URL = "https://libreborme.net/borme/api/v1/persona/" + apellidos.replace(" ", "-") + "-" + nombre.replace(" ", "-") + "/"
    html = requests.get(URL)
    if html > 10:
        try:
            
            j = json.loads(html.text)
            parserLibreborme_json(j)
        
        except:
            print "[!][WARNING][LIBREBORME][>] Error con la API..."
    elif html < 10:
        URL = "https://libreborme.net/borme/api/v1/persona/" + nombre.replace(" ", "-") + "-" + apellidos.replace(" ", "-") + "/"
        html = requests.get(URL)
        try:
            j = json.loads(html.text)
            parserLibreborme_json(j)

        except:
            print "[!][WARNING][LIBREBORME][>] Error con la API..."
    else:
        print "|----[INFO][EMPRESAS][>] No aparecen resultados en el BORME."

#Funciones para buscar en Wikipedia
def searchWikipedia(target):

    try:
        wikipedia.set_lang("es")
        d0 = wikipedia.search(target)

        if d0:
            print "|----[INFO][WIKIPEDIA][>] "
            print "     |----[INFO][SEARCH][>] "
            print "     - Resultados encontrados: "
            for r in d0:
                print "     - " + r
        else:
            print "|----[INFO][WIKIPEDIA][>] No aparecen resultados en WIKIPEDIA."

    except:
        print "[!][WARNING][WIKIPEDIA][>] Error en la API..."

    try:
        d1 = wikipedia.page(target)

        linksWIKI = d1.links
        urlWIKI = d1.url

        if d1:
            print "     |----[INFO][TAGS][>] "
            for l in linksWIKI:
                print "     - " + l
            print "|----[FUENTES][WIKIPEDIA][>] "
            print "     - " + urlWIKI
        else:
            print "|----[INFO][WIKIPEDIA][>] No aparecen resultados en WIKIPEDIA."
    
    except:
        print "[!][WARNING][WIKIPEDIA][>] Error en la API o no aparecen resultados..."

#Funciones para buscar en Youtube
def searchYoutube(target):
    URL = "https://www.youtube.com/results?search_query="
    html = requests.get(URL + target).text

    soup = BeautifulSoup(html, "html.parser")
    vids = soup.findAll('a',attrs={'class':'yt-uix-tile-link'})
    vids_titles = soup.findAll("div", attrs={'class', 'style-scope ytd-video-renderer'})

    videolist=[]

    for v in vids:
        tmp = 'https://www.youtube.com' + v['href']
        videolist.append(tmp)
    
    print "|----[INFO][YOUTUBE][>] "
    for v in vids_titles:
        print "     - " + v
        print html
    print "|----[FUENTES][YOUTUBE][>] "
    for u in videolist:
        print "     - " + u

#Funciones para buscar en las Páginas Amarillas
def cleanPaginasAmarillas_result(r):
    r_array = r.split("Ver mapa")

    r2_array = r_array[0].split("Imprimir Ficha")
    r = r2_array[2].split()

    return r

def searchPaginasAmarillas(nombre, a1, a2, loc):
    url = "http://blancas.paginasamarillas.es/jsp/resultados.jsp?no=" + nombre + "&ap1=" + a1 + "&ap2=" + a2 + "&sec=41&pgpv=1&tbus=0&nomprov=" + loc + "&idioma=spa"

    html = requests.get(url).text

    soup = BeautifulSoup(html, "html.parser")
    r = soup.find("div", attrs={'class': 'resul yellad yellad_ad0'})
    r = remove_tags(str(r))

    if not r == "None":
        print "|----[INFO][PAGINAS AMARILLAS][>] "
        print "     - " + str(cleanPaginasAmarillas_result(r))
    else:
        pass


def banner():
    print """
                                                                                                        
                             -:--:::-...-::---..` `                                                 
                           `+s+so+++/++:---:::--:::::-::------..```                                 
                           +dhsdho+/+/::://:::----/:++o/-----....--:-.                              
                          -NNNNmdsdo+s/://:::::/-::y/://--:-.....-.--::.                            
                          yNhyNMmdd++y://:/::::::::---::-/:::---.--.--::-`                          
                          yh//hNNmhssy:/s+:/+/++/+++/////:+/:::-....-----.`                         
                           .` :-/+ooso++o++ooososysoooo+://oso/::------.-.-`                        
                                    `-``` ./oshhysssssssoooo++:::/:::----.-.                        
                                              smhyoos++++sssso//------:+---.                        
                                             `yNmdyo+oo+:.oyhysys+::--..---.                        
    OSINT PARA TODOS                          +NNNmhso+/:-``+dmdhyho+:-:---:.`                       
                                            .NNNNmyo/-``   `ymmdhyys+++::--..                       
        E                                   hNmNmho/`       /NNmdhhms+oo-.....                      
                                           +Nmdddh+`      ` .NNmdmNo/o/+:----:                      
            INVESTIGA CONMIGO...          .Nmmddhs-        `:NNNNd/:+++o+/:---                      
                                         .dmmmdho/.       :+dMNsso+/+++o+++:--`                     
                                        :mmmdhyo/`     `+dNNdsys/+++/+/+/o+/--`                     
                                       oNmddhs+:.-.  `+mNNNy+o++////////+++/:-                      
                                     -ydhhyss++hdho-+dNNNh++o+///::////+++///.                      
                                   .ydhyssooosmmmddmmNNds++++/:::://////++++/.                      
                                  yddysso+ooydmmdhhmNms+++:`/yoo+/////++/+++:.                      
                                  sdhss++shhdhyhhymmy+++:`  .mhyso++///+////--.                     
                                  mmhss+hhmdhsshmmyoo/.      ymdhyyo+///+++/:---`                   
                                  hNmdhhmdmdyydmy+o/.        -mddhhys+//o++//--:--`                 
                                   /mMMNmdmNmdyo+:`           +ddddhyo//ooo+:--:::--.`              
                                     :+syhhyo/:.               odddhhs+/+sso+:.:::::::-.`         """
    print "-----------------------------------------------------------------------------------------------"
    print "DANTE'S GATES MINIMAL v 1.0 | <<TIP-1337>> | Gorgue de Triana | QUANTIKA14 | @JORGEWEBSEC"
    print "     VERSION: 1.0 | 09/02/2019 | INVESTIGA CONMIGO DESDE EL SU | WWW.QUANTIKA14.COM "

def menu():
    print ""
    print "-----------------------------------------------------------------------------------------------"
    print "Dante's Gates Minimal Version es un buscador inteligente para hacer OSINT de forma automática."
    print "Toda la información es siempre de fuentes abiertas y siempre se dará la dirección de las fuentes"
    print ""
    print "________________________________________"
    print "| 1. Nombre y apellidos                |"
    print "| 2. Nombre, apellidos y ciudad        |"
    print "|______________________________________|"
    m = int(raw_input("Selecciona 1/2: "))
    if m == 1:
        nombre = raw_input("Por favor indique el nombre: ")
        apellido1 = raw_input("Por favor indique el primer apellido: ")
        apellido2 = raw_input("Por favor indique el segundo apellido: ")
        target = nombre + " " + apellido1 + " " + apellido2
        apellidos = apellido1 + " " + apellido2

        searchWikipedia(target)
        searchLibreborme(apellidos, nombre)
        searchYoutube(target)

    if m == 2:
        nombre = raw_input("Por favor indique el nombre: ")
        apellido1 = raw_input("Por favor indique el primer apellido: ")
        apellido2 = raw_input("Por favor indique el segundo apellido: ")
        loc = raw_input("Por favor indique la ciudad: ")
        target = nombre + " " + apellido1 + " " + apellido2
        apellidos = apellido1 + " " + apellido2
        
        searchWikipedia(target)
        searchLibreborme(apellidos, nombre)
        searchYoutube(target)
        searchPaginasAmarillas(nombre, apellido1, apellido2, loc)

def main():
    banner()
    menu()
    

main()
