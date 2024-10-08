from pprint import pprint
import requests
import urllib.parse
from colorama import Style
import PySimpleGUI as sg
import os, fnmatch
import html
import re
import tkinter as tk
from tkinter import Canvas, Listbox
from time import sleep, strftime, gmtime
import sys
from pygame import mixer
from pathlib import Path
import librosa
import asyncio

mixer.init()



BACKGROUND_COLOR = '#2a2a2a'
TEXT_COLOR = '#ffffff'
INPUT_BACKGROUND = '#181818'
MULTILINE_BACKGROUND = '#494949'
SCROLLBAR_COLOR = '#3E4451'
OPTION_COLOR = "#cecece"

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS  # Temporary folder for PyInstaller
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path).replace("\\", "/")

sings_dir = resource_path('sings')
data_dir = resource_path('data')

def getPath():
    with open(f"{data_dir}/path", "r") as f:
        res = f.readline()
        return res

def writePath(path):
    with open(f"{data_dir}/path", "w") as f:
        f.write(path)

def check_file_exists(file_path):
    return Path(file_path).exists()

def remove_ansi_escape_codes(text):
    ansi_escape = re.compile(r'\x1b\[.*?m')
    return ansi_escape.sub('', text)

def decode_escape_sequences(s):
    def replace_hex(match):
        hex_value = match.group(1)
        return chr(int(hex_value, 16)) 
    
    return re.sub(r'\\x([0-9A-Fa-f]{2})', replace_hex, s)

def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [x1+radius, y1,
              x1+radius, y1,
              x2-radius, y1,
              x2-radius, y1,
              x2, y1,
              x2, y1+radius,
              x2, y1+radius,
              x2, y2-radius,
              x2, y2-radius,
              x2, y2,
              x2-radius, y2,
              x2-radius, y2,
              x1+radius, y2,
              x1+radius, y2,
              x1, y2,
              x1, y2-radius,
              x1, y2-radius,
              x1, y1+radius,
              x1, y1+radius,
              x1, y1]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def capitalize_first_letter_inside_parentheses(text):
    def replacer(match):
        inside_parentheses = match.group(1)
        capitalized = inside_parentheses.title()
        return f"({capitalized})"  

    pattern = r'\(([^)]+)\)'
    
    result = re.sub(pattern, replacer, text)
    
    return result

def internet_connection():
    try:
        response = requests.get("https://youtube.com", timeout=2)
        return True
    except :
        return False  
    
def underline_text_between_underscores(text):
    if text == "":
        return [{"text":text, "italic":False, "bold":False, "color":False}]
    parts = re.split(r'(__)', text)  
    notShown = False
    if text.startswith(" #"):
        notShown = True
    
    row = []

    # INVENTED => ORANGE
    # NORMAL => BOLD
    # NOT SHOWN => NORMAL
    
    invented = False  
    
    for i in range(len(parts)):
        if parts[i] == '__':
            invented = not invented 
        elif parts[i] == "" or parts[i] == " ":
            pass
        else:
            if notShown :
                if i == 0:

                    row.append({"text":parts[i][2:], "italic":True, "bold":False, "color":False})
                else:

                        row.append({"text":parts[i], "italic":True, "bold":False, "color":False})
            else:

                if invented:
                    row.append({"text":parts[i], "italic":False, "bold":True, "color":True})
                else:
                    row.append({"text":parts[i], "italic":False, "bold":True, "color":False})
    if row == []:
        row = [{'text': ' ', 'italic': False, 'bold': False, 'color': False}]
    return row

def upper_after_apostrophe(s):
    result = []
    capitalize_next = False
    
    for i in range(len(s)):
        char = s[i]
        if capitalize_next and char.isalpha():
            result.append(char.upper())
            capitalize_next = False
        else:
            capitalize_next = False
            result.append(char)
        
        if char == "'":
            capitalize_next = True

    return s
    return ''.join(result)

def getLyrics(title):
    global lien
    global titre
    chanson = upper_after_apostrophe(capitalize_first_letter_inside_parentheses(title.replace(" ", "_")[0].upper() + title.replace(" ", "_").replace("?", "%3F")[1:]))
    titre = chanson
    url = "https://n-oubliez-pas-les-paroles.fandom.com/fr/wiki/" + chanson
    lien = url


    reponse = requests.get(url)
    paroles = reponse.text.split("""<li>(x 2) en fin de ligne&#160;: la ligne doit être répétée 2 fois</li></ul>
</div>""")[1].split("""</p><p><br />
</p>
<h2><span class="mw-headline" id="Dates_de_sortie">Dates de sortie</span>""")[0].replace("</b>","").replace("<b>","").replace("</p>","").replace("<p>","").replace("<br />","").replace("</i>",Style.RESET_ALL).replace("<i>","#").replace("(", "\x1B[3m" + Style.DIM).replace(")", Style.RESET_ALL).replace('<span style="color:#E67E30">', "__").replace("</span>", "__")

    parolesSplit = paroles.split("\n")



    for i in range(len(parolesSplit)):
        for j in range(10):
            if "(x {number})".format(number=j) in parolesSplit[i]:
                if not "[(x {number})".format(number=j) in parolesSplit[i]:

                    for k in range(j+1):

                        parolesSplit.insert(i+1, str(j-k+1) + "x " + parolesSplit[i].split("(x {number})".format(number=j))[0])  
                    del parolesSplit[i]
    newParoles = ""
    

    for i in range(len(parolesSplit)):
        if i == 0:
            newParoles += remove_ansi_escape_codes(parolesSplit[i])
        else:
            newParoles += remove_ansi_escape_codes("\n {line}".format(line=parolesSplit[i]))
    return newParoles

def getLyricsFromlink(link):
    global lien
    url = link
    lien = url


    reponse = requests.get(url)
    try:
        paroles = reponse.text.split("""<li>(x2) en fin de ligne&#160;: la ligne doit être répétée 2 fois</li></ul>""")[1].split("""</p><p><br />
    </p>
    <h2><span class="mw-headline" id="Dates_de_sortie">Dates de sortie</span>""")[0].replace("</b>","").replace("<b>","").replace("</p>","").replace("<p>","").replace("<br />","").replace("</i>",Style.RESET_ALL).replace("<i>","#").replace("(", "\x1B[3m" + Style.DIM).replace(")", Style.RESET_ALL).replace('<span style="color:#E67E30">', "__").replace("</span>", "__")
    except:
        paroles = reponse.text.split("""<li>(x 2) en fin de ligne&#160;: la ligne doit être répétée 2 fois</li></ul>""")[1].split("""</p><p><br />
    </p>
    <h2><span class="mw-headline" id="Dates_de_sortie">Dates de sortie</span>""")[0].replace("</b>","").replace("<b>","").replace("</p>","").replace("<p>","").replace("<br />","").replace("</i>",Style.RESET_ALL).replace("<i>","#").replace("(", "\x1B[3m" + Style.DIM).replace(")", Style.RESET_ALL).replace('<span style="color:#E67E30">', "__").replace("</span>", "__")
    parolesSplit = paroles.split("\n")



    for i in range(len(parolesSplit)):
        for j in range(10):
            if "(x {number})".format(number=j) in parolesSplit[i]:
                if not "[(x {number})".format(number=j) in parolesSplit[i]:

                    for k in range(j+1):

                        parolesSplit.insert(i+1, str(j-k+1) + "x " + parolesSplit[i].split("(x {number})".format(number=j))[0])  
                    del parolesSplit[i]
    newParoles = ""
    

    for i in range(len(parolesSplit)):
        if i == 0:
            newParoles += remove_ansi_escape_codes(parolesSplit[i])
        else:
            newParoles += remove_ansi_escape_codes("\n {line}".format(line=parolesSplit[i]))
    return newParoles

def getSings(part):

    if part == 1:
        url = "https://n-oubliez-pas-les-paroles.fandom.com/fr/wiki/Liste_des_chansons_existantes_(de_la_lettre_A_%C3%A0_la_lettre_M)"
        reponse = requests.get(url)
        paroles = reponse.text.split("""<h2><span class="mw-headline" id="Chiffre"><big><b>Chiffre</b></big></span></h2>
<h3><span class="mw-headline" id="113"><b>113</b></span></h3>""")[1].split("""<p><br /><a href="/fr/wiki/Listes_des_chansons_existantes_(de_la_lettre_N_%C3%A0_la_lettre_Z)" class="mw-redirect" title="Listes des chansons existantes (de la lettre N à la lettre Z)"><b>Pour aller à la liste des chansons existantes de N à Z</b></a>
</p></div>""")[0]
    elif part == 2:
        url = "https://n-oubliez-pas-les-paroles.fandom.com/fr/wiki/Listes_des_chansons_existantes_(de_la_lettre_N_%C3%A0_la_lettre_Z)"
        reponse = requests.get(url)
        paroles = reponse.text.split("""<h2><span class="mw-headline" id="N"><b><big>N</big></b></span></h2>
<h3><span class="mw-headline" id="Nacash"><b>Nacash</b></span></h3>""")[1].split("""<p><br />
<b><a href="/fr/wiki/Liste_des_chansons_existantes_(de_la_lettre_A_%C3%A0_la_lettre_M)" title="Liste des chansons existantes (de la lettre A à la lettre M)">Pour revenir à la liste des chansons existantes de A à M</a></b>
</p>""")[0]
    else:
        raise ValueError("Invalid input. Please enter either 1 or 2.")



    parolesSplit = paroles.split("\n")
    result = []
    for i in range(len(parolesSplit)):
        if not parolesSplit[i] == "" and "href=" in parolesSplit[i]:
            res = html.unescape(parolesSplit[i].split('title="')[1].split('">')[0].lower())
            if not res == "liste des chansons existantes (de la lettre a à la lettre m)":
                result.append(res)

    return result

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name).split("\\")[1].split(".txt")[0].replace("%2F", "/").replace("%3F", "?"))
    return result

def chunk_text(text, chunk_size=5):
    
    result = []

    for _ in range(7):
        index = 0
        for i in range(len(text)):
            if i == chunk_size:
                break
            if not isinstance(text[i], list):

                if text[i]["text"] == " " and i > index:
                    index = i
        custom = False
        if index == 0:
            custom = False
            notFound = chunk_size
            
            while index == 0:
                # print("----")
                # print(len(text))
                notFound += 1
                if len(text) > 0:
                    
                    for i in range(len(text)):
                        # print(text[i][0])
                        if 0 == len(text):
                            # print("text finish")
                            index = i
                            break

                        # if i == notFound:
                        #     break
                        if not isinstance(text[i], list):
                            if text[i]["text"] == " " and i > index:
                                index = int(i/2)
                                custom = True
                                break
                    # input()
                else:
                    index = 999
                    # print(result)
        if index != 999:
            if not custom :
                result.append([t for t in text[:index]])
                text = text[index+1:]
            else:
                result.append([t for t in text[:index]])
                text = text[index:]
        
    removed = 0
    for i in range(len(result)):
        if result[i] == []:
            removed += 1
            i = i -1
    for _ in range(removed):
        result.remove([])

    return result

def update_lyrics_window(window, lyrics, chunk_index, size):
    
    for i in range(size):
        currentChunk = lyrics[chunk_index]
        for j in range(5):
            window["-LYR " + str(i) + f"#{j+1}-"].update("", font=('Helvetica', 12 ), text_color=OPTION_COLOR)
        if i+1 > len(currentChunk):
            for j in range(5):
                window["-LYR " + str(i) + f"#{j+1}-"].update(" ")
        else:
            line = currentChunk[i]
            

            if not isinstance(line, list):
                bold = line["bold"]
                italic = line["italic"]
                colored = line["color"]
                text = line["text"]

                if italic:
                    if bold:
                        if colored:
                            window["-LYR " + str(i) + "#1-"].update(text, font=('Helvetica', 12, 'bold italic'), text_color="Orange")
                        else:
                            window["-LYR " + str(i) + "#1-"].update(text, font=('Helvetica', 12, 'bold italic'), text_color=OPTION_COLOR)
                    else:
                        if colored:
                            window["-LYR " + str(i) + "#1-"].update(text, font=('Helvetica', 12, 'italic'), text_color="Orange")
                        else:
                            window["-LYR " + str(i) + "#1-"].update(text, font=('Helvetica', 12, 'italic'), text_color=OPTION_COLOR)
                else:
                    if bold:
                        if colored:
                            window["-LYR " + str(i) + "#1-"].update(text, font=('Helvetica', 12, 'bold'), text_color="Orange")
                        else:
                            window["-LYR " + str(i) + "#1-"].update(text, font=('Helvetica', 12, 'bold'), text_color=OPTION_COLOR)
                    else:
                        if colored:
                            window["-LYR " + str(i) + "#1-"].update(text, font=('Helvetica', 12), text_color="Orange")
                        else:
                            window["-LYR " + str(i) + "#1-"].update(text, font=('Helvetica', 12), text_color=OPTION_COLOR)
                
            else:
                for k in range(len(line)):
                    subline = line[k]
                    bold = subline["bold"]
                    italic = subline["italic"]
                    colored = subline["color"]
                    text = subline["text"]

                    if italic:
                        if bold:
                            if colored:
                                window["-LYR " + str(i) + f"#{k+1}-"].update(text, font=('Helvetica', 12, 'bold italic'), text_color="Orange")
                            else:
                                window["-LYR " + str(i) + f"#{k+1}-"].update(text, font=('Helvetica', 12, 'bold italic'), text_color=OPTION_COLOR)
                        else:
                            if colored:
                                window["-LYR " + str(i) + f"#{k+1}-"].update(text, font=('Helvetica', 12, 'italic'), text_color="Orange")
                            else:
                                window["-LYR " + str(i) + f"#{k+1}-"].update(text, font=('Helvetica', 12, 'italic'), text_color=OPTION_COLOR)
                    else:
                        if bold:
                            if colored:
                                window["-LYR " + str(i) + f"#{k+1}-"].update(text, font=('Helvetica', 12, 'bold'), text_color="Orange")
                            else:
                                window["-LYR " + str(i) + f"#{k+1}-"].update(text, font=('Helvetica', 12, 'bold'), text_color=OPTION_COLOR)
                        else:
                            if colored:
                                window["-LYR " + str(i) + f"#{k+1}-"].update(text, font=('Helvetica', 12), text_color="Orange")
                            else:
                                window["-LYR " + str(i) + f"#{k+1}-"].update(text, font=('Helvetica', 12), text_color=OPTION_COLOR)

def legendWindow():

    
    infos_column = [
        [sg.Column([
        [sg.Text("gras", font=('Helvetica', 11, 'bold'), background_color=BACKGROUND_COLOR, size=(None,1))],
        [sg.Text("texte montré à l'écran ", font=('Helvetica', 10, 'bold'), background_color=BACKGROUND_COLOR, size=(None,1))],
        [sg.Text(" ", background_color=BACKGROUND_COLOR, size=(None,1))],
        [sg.Text("italic", font=('Helvetica', 11, "italic"), background_color=BACKGROUND_COLOR, size=(None,1))],
        [sg.Text("texte pas montré à l'écran mais présent dans la version du chanteur", font=('Helvetica', 10, "italic"), background_color=BACKGROUND_COLOR, size=(None,1))],
        [sg.Text(" ", background_color=BACKGROUND_COLOR, size=(None,1))],
        [sg.Text("orange", font=('Helvetica', 11, "bold"), text_color="Orange", background_color=BACKGROUND_COLOR, size=(None,1))],
        [sg.Text("texte de NOPLP n'existant pas dans la version du chanteur ", font=('Helvetica', 10, "bold"), text_color="Orange", background_color=BACKGROUND_COLOR, size=(None,1))],
        [sg.Text(" ", background_color=BACKGROUND_COLOR, size=(None,1))],
        [sg.Button("Retour", font=('Helvetica', 13, "bold"), key="-RETURN-", size=(30, 1), border_width=0, button_color=("#ffffff", "#181818"))],
        
    ], background_color=BACKGROUND_COLOR, size=(None, None), element_justification='center', expand_x=True, expand_y=True, pad=0)]]

    popup = sg.Window("Légende", infos_column, background_color=BACKGROUND_COLOR, finalize=True, no_titlebar=True, grab_anywhere=True, element_padding=0, location=(20, 20))






    while True:
        event, values = popup.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "-RETURN-":
           return popup.close()

isPaused = False
prev = 0
def createLyricWindow(lyrics, title):
    global isPaused
    global prev
    musicPath = f"{getPath()}/{title}.mp3"
    fileExist = check_file_exists(musicPath)
    SplitLyrics = lyrics.split("\n")
    lyrics_column = []
    temp = []
    for i in range(len(SplitLyrics)):
        n = underline_text_between_underscores(SplitLyrics[i])
        if len(n) ==1:
            temp.append(n[0])
        else:
            temp.append(n)

    chunkedLyrics = chunk_text(temp, 20)
    
    nbChunk = len(chunk_text(temp, 20))
    current_chunk_index = 0
    size = 22

    for i in range(size):
        lyrics_column.append([])
        for j in range(5):
               
            lyrics_column[i].append(sg.Text("", font=('Helvetica', 12, ), text_color=OPTION_COLOR, background_color=BACKGROUND_COLOR, expand_x=False, pad=(0,0), size=(None, 1), key="-LYR " + str(i) + f"#{j+1}-"))

    lyrics_column.append([sg.Button("previous", font=('Helvetica', 10, "bold"), key="-PREV-", size=(None, 1), border_width=0, button_color=("#878787", "#1b1b1b")), sg.Button("Légende", font=('Helvetica', 10, "bold"), key="-LEGEND-", size=(9, 1), border_width=0, button_color=("#878787", "#1b1b1b")), sg.Button("Next", font=('Helvetica', 10, "bold"), key="-NEXT-", size=(None, 1), border_width=0, button_color=("#878787", "#1b1b1b"))])
    if fileExist:
        duration = int(librosa.get_duration(path=musicPath))
        durationTime = strftime("%H:%M:%S", gmtime(duration
                                                   ))
        print(duration)
        lyrics_column.append([sg.Slider(range=(0, duration), text_color=TEXT_COLOR, trough_color="#1b1b1b", background_color=BACKGROUND_COLOR, default_value=0, size=(20, 15), orientation='h', key='-TIME-', enable_events=True), sg.Button(image_filename=f"{data_dir}/pause.png", image_size=(50, 50), key="-PAUSE-", size=(None, 1), border_width=0, button_color=("#878787", BACKGROUND_COLOR)), sg.Slider(range=(0, 100), text_color=TEXT_COLOR, trough_color="#1b1b1b", background_color=BACKGROUND_COLOR, default_value=30, size=(20, 15), orientation='h', key='-VOLUME-', enable_events=True)])


    lyrics_layout = [
        [
            sg.Column(lyrics_column, key="-LYRICS-", background_color=BACKGROUND_COLOR, size=(None, None), justification="center", element_justification="center", expand_y=True, expand_x=True),
        ]
    ]
    
    if fileExist:
        print(musicPath)
        
        mixer.music.load(musicPath)
        mixer.music.play()
        mixer.music.set_volume(0.3)
    window_lyrics = sg.Window("Lyrics", lyrics_layout, size=(800,600), finalize=True, background_color=BACKGROUND_COLOR, icon=data_dir+"/logo.ico")
    update_lyrics_window(window_lyrics, chunkedLyrics, current_chunk_index, size)
    
    offset = 0
    while True:
        event, values = window_lyrics.read(timeout=100)
        currentTime = int(mixer.music.get_pos()/1000) + offset
        

        
        # End program if user closes window_search or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            mixer.music.unload()
            break
        elif event == "-NEXT-":
            current_chunk_index += 1
            update_lyrics_window(window_lyrics, chunkedLyrics, current_chunk_index, size)
            
            # Disable "Next" button if we're at the last chunk
            if current_chunk_index == len(chunkedLyrics) - 1:
                window_lyrics['-NEXT-'].update(disabled=True)
            
            # Enable "Previous" button
            window_lyrics['-PREV-'].update(disabled=False)
        elif event == "-PREV-":
            current_chunk_index -= 1
            update_lyrics_window(window_lyrics, chunkedLyrics, current_chunk_index, size)
            
            # Disable "Previous" button if we're at the first chunk
            if current_chunk_index == 0:
                window_lyrics['-PREV-'].update(disabled=True)
            
            # Enable "Next" button
            window_lyrics['-NEXT-'].update(disabled=False)
        elif event == "-LEGEND-":
            legendWindow()
        elif event == "-PAUSE-":
            print(currentTime)
            if isPaused:
                window_lyrics["-PAUSE-"].update(image_filename=f"{data_dir}/pause.png")
                mixer.music.unpause()
                isPaused = False
            else:
                window_lyrics["-PAUSE-"].update(image_filename=f"{data_dir}/play.png")
                mixer.music.pause()
                isPaused = True
        elif event == "-VOLUME-":
            volume = values["-VOLUME-"] / 100  # Convert slider value (0-100) to volume (0.0-1.0)
            mixer.music.set_volume(volume)        
        elif event == "-TIME-":
            mixer.music.set_pos(values["-TIME-"])
            # currentTime = int(values["-TIME-"])
            offset = int(values["-TIME-"]) - int(mixer.music.get_pos()/1000)
            prev = currentTime - offset - 1
            print(int(values["-TIME-"]))
            print(offset)
            print("##")
        else:
            if prev == currentTime -1:
                print("current time : " + str(int(mixer.music.get_pos()/1000)))
                print("offset time : " + str(offset))
                print("final time : " + str(currentTime))
                print("--")
                prev = currentTime
                window_lyrics["-TIME-"].update(value=currentTime)
            elif prev != currentTime:
                prev = currentTime

def main():
    default = getPath()


    search_layout = [
        [
            sg.Push(background_color=BACKGROUND_COLOR),
            sg.Text("Song Searcher", font=('Verdana', 17, "bold"), text_color="#fdfdfd", background_color=BACKGROUND_COLOR),
            sg.Push(background_color=BACKGROUND_COLOR),
        ],
        [
            sg.Push(background_color=BACKGROUND_COLOR),
            sg.In(size=(25, 1), enable_events=True, key="-SONG-", background_color=INPUT_BACKGROUND, text_color="#bcafbf", border_width=0),
            sg.Push(background_color=BACKGROUND_COLOR),
        ],
        [
            sg.Canvas(key="-CANVAS-", size=(272, 374), background_color=MULTILINE_BACKGROUND),        
        ],
        [
            sg.Text("Audio folder", font=('Verdana', 10, "bold"), text_color="#fdfdfd", background_color=BACKGROUND_COLOR),
            sg.In(size=(16,1), enable_events=True ,key='-FOLDER-', default_text=default), 
            sg.FolderBrowse(font=('Helvetica', 13, "bold"), button_color=("#ffffff", "#181818"), size=(None, 1))
        ]
    ]


    window_search = sg.Window("NOPLP lyrics", search_layout, finalize=True, size=(322, 501), background_color=BACKGROUND_COLOR, icon=data_dir+"/logo.ico")
    print(window_search.AllKeysDict)





    ############################################### LISTBOX LOCAL 
    # Access the Tkinter canvas through PySimpleGUI
    canvas_elem = window_search['-CANVAS-'].TKCanvas
    canvas = Canvas(canvas_elem, height=394, highlightthickness=0, bg=BACKGROUND_COLOR)
    canvas.pack(fill='both', expand=False)

    # Draw rounded rectangle for the listbox
    round_rectangle(canvas, 0, 0, 292, 394, radius=25, fill=MULTILINE_BACKGROUND)

    # Create a Tkinter Listbox and place it inside the rounded rectangle
    listbox = Listbox(canvas, bg=MULTILINE_BACKGROUND, bd=0, highlightthickness=0, activestyle='none', font=('Helvetica', 12), fg=OPTION_COLOR)
    listbox.place(x=10, y=10, width=272, height=374)  # Adjust dimensions based on your layout


    # Function to simulate PySimpleGUI's event system using the "-LOCAL SONG LIST-" key
    def on_select(event):
        selected_indices = listbox.curselection()  # Get selected items
        selected_songs = [listbox.get(i) for i in selected_indices]  # Get values of selected items
        # Send event to PySimpleGUI
        window_search.write_event_value('-LOCAL SONG LIST-', selected_songs)

    def update_listbox(new_values):
        listbox.delete(0, tk.END)  # Clear current items
        for item in new_values:
            listbox.insert(tk.END, item)  # Insert new items
    # Bind the listbox selection to the event handler
    listbox.bind('<<ListboxSelect>>', on_select)



    files = find('*.txt', sings_dir)
    update_listbox(files)





    # Create an event loop
    while True:
        event, values = window_search.read()
        # End program if user closes window_search or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break
        elif len(values[event]) > 0 and event == "-SONG-":
            
            files = find(values[event] + '*.txt', sings_dir)
            update_listbox(files)    
        elif len(values[event]) > 0 and event == "-LOCAL SONG LIST-":
            with open(f'{sings_dir}/{values[event][0]}.txt', 'r', encoding="utf-8") as file:
                # Read the entire content of the file
                content = file.read()
            createLyricWindow(content, values[event][0])
        elif len(values[event]) > 0 and event == "-FOLDER-":
            print(values[event])
            writePath(values[event])

main()
