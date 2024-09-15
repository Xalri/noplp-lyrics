from pprint import pprint
import requests
import urllib.parse
from colorama import Style
import PySimpleGUI as sg
import os, fnmatch
import html
import re
# test


def remove_ansi_escape_codes(text):
    ansi_escape = re.compile(r'\x1b\[.*?m')
    return ansi_escape.sub('', text)

def decode_escape_sequences(s):
    def replace_hex(match):
        hex_value = match.group(1)
        return chr(int(hex_value, 16)) 
    
    return re.sub(r'\\x([0-9A-Fa-f]{2})', replace_hex, s)

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
    except requests.ConnectionError or requests.exceptions.ReadTimeout:
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
        elif parts[i] == "":
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
    return row

def getLyrics(title):

    chanson = capitalize_first_letter_inside_parentheses(title.replace(" ", "_")[0].upper() + title.replace(" ", "_")[1:])
    url = "https://n-oubliez-pas-les-paroles.fandom.com/fr/wiki/" + chanson
    print("------")
    print("Url : " + url)


    reponse = requests.get(url)
    paroles = reponse.text.split("""<li>(x 2) en fin de ligne&#160;: la ligne doit être répétée 2 fois</li></ul>
</div>""")[1].split("""</p><p><br />
</p>
<h2><span class="mw-headline" id="Dates_de_sortie">Dates de sortie</span>""")[0].replace("</b>","").replace("<b>","").replace("</p>","").replace("<p>","").replace("<br />","").replace("</i>",Style.RESET_ALL).replace("<i>","#").replace("(", "\x1B[3m" + Style.DIM).replace(")", Style.RESET_ALL)

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
    # print(newParoles)
    print(len())
    print("------")
    return newParoles

def getSings(part):

    if part == 1:
        url = "https://n-oubliez-pas-les-paroles.fandom.com/fr/wiki/Liste_des_chansons_existantes_(de_la_lettre_A_%C3%A0_la_lettre_M)"
        reponse = requests.get(url)
        paroles = reponse.text.split("""<h2><span class="mw-headline" id="Chiffre"><big><b>Chiffre</b></big></span></h2>
<h3><span class="mw-headline" id="113"><b>113</b></span></h3>""")[1].split("""<p><br /><a href="/fr/wiki/Listes_des_chansons_existantes_(de_la_lettre_N_%C3%A0_la_lettre_Z)" class="mw-redirect" title="Listes des chansons existantes (de la lettre N à la lettre Z)"><b>Pour aller à la liste des chansons existantes de N à Z</b></a>
</p></div>""")[0]
        print("part 1")
    elif part == 2:
        print("part 2")
        url = "https://n-oubliez-pas-les-paroles.fandom.com/fr/wiki/Listes_des_chansons_existantes_(de_la_lettre_N_%C3%A0_la_lettre_Z)"
        reponse = requests.get(url)
        paroles = reponse.text.split("""<h2><span class="mw-headline" id="N"><b><big>N</big></b></span></h2>
<h3><span class="mw-headline" id="Nacash"><b>Nacash</b></span></h3>""")[1].split("""<p><br />
<b><a href="/fr/wiki/Liste_des_chansons_existantes_(de_la_lettre_A_%C3%A0_la_lettre_M)" title="Liste des chansons existantes (de la lettre A à la lettre M)">Pour revenir à la liste des chansons existantes de A à M</a></b>
</p>""")[0]
    else:
        raise ValueError("Invalid input. Please enter either 1 or 2.")
    # print("Url : " + url)



    parolesSplit = paroles.split("\n")
    # test = paroles.split("""<h3><span class="mw-headline" id=""")[1].split("<b>")[1].split("\n")
    # # print(test)
    # testlist = []
    # title = html.unescape(test[0].split("</b")[0])
    # print(title)
    # for sings in test[1:]:
    #     if not sings == "":
    #         # print(sings)
    #         # print(sings.split('title="')[1].split('">')[0])
    #         testlist.append({"songTitle": sings.split('title="')[1].split('">')[0], "artistTitle":decode_escape_sequences(title)})
    # print(testlist)
    # print(testlist[0]["artistTitle"])
    # print("----------------------------------------------------------------")
    # print(" ")
    # d
    result = []
    for i in range(len(parolesSplit)):
        if not parolesSplit[i] == "" and "href=" in parolesSplit[i]:
            result.append(html.unescape(parolesSplit[i].split('title="')[1].split('">')[0].lower()))

    return result

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name).split("\\")[1].split(".txt")[0])
    return result

#ttest
def chunk_textt(text, chunk_size=5):
    nbChunk = int(len(text)/chunk_size)
    result = []
    pprint(text[0][0]["text"])
    # temp = "".join([(t[0]["text"] + "\n") for t in text[:chunk_size]])
    temp = ""
    for i, t in enumerate(text[:chunk_size]):
        temp += t[0]["text"]
        if i < len(text[:chunk_size]) - 1:
            temp += f"\n/\n"
    print(temp)
    indices = [i for i, c in enumerate(temp) if c == "/"]
    print(indices)
    
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]  

def chunk_text(text, chunk_size=5):
    result = []

    for _ in range(7):
        index = 0
        for i in range(len(text)):
            print(text[i][0])
            if i == chunk_size:
                break
            if text[i][0]["text"] == " " and i > index:
                index = i
        if index == 0:
            notFound = chunk_size
            print("not found")
            print("test2")
            while index == 0:
                print("----")
                print(len(text))
                notFound += 1
                if len(text) > 0:
                    
                    for i in range(len(text)):
                        print(text[i][0])
                        if 0 == len(text):
                            print("text finish")
                            index = i
                            break

                        # if i == notFound:
                        #     break
                        if text[i][0]["text"] == " " and i > index:
                            index = int(i/2)
                            break
                    # input()
                else:
                    index = 999
                    print(result)
        print("ok")
        if text != 999:
            result.append([t[0] for t in text[:index]])
            text = text[index+1:]
    for elem in result:
        pprint(elem)
        print("_______________________")

    return result
        


def update_lyrics_window(window, lyrics, chunk_index, size):
    
    for i in range(size):
        currentChunk = lyrics[chunk_index]
        if i+1 > len(currentChunk):
            print("false " + str(i))
            window["-LYR " + str(i) + "-"].update(" ")
        else:
            print(i)
            line = currentChunk[i]
            bold = line["bold"]
            italic = line["italic"]
            colored = line["color"]
            text = line["text"]

            if italic:
                if bold:
                    if colored:
                        window["-LYR " + str(i) + "-"].update(text, font=('Helvetica', 12, 'bold italic'), text_color="Orange")
                        # lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12, 'bold italic'), text_color="Orange", pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
                    else:
                        window["-LYR " + str(i) + "-"].update(text, font=('Helvetica', 12, 'bold italic'))
                        # lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12, 'bold italic'), pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
                else:
                    if colored:
                        window["-LYR " + str(i) + "-"].update(text, font=('Helvetica', 12, 'italic'), text_color="Orange")
                        # lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12, 'italic'), text_color="Orange", pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
                    else:
                        window["-LYR " + str(i) + "-"].update(text, font=('Helvetica', 12, 'italic'))
                        # lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12, 'italic'), pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
            else:
                if bold:
                    if colored:
                        window["-LYR " + str(i) + "-"].update(text, font=('Helvetica', 12, 'bold'), text_color="Orange")
                        # lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12, 'bold'), text_color="Orange", pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
                    else:
                        window["-LYR " + str(i) + "-"].update(text, font=('Helvetica', 12, 'bold'))
                        # lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12, 'bold'), pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
                else:
                    if colored:
                        window["-LYR " + str(i) + "-"].update(text, font=('Helvetica', 12), text_color="Orange")
                        # lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12), text_color="Orange", pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
                    else:
                        window["-LYR " + str(i) + "-"].update(text, font=('Helvetica', 12))
                        # lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12), pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
def createLyricWindow(lyrics):
    SplitLyrics = lyrics.split("\n")
    lyrics_column = []
    temp = []
    for i in range(len(SplitLyrics)):
        # if SplitLyrics[i].startswith(" #"):
        #     lyrics_column.append([sg.Text(SplitLyrics[i][2:], text_color='grey')])
        # else:
        #     lyrics_column.append([sg.Text(SplitLyrics[i])])

        n = underline_text_between_underscores(SplitLyrics[i])
        for l in n:
            temp.append([l])

    # chunkLyrics = chunk_text(temp, 20)
    pprint(temp)
    print(len(temp))
    print("================================")
    chunkedLyrics = chunk_text(temp, 20)
    
    nbChunk = len(chunk_text(temp, 20))
    # print(nbChunk)
    # print("--------------------------------")
    # pprint(chunk_text(temp, 20))
    current_chunk_index = 0
    size = int(len(temp)/2)
    for i in range(size):
        lyrics_column.append([])
        currentChunk = chunkedLyrics[current_chunk_index]
        if i >= len(currentChunk) -1:
            lyrics_column[i].append(sg.Text("‎"))
        else:

            line = currentChunk[i]
            bold = line["bold"]
            italic = line["italic"]
            colored = line["color"]
            text = line["text"]

            if italic:
                if bold:
                    if colored:
                        lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12, 'bold italic'), text_color="Orange", pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
                    else:
                        lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12, 'bold italic'), pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
                else:
                    if colored:
                        lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12, 'italic'), text_color="Orange", pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
                    else:
                        lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12, 'italic'), pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
            else:
                if bold:
                    if colored:
                        lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12, 'bold'), text_color="Orange", pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
                    else:
                        lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12, 'bold'), pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
                else:
                    if colored:
                        lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12), text_color="Orange", pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
                    else:
                        lyrics_column[i].append(sg.Text(text, font=('Helvetica', 12), pad=(0,0), size=(None, 1), expand_x=True, key="-LYR " + str(i) + "-"))
    # pprint(chunkLyrics)
    # print(chunkLyrics)
    pprint(chunkedLyrics[current_chunk_index])
    pprint(len(chunkedLyrics[current_chunk_index]))
    pprint(len(lyrics_column))
    # print(lyrics_column)

    infos_column = [
        [sg.Text("Légende:", font=('Helvetica', 12, "underline"))],
        [sg.Text("gras -> texte montré à l'écran ", font=('Helvetica', 12, 'bold'))],
        [sg.Text("italic -> texte pas montré à l'écran mais présent dans la version du chanteur", font=('Helvetica', 12, "italic"))],
        [sg.Text("orange -> texte de NOPLP n'existant pas dans la version du chanteur ", font=('Helvetica', 12, "bold"), text_color="Orange")],
        [sg.Text(" ")],
        [sg.Button("Previous", key="-PREV-", disabled=True), sg.Button("Next", key="-NEXT-")],
    ]

    lyrics_layout = [
        [
            sg.Column(lyrics_column, key="-LYRICS-"),
            sg.Column(infos_column, key="-INFOS-"),

        ]
    ]
    

    window_lyrics = sg.Window("Lyrics", lyrics_layout, location=(900,0), size=(1000,1280), finalize=True)
    pprint(window_lyrics.element_list())
    while True:
        event, values = window_lyrics.read()
        print(event)
        # End program if user closes window_search or
        # presses the OK button
        if event == "OK" or event == sg.WIN_CLOSED:
            break
        if event == "-NEXT-":
            current_chunk_index += 1
            print(current_chunk_index)
            update_lyrics_window(window_lyrics, chunkedLyrics, current_chunk_index, size)
            
            # Disable "Next" button if we're at the last chunk
            if current_chunk_index == len(lyrics_column) - 1:
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





search_layout = [
    [
        sg.Text("Song Searcher"),
        sg.In(size=(25, 1), enable_events=True, key="-SONG-")
    ],
    [sg.Text("Downloaded song"),],
    [
        
        sg.Listbox(
            values=[], enable_events=True, size=(40, 10), key="-LOCAL SONG LIST-"
        )
    ],
    [sg.Text("Online song"),],
    [
        
        sg.Listbox(
            values=[], enable_events=True, size=(40, 10), key="-ONLINE SONG LIST-"
        )
    ],
]

lyrics_viewer_column = [
    [sg.Text("Choose an song from list on left:", key="-NO SONG TEXT-", )],
]

layout = [
    [
        sg.Column(search_layout),

    ]
]

# Create the window
window_search = sg.Window("NOPLP lyrics", layout)

# Create an event loop
while True:
    event, values = window_search.read()
    print(event)
    # End program if user closes window_search or
    # presses the OK button
    if event == "OK" or event == sg.WIN_CLOSED:
        break
    elif len(values[event]) > 0 and event == "-SONG-":
        
        files = find(values[event] + '*.txt', './sings')
        window_search["-LOCAL SONG LIST-"].update(files)

        if 1 == 2:
        # if internet_connection()
            if values[event][0].upper() < "m":
                search = getSings(1)
            else:
                search = getSings(2)
            results = [item for item in search if item.lower().startswith(values[event].lower())]
            # print("taille : " + str(len(search)))
            for song in results:
                # print(results[:1])
                if song in files:
                    # print(song)
                    results.remove(song)
            window_search["-ONLINE SONG LIST-"].update(results)
    elif len(values[event]) > 0 and event == "-LOCAL SONG LIST-":
        with open('./sings/{filename}.txt'.format(filename=values[event][0]), 'r') as file:
            # Read the entire content of the file
            content = file.read()
        # window_search.close()
        createLyricWindow(content)
    elif len(values[event]) > 0 and event == "-ONLINE SONG LIST-":
        lyrics = getLyrics(values[event][0])
        Split = lyrics.split("\n")
        new = ""
        for line in Split:
            new += str(line.encode("utf-8"))
        print(new)

        with open("./sings/{filename}.txt".format(filename=values[event][0]), 'w') as file:
            # Write content to the file
            file.write(lyrics)
        # window_search.close()
        createLyricWindow(lyrics)


# title = urllib.parse.quote(input("Titre : \n"))
