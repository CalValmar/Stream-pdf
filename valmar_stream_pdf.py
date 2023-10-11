from colorama import Fore, Style
import base64
import zlib
import os
import re

# Fichier PDF par défaut :
default_pdf_file = 'bac2004.pdf' # A modifier par le nom du fichier PDF à analyser

def print_banner():
    banner = """    ______                       ___  ___  ____
   / __/ /________ ___ ___ _    / _ \/ _ \/ __/
  _\ \/ __/ __/ -_) _ `/  ' \  / ___/ // / _/  
 /___/\__/_/  \__/\_,_/_/_/_/ /_/  /____/_/  """
    
    info = """
  [+] Github : https://github.com/CalValmar
  [+] Auteur : Valmar
  [+] Version : 1.0 """
    
    print(Fore.GREEN + Style.BRIGHT + banner)
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + info)

# Fonction pour clear le terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fonction pour supprimer les fichiers
def remove_files():
    for file in os.listdir('generated_files'):
        os.remove(os.path.join('generated_files', file))
    for file in os.listdir('objects_streams_list'):
        os.remove(os.path.join('objects_streams_list', file))
 
# Fonction pour afficher la liste des objets / streams
def object_stream_list(pdf_file):
    with open(pdf_file, 'rb') as f:
        content = f.read()
        
    list_obj = []
    for i, obj in enumerate(content.split(b'endobj')):
        if b'obj' in obj:
            list_obj.append(i + 1)
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + f"\n Liste des objets dans '{pdf_file}' :" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f"\n {list_obj}")

    list_stream = []
    for i, obj in enumerate(content.split(b'endobj')):
        if b'stream' in obj:
            list_stream.append(i + 1)
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + f"\n Liste des stream dans '{pdf_file}' :" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f"\n {list_stream}")
    
    # Enregistrer la liste des objets / streams dans un le fichier '/objects_streams_list/{pdf_file}_list.txt'
    if not os.path.exists(f"objects_streams_list/{pdf_file}_list.txt"):
        with open(os.path.join('objects_streams_list', f'{pdf_file}_list.txt'), 'w') as f:
            f.write(f"Liste des objets dans '{pdf_file}' :\n {list_obj}\n\nListe des stream dans '{pdf_file}' :\n {list_stream}")
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"\n [+] Liste des objets / streams enregistrée dans" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f" objects_streams_list/{pdf_file}_list.txt")


# Fonction pour extraire les objets Stream
def extract_object_stream(pdf_file, object_stream_number, output_file):
    try:
        # Ouvrir le fichier PDF en mode binaire
        with open(pdf_file, 'rb') as f:
            content = f.read()
        
        # Séparer les objets Stream
        object_streams = content.split(b'endobj')
        
        if object_stream_number == -1:
            # Extraction de tous les objets
            with open(output_file, 'wb') as out_f:  
                for obj in object_streams:
                    out_f.write(obj + b'endobj\n')
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"\n [+] Tous les objets / streams ont été extraits avec succès dans" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f" {output_file}")
        elif object_stream_number >= 1 and object_stream_number <= len(object_streams):
            # Récupérer l'objet Stream demandé
            object_stream = object_streams[object_stream_number - 1] + b'endobj\n'
            with open(output_file, 'wb') as out_f:
                out_f.write(object_stream)    
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"\n [+] Objet / Stream {object_stream_number} extrait avec succès dans" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f" {output_file}")

        else:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] L'objet / Stream {object_stream_number} n'existe pas dans ce PDF.")
    except FileNotFoundError:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] Le fichier PDF '{pdf_file}' n'a pas été trouvé.")
    except Exception as e:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] Une erreur s'est produite : {str(e)}")


# Fonction pour extraire les objets Stream FlateDecode
def extract_flatedecode(pdf_file, output_file):
    # Récupérer les objets Stream FlateDecode
    stream = re.compile(rb'.*?FlateDecode.*?stream(.*?)endstream', re.S) 
    
    # Extraire les objets Stream FlateDecode
    for i, s in enumerate(stream.findall(open(pdf_file, 'rb').read())):
        s = s.strip(b'\r\n')
        try:
            with open(os.path.join('generated_files', output_file), 'wb') as f:
                f.write(zlib.decompress(s))
                if i == 0:
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"\n [+] Objet / Stream extrait avec succès dans" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f" generated_files/{output_file}")
                    print(Fore.LIGHTBLACK_EX + Style.BRIGHT + " Cela peut prendre quelques secondes...")
                else:
                    continue
        
        except zlib.error:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n [-] Le contenu n'est pas compressé avec FlateDecode.")       
        except Exception as e:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] Une erreur s'est produite : {str(e)}")
        

# Fonction pour décoder le contenu d'un Flatecode en base64
def decode_flatedecode(pdf_file, outpout_file):
    try:        
        # Décoder le contenu en base64
        decoded_content = base64.b64decode(open(pdf_file, 'rb').read())
        
        with open(os.path.join('generated_files', outpout_file), 'wb') as out_f:
            out_f.write(decoded_content)
        
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\n [+] Décodé avec succès dans" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f" generated_files/{outpout_file}")
        
    except FileNotFoundError:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n [-] Le fichier PDF n'a pas été trouvé.")
    except Exception as e:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] Une erreur s'est produite : {str(e)}")     


# Fonction principale
def main():
    print_banner()
    
    while True:
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\n Sélectionnez le type d'extraction :")
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n  [1] ➙ Afficher tous les objets/streams")
        print("  [2] ➙ Extraire tous les objets/streams")
        print("  [3] ➙ Extraire un objets/streams spécifique")
        print("  [4] ➙ Extraire le FlateDecode")
        print("  [5] ➙ Supprimer les fichiers générés")
        print("  [6] ➙ Quitter le programme")
        
        extraction_type = input(Fore.GREEN + "\n Option : ")
        
        # [1] Afficher tous les objets Stream
        if extraction_type == '1':
            pdf_file = input(Fore.GREEN + " Entrez le nom du fichier PDF à analyser : ")
            if pdf_file == '':
                pdf_file = default_pdf_file
            
            if not os.path.exists("objects_streams_list"):
                os.makedirs("objects_streams_list")
            clear_screen(), object_stream_list(pdf_file)
        
            choice = input(Fore.LIGHTBLACK_EX + "\n Appuyez sur Entrée pour continuer...")
            if choice == '':
                clear_screen(), print_banner()
                continue
            else:
                break
        
        # [2] Extraire tous les objets Stream
        elif extraction_type == '2':
            pdf_file = input(Fore.GREEN + " Entrez le nom du fichier PDF à analyser : ")
            if pdf_file == '':
                pdf_file = default_pdf_file
            extract_object_stream(pdf_file, -1, os.path.join('generated_files', 'all_objects.txt'))
            
            choice = input(Fore.LIGHTBLACK_EX + "\n Appuyez sur Entrée pour continuer...")
            if choice == '':
                clear_screen(), print_banner()
                continue
            else:
                break
        
        # [3] Extraire un objet Stream spécifique
        elif extraction_type == '3':
            pdf_file = input(Fore.GREEN + " Entrez le nom du fichier PDF à analyser : ")
            if pdf_file == '':
                pdf_file = default_pdf_file
            object_stream_number = input(Fore.GREEN + " Entrez le numéro de l'objet / stream à extraire : ")
            try:
                object_stream_number = int(object_stream_number)
            except ValueError:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n [-] Le numéro de l'objet / stream doit être un entier.")
                choice = input(Fore.LIGHTBLACK_EX + "\n Appuyez sur Entrée pour continuer...")
                clear_screen(), print_banner()
                continue
            if object_stream_number <= 0:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n [-] Le numéro de l'objet / stream doit être supérieur à zéro.")
                choice = input(Fore.LIGHTBLACK_EX + "\n Appuyez sur Entrée pour continuer...")
                clear_screen(), print_banner()
                continue
            if object_stream_number > len(open(pdf_file, 'rb').read().split(b'endobj')):
                print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n [-] Le numéro de l'objet / stream est supérieur au nombre d'objets / stream dans ce PDF.")
                choice = input(Fore.LIGHTBLACK_EX + "\n Appuyez sur Entrée pour continuer...")
                clear_screen(), print_banner()
                continue
            try:
                extract_object_stream(pdf_file, object_stream_number, os.path.join('generated_files', f'object_stream_{object_stream_number}.txt'))
                # Demander à l'utilisateur s'il veut visualiser le contenu de l'objet Stream
                while True:
                    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\n Voulez-vous visualiser le contenu de l'objet / stream ?")
                    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n  [1] ➙ Oui")
                    print("  [2] ➙ Non")
                    choice = input(Fore.GREEN + "\n Option : ")
                    if choice == '1':
                        try: 
                            print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + f"\n\n Contenu de l'objet / stream {object_stream_number} :" + Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n" + "-" * 80 + Fore.WHITE + Style.BRIGHT + open(os.path.join('generated_files', f'object_stream_{object_stream_number}.txt'), 'r').read() + Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n" + "-" * 80)
                            choice = input(Fore.LIGHTBLACK_EX + "\n Appuyez sur Entrée pour continuer...")
                            clear_screen(), print_banner()
                            break
                        except UnicodeDecodeError:
                            print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] Impossible d'afficher le contenu de l'objet / stream {object_stream_number}.")
                            choice = input(Fore.LIGHTBLACK_EX + "\n Appuyez sur Entrée pour continuer...")
                            clear_screen(), print_banner()
                            break
                        except FileNotFoundError:
                            print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] Le fichier 'object_stream_{object_stream_number}.txt' n'a pas été trouvé.")
                            choice = input(Fore.LIGHTBLACK_EX + "\n Appuyez sur Entrée pour continuer...")
                            clear_screen(), print_banner()
                            break
                    elif choice == '2':
                        clear_screen(), print_banner()
                        break
                    else:
                        clear_screen()
                        print(Fore.RED + Style.BRIGHT + "\n [-] Veuillez entrer 1 ou 2 pour sélectionner une option.")
                           
            except FileNotFoundError:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n [-] Le fichier PDF n'a pas été trouvé.")
                choice = input(Fore.LIGHTBLACK_EX + "\n Appuyez sur Entrée pour continuer...")
                clear_screen(), print_banner()
                continue
            except Exception as e:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] Une erreur s'est produite : {str(e)}")
                choice = input(Fore.LIGHTBLACK_EX + "\n Appuyez sur Entrée pour continuer...")
                clear_screen(), print_banner()
                continue
               
        # [4] Extraire le flatecode du pdf    
        elif extraction_type == '4':
            pdf_file = input(Fore.GREEN + " Entrez le nom du fichier PDF à analyser : ")
            if pdf_file == '':
                pdf_file = default_pdf_file
            extract_flatedecode(pdf_file, 'raw_flatedecode.txt')
               
            # Demander à l'utilisateur s'il veut décoder le contenu du FlateDecode
            while True:
                print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\n Voulez-vous decoder (base64) le contenu de l'objet / stream ?")
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n  [1] ➙ Oui")
                print("  [2] ➙ Non")
                choice = input(Fore.GREEN + "\n Option : ")
                if choice == '1':
                    decode_flatedecode(os.path.join('generated_files', 'raw_flatedecode.txt'), 'decoded_flatedecode.jpg') # Modifier l'extension du fichier de sortie si nécessaire
                    choice = input(Fore.LIGHTBLACK_EX + "\n Appuyez sur Entrée pour continuer...")
                    clear_screen(), print_banner()
                    break
                elif choice == '2':
                    clear_screen(), print_banner()
                    break
                else:
                    clear_screen()
                    print(Fore.RED + Style.BRIGHT + "\n [-] Veuillez entrer 1 ou 2 pour sélectionner une option.")
                
        # [5] Supprimer les fichiers générés
        elif extraction_type == '5':
            try:
                remove_files()
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\n [+] Les fichiers générés ont été supprimés avec succès.")
                choice = input(Fore.LIGHTBLACK_EX + "\n Appuyez sur Entrée pour continuer...")
                clear_screen(), print_banner()
                continue
            except Exception as e:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] Une erreur s'est produite : {str(e)}")
                choice = input(Fore.LIGHTBLACK_EX + "\n Appuyez sur Entrée pour continuer...")
                clear_screen(), print_banner()
                continue
                
        # [6] Quitter le programme 
        elif extraction_type == '6':
            clear_screen()
            break
        else:
            clear_screen()
            print(Fore.RED + Style.BRIGHT + "\n [-] Veuillez entrer un nombre entre 1 et 5.")


# Lancement du programme
if __name__ == '__main__':
    if not os.path.exists('generated_files'):
        os.makedirs('generated_files')
    main()
    