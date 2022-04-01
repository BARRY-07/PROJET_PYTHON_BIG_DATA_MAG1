from fpdf import FPDF
from zipfile import ZipFile
import wget
import sys
import json
import urllib.request
import logging
#Pour s'assurer d'avoir 5 arguments (fichier python, fichier json, fichier zip, fichier txt et fichier pdf
if len(sys.argv) != 5:
    sys.exit('ERROR: This file execution needs 5 arguments')
#Pour le style d'affichage du fichier PYlog.txt
logging.basicConfig(filename=sys.argv[3],level=logging.INFO,format='%(message)s')

url_zipfile = sys.argv[2]

#On telecharge le fichier zip et on l'extrait dans la memoire vive, une memoire temporaire
#Ici on veut eviter de l'extraire dans le disque dur
wget.download(url_zipfile,out='/tmp') #Telechargement
zip_file='/tmp/data.zip' #'/temp' designe le dossier temporaire
zip_archive=ZipFile(zip_file,'r')
zip_archive.extractall(path='/tmp')#Extraction

url_json=sys.argv[1]

#Telechargement des donnees JSON et decodage en utf8
response=urllib.request.urlopen(url_json)
content=response.read()
data=json.loads(content.decode("utf8"))
#Ces listes vont prendre les caracteristiques dont on a besoin
names=[]
types=[]
weights=[]
heights=[]
images=[]
weaknesses=[]
for i in range(len(data['pokemon'])):
    names.append(data['pokemon'][i]['name'])
    types.append(data['pokemon'][i]['type'])
    weights.append(data['pokemon'][i]['weight'])
    heights.append(data['pokemon'][i]['height'])
    images.append(data['pokemon'][i]['img'])
    weaknesses.append(data['pokemon'][i]['weaknesses'])
#Pour Trier les pokemons selon leurs noms
names,types,weights,heights,images,weaknesses=[list(i) for i in zip(*sorted(zip(names,types,weights,heights,images,weaknesses)))]


class PDF(FPDF):
    # Mise en forme de l'entête
    def header(self):
        # Logo
        self.image('/tmp/logo.png', 10, 12, 30)
        # Police
        self.set_font('arial', 'B', 15)
        #Titre
        self.cell(280, 15, f'Pokemon Yearbook - Gr. {self.page_no()}', border=True, ln=1, align='C')
        #Reour a ligne
        self.ln(10)

    # Mise en forme du bas de page
    def footer(self):
        # Potion du text
        self.set_y(-15)
        # Police
        self.set_font('arial', 'I', 8)
        # Numero des pages
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

# Creation du pdf
pdf = PDF('L', 'mm', 'A4')

# Total de pages dans le pdf
pdf.alias_nb_pages()

# Set auto page break
pdf.set_auto_page_break(auto = True, margin = 15)

# Ajout de page dans le pdf
pdf.add_page()

# Installation des polices dans le ZipFile

pdf.add_font("DejaVuSansCondensed",'','/tmp/DejaVuSansCondensed.ttf',uni=True)
pdf.add_font("DejaVuSansCondensed-Bold",'','/tmp/DejaVuSansCondensed-Bold.ttf',uni=True)


logging.info('We have '+str(len(names))+' pokemons.') # Premier message du logfile

y=0 # Variable qui va gerer le positionnement des informations sur les pokemons par Page

for i in range(len(names)):
    try: #On utilise le try pour eviter le probleme dans liens url pour les images
        pdf.cell(93, 43,'', 1)
        pdf.image(images[i], 12, 35+y, 30) #Potionnement de l'image du pokemon et taille de l'image
        pdf.set_xy(50, 38+y)
        pdf.set_font('Arial','B', size=8)
        pdf.cell(80, 4, 'Type:', 0, 1,'L')
        pdf.set_xy(50, 48+y)
        pdf.cell(80, 4, 'Height:', 0, 1, 'L')
        pdf.set_xy(50, 58+y)
        pdf.cell(80, 4, 'Weight:', 0, 1, 'L')
        pdf.set_xy(50, 68+y)
        pdf.cell(80, 4, 'Weaknesses:', 0, 1, 'L')
        pdf.set_font('Arial', size=8)
        pdf.set_xy(50, 43+y)
        x=10
        for j in range(len(types[i])): # Nous  avons parfois des listes dans la liste "types"
            if len(types[i])!=1:
                pdf.cell(0,0,types[i][j]+',', 0, 1,fill=False)
                pdf.set_xy(50+x, 43 + y)
                x=x+10
            else:
                pdf.cell(0,0,types[i][j], 0, 1, fill=False)
        pdf.set_xy(50, 53+y)
        pdf.cell(0,0,heights[i], 0, 1, 'L')
        pdf.set_xy(50, 63+y)
        pdf.cell(0,0, weights[i], 0, 1, 'L')
        pdf.set_xy(50, 73+y)
        x = 10
        for j in range(len(weaknesses[i])): # Nous  avons parfois des listes dans la liste "weaknesses"
            if len(weaknesses[i]) != 1:
                pdf.cell(0,0, weaknesses[i][j] + ',', 0, 1, fill=False)
                pdf.set_xy(50 + x, 73 + y)
                x = x + 10
            else:
                pdf.cell(0,0, weaknesses[i][j], 0, 1, fill=False)
        pdf.set_xy(12, 62+y)
        pdf.set_font('DejaVuSansCondensed-Bold', size=11)
        pdf.set_text_color(300, 30, 40)
        pdf.cell(80, 4, 'Name: ', 0, 1, 'L')
        pdf.set_xy(12, 68+y)
        pdf.set_font('DejaVuSansCondensed', size=11)
        pdf.set_text_color(300, 30, 40)
        pdf.cell(80, 4,names[i], 0, 1, 'L')
        pdf.set_text_color(0,0,0)
        pdf.ln(6)
        if y==84:
            y=0
        else:
            y=y+42
        logging.info('Treating the pokemon: {}'.format(names[i])) # Message du LogFile quand tout va bien

    except: # Ce bloc gere la partie ou on aurait une erreur dans l'URL de l'image du pokemon
        pdf.image('/tmp/placeholder.png', 12, 35 + y, 30) #remplacement de l'URL par l'image 'placeholder'
        pdf.set_xy(50, 38 + y)
        pdf.set_font('Arial', 'B', size=8)
        pdf.cell(80, 4, 'Type:', 0, 1, 'L')
        pdf.set_xy(50, 48 + y)
        pdf.cell(80, 4, 'Height:', 0, 1, 'L')
        pdf.set_xy(50, 58 + y)
        pdf.cell(80, 4, 'Weight:', 0, 1, 'L')
        pdf.set_xy(50, 68 + y)
        pdf.cell(80, 4, 'Weaknesses:', 0, 1, 'L')
        pdf.set_font('Arial', size=8)
        pdf.set_xy(50, 43 + y)
        x = 10
        for j in range(len(types[i])):
            if len(types[i]) != 1:
                pdf.cell(0, 0, types[i][j] + ',', 0, 1, fill=False)
                pdf.set_xy(50 + x, 43 + y)
                x = x + 10
            else:
                pdf.cell(0, 0, types[i][j], 0, 1, fill=False)
        pdf.set_xy(50, 53 + y)
        pdf.cell(0, 0, heights[i], 0, 1, 'L')
        pdf.set_xy(50, 63 + y)
        pdf.cell(0, 0, weights[i], 0, 1, 'L')
        pdf.set_xy(50, 73 + y)
        x = 10
        for j in range(len(weaknesses[i])):
            if len(weaknesses[i]) != 1:
                pdf.cell(0, 0, weaknesses[i][j] + ',', 0, 1, fill=False)
                pdf.set_xy(50 + x, 73 + y)
                x = x + 10
            else:
                pdf.cell(0, 0, weaknesses[i][j], 0, 1, fill=False)
        pdf.set_xy(12, 62 + y)
        pdf.set_font('DejaVuSansCondensed-Bold', size=11)
        pdf.set_text_color(300, 30, 40)
        pdf.cell(80, 4, 'Name: ', 0, 1, 'L')
        pdf.set_xy(12, 68 + y)
        pdf.set_font('DejaVuSansCondensed', size=11)
        pdf.set_text_color(300, 30, 40)
        pdf.cell(80, 4, names[i], 0, 1, 'L')
        pdf.set_text_color(0, 0, 0)
        pdf.ln(6)
        if y == 84:
            y = 0
        else:
            y = y + 42
        logging.info('Treating the pokemon: {}'.format(names[i]))
        # Message du LogFile quand le lien URL de l'image comporte une erreur
        logging.info('!!! the image file {} does not exist. It was	replaced with the placeholder...	!!!'.format(images[i]))
logging.info('All done.') # Message de fin du LogFile
pdf.output(sys.argv[4])


#Pour generer le fichier requirements.txt il faut:
### faire pip install pipreqs
### pipreqs /chemin/dacces/du/projet