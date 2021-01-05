import re
import os

hexaPattern = r'%[0-9a-fA-F]{2}'
bitratePattern = r'[0-9]{3}kbps'
yearPattern = r'[12]{1}[0-9]{3}'
def fixTag(tag):
    # Preliminary change, must modify for each website
    def fixWebsiteName(file):
        file = re.sub(r'Masstamilan\.in','', file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'Masstamilan','', file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'Starmusiq\.la', '',file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'Starmusiq', '',file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'www\.', '', file, flags=re.IGNORECASE).lstrip()
        file = re.sub(r'\.info', '', file, flags=re.IGNORECASE).lstrip()
        return file

    # Common stuff
    def fixPunctuation(file):
        file = re.sub(hexaPattern, '', file)
        file = re.sub(bitratePattern, '', file, flags=re.IGNORECASE)
        file = re.sub(yearPattern, '', file)
        file = re.sub('_','', file)
        file = re.sub(r'\:','', file)
        file = re.sub(r'\[','', file)
        file = re.sub(r'\]','', file)
        file = re.sub(r'\(\)', '', file)
        file = re.sub(r'\.+', '.', file)
        file = re.sub(r'^ ', '', file)
        file = re.sub(r'-\.', '.', file)
        file = re.sub(r'-', '', file)
        # file = re.sub(r'-+$', '', file)
        return file.title().lstrip().rstrip()

    m = re.match(' a r ', tag, flags=re.IGNORECASE)
    if m:
        print ("FIX THIS NAME!!: ", m.groups())

    return fixPunctuation(fixWebsiteName(tag))
def fixTitleNames(title):
    title = re.sub(r'^[0-9]{2}', '', title).lstrip()
    title = re.sub(r'^.+', '', title).lstrip()
    return title

def fixArtistNames(artist):
    artist = re.sub(r'\.', ' ', artist)
    artist = re.sub(r'&', ', ', artist)
    artist = re.sub(r'  ', ' ', artist)

    # Specific artist names
    artist = re.sub(r' and', ';', artist, flags=re.IGNORECASE)
    artist = re.sub(r'a\.r\.', 'A R ', artist, flags=re.IGNORECASE)
    artist = re.sub(r'kj ', 'K J ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'k\.j\.', 'K J ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'spb ', 'S P B ',artist, flags=re.IGNORECASE)
    artist = re.sub(r's\.p\.b.', 'S P B ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\ Lasubrahmanyam', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;Lasubrahmanyam', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;Lasubramaniam', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;Lasubramanyam', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;La', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Lasubrahmanyam', '',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Lasubramaniam', '',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Lasubramanyam', '',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;Charan', 'S P Charan',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\; Charan', 'S P Charan',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B Charan', 'S P Charan',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Shanka R', 'Shankar',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sanka R', 'Shankar',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sekha R', 'Sekhar',artist, flags=re.IGNORECASE)
    artist = re.sub(r'kakka R', 'Kakkar',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Aalaa R Ja', 'Aalap Raja',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Dhanya R', 'Dhanyasri',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Srika R', 'Srikar',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Kuma R', 'Kumar',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Vanija R M', 'Vani Jayaram',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Vani ja R M', 'Vani Jayaram',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Deepan Cha R Varthy', 'Deepan Chakravarthy',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S\. P\. Balasubrahmanyam', 'S P B',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S Janki', 'S Janaki',artist, flags=re.IGNORECASE)
    artist = re.sub(r'La ;', '',artist, flags=re.IGNORECASE)
    artist = re.sub(r'G V Nd', 'Govind', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Wa R Er', 'Warrier', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Ba R R', 'Basrur', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Ha R S', 'Harris', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Jayaraj', 'Jeyaraj', artist, flags=re.IGNORECASE)
    artist = re.sub(r'B; Charan', 'B Charan', artist, flags=re.IGNORECASE)
    artist = re.sub(r'B;Charan', 'B Charan', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Ba R M', 'Balram', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Niza R', 'Nizar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Chola R Saya', 'Solar Sai', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Aiva R', 'Aivar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sola R', 'Solar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'sheka R', 'Shekar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'sunda R', 'Sundar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Snda R', 'Sundar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Aishwa r a', 'Aishwarya', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sathya r kash', 'Sathya Prakash', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Uma R Manan', 'Uma Ramanan',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B ', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P Ba ', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P Ba\;', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;Subramaniyam', 'S P B;',artist, flags=re.IGNORECASE)
    artist = re.sub(r'gv ', 'G V ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'Chorus', '',artist, flags=re.IGNORECASE)
    artist = re.sub(r'g\.v\.', 'G V ',artist, flags=re.IGNORECASE)
    artist = re.sub(r'S A R Jkumar', 'S A Rajkumar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sa R Jkumar', 'S A Rajkumar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Varsha R Njith', 'Varsha Ranjith', artist, flags=re.IGNORECASE)
    artist = re.sub(r'5Eli Com', '', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Vathu', 'Aaravathu', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Yaan', 'Aariyaan', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Am', 'Aarvam', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Sh Ganash', 'Amresh Ganesh', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Tha', 'Amrutha', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Arrorahman', 'A R Rahman', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Isaignani Illayaraaja', 'Ilaiyaraaja', artist, flags=re.IGNORECASE)
    artist = re.sub(r'S P B\;La\;', 'S P B;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R T', 'Amrit', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Mili Na R A R T', 'Milli Nair; Amrit', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Hi', 'Aarthi', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R An', 'Aryan', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Ag V Ntira', 'A Raaga Ventira', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Pa R Pazhanisamy','Pa Ra Pazhanisamy;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Seka R','Sekar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'a R\;','ar;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sega R','Segar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Cha R','Chakri', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sudhaka R','Sudhakar', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Nambia R','Nambiar;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sowmta R O','Sowmya Rao;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Ranina R Ddy','Ranina Reddy;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Gopa R O','Gopal Rao;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'P Suseela','P Susheela;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'ks chitra','K S Chitra;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'jairam','jayaram;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'R O','Rao', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Jeya R E','Jeyashree;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Vijaya R Ash','Vijay Prakash;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Vija R Kash','Vijay Prakash;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Jaya R','Jayashree;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'La R Nce','Lawrence;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sa R M','Sargam;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Ragovinda R', 'Raghavendra;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Nambiya R','Nambiar;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Maria R E','Maria Roe;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Maa R M','Maatram;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Na R','Nair;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Shilpa R O','Shilpa Rao;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Rao','Rao;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Viswanathan Ramamoorthy','M S Viswanathan; T K Ramamoorthy;', artist, flags=re.IGNORECASE)    
    artist = re.sub(r'Viswanathan\–Ramamoorthy','M S Viswanathan; T K Ramamoorthy;', artist, flags=re.IGNORECASE)    
    artist = re.sub(r'a R Shnan','akrishnan;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'a R Shan','akrishnan;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Vidyasaga R','Vidyasagar;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Sudha R Ghunathan', 'Sudha Raghunathan;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Steeve Vatz A K A R Ky',' Steevevatz',artist, flags=re.IGNORECASE)
    artist = re.sub(r'R Jeshwaran', 'Rajeshwaran;', artist, flags=re.IGNORECASE)
    artist = re.sub(r'A R Ham','Abraham', artist, flags=re.IGNORECASE)
    artist = re.sub(r'Dha R J','Dhiraj',artist, flags=re.IGNORECASE)
    artist = re.sub(r'\.', ' ', artist)
    artist = re.sub(r'-', ' ', artist)
    artist = re.sub(r'<', ' ', artist)
    artist = re.sub(r'>', ' ', artist)
    artist = re.sub(r'{', ' ', artist)
    artist = re.sub(r'}', ' ', artist)
    artist = re.sub(r'/', ' ',artist)
    artist = re.sub(r'\\', ' ',artist)
    artist = re.sub(r' +', ' ', artist)
    artist = re.sub(r',', ';',artist)
    artist = re.sub(r' ;', ';',artist)
    artist = re.sub(r';+', ';',artist)
    artist = re.sub(r';$', '',artist)
    artist = artist.title().lstrip().rstrip()
    return artist

def spaceOutName(name_title):
    for w in re.findall(r'[A-Z]', name_title):
        name_title = re.sub(w, ' ' + w, name_title)
    return fixTag(re.sub(r' +',' ', name_title).lstrip())
def getTitle(tag, filename):
    if tag.title:
        return spaceOutName(tag.title)
    name_title = os.path.basename(filename.strip('.mp3'))
    return spaceOutName(name_title)

def getAlbum(tag, filename):
    if tag.album:
        return tag.album
    filename_split = os.path.dirname(filename).split('\\')
    if len(filename_split) == 1:
        filename_split = os.path.dirname(filename).split('/')
    if len(filename_split) == 1:
        print("Failed to split filename")
        return ""
    else:
        return spaceOutName(filename_split[-1])
    
def getYear(tag, filename):
    if tag.getBestDate():
        return str(tag.getBestDate())
    filename_split = os.path.dirname(filename).split('\\')
    if len(filename_split) == 1:
        filename_split = os.path.dirname(filename).split('/')
    if len(filename_split) == 1:
        print("Failed to split filename")
        return ""
    else:
        return filename_split[-2]
