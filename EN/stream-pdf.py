from colorama import Fore, Style
import base64
import zlib
import os
import re

# Default PDF file:
default_pdf_file = 'bac2004.pdf'  # Change to the PDF file name you want to analyze for easier script usage (press Enter to use the default file)

def print_banner():
    banner = """    ______                       ___  ___  ____
   / __/ /________ ___ ___ _    / _ / _ / __/
  _\ \/ __/ __/ -_) _ `/  ' \  / ___/ // / _/
 /___/\__/_/  \__/\_,_/_/_/_/ /_/  /____/_/  """

    info = """
  [+] Github: https://github.com/CalValmar
  [+] Author: Valmar
  [+] Version: 1.0 """

    print(Fore.GREEN + Style.BRIGHT + banner)
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + info)

# Function to clear the terminal
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Function to remove files
def remove_files():
    for file in os.listdir('generated_files'):
        os.remove(os.path.join('generated_files', file))
    for file in os.listdir('objects_streams_list'):
        os.remove(os.path.join('objects_streams_list', file))

# Function to display the list of objects/streams
def object_stream_list(pdf_file):
    with open(pdf_file, 'rb') as f:
        content = f.read()

    list_obj = []
    for i, obj in enumerate(content.split(b'endobj')):
        if b'obj' in obj:
            list_obj.append(i + 1)
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + f"\n List of objects in '{pdf_file}':" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f"\n {list_obj}")

    list_stream = []
    for i, obj in enumerate(content.split(b'endobj')):
        if b'stream' in obj:
            list_stream.append(i + 1)
    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + f"\n List of streams in '{pdf_file}':" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f"\n {list_stream}")

    # Save the list of objects/streams to the file '/objects_streams_list/{pdf_file}_list.txt'
    if not os.path.exists(f"objects_streams_list/{pdf_file}_list.txt"):
        with open(os.path.join('objects_streams_list', f'{pdf_file}_list.txt'), 'w') as f:
            f.write(f"List of objects in '{pdf_file}':\n {list_obj}\n\nList of streams in '{pdf_file}':\n {list_stream}")
        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"\n [+] List of objects/streams saved in" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f" objects_streams_list/{pdf_file}_list.txt")

# Function to extract objects/streams
def extract_object_stream(pdf_file, object_stream_number, output_file):
    try:
        # Open the PDF file in binary mode
        with open(pdf_file, 'rb') as f:
            content = f.read()

        # Split the object streams
        object_streams = content.split(b'endobj')

        if object_stream_number == -1:
            # Extract all objects
            with open(output_file, 'wb') as out_f:
                for obj in object_streams:
                    out_f.write(obj + b'endobj\n')
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"\n [+] All objects/streams successfully extracted to" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f" {output_file}")
        elif object_stream_number >= 1 and object_stream_number <= len(object_streams):
            # Get the requested object stream
            object_stream = object_streams[object_stream_number - 1] + b'endobj\n'
            with open(output_file, 'wb') as out_f:
                out_f.write(object_stream)
            print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"\n [+] Object/Stream {object_stream_number} successfully extracted to" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f" {output_file}")

        else:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] Object/Stream {object_stream_number} does not exist in this PDF.")
    except FileNotFoundError:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] The PDF file '{pdf_file}' was not found.")
    except Exception as e:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] An error occurred: {str(e)}")

# Function to extract FlateDecode content
def extract_flatedecode(pdf_file, output_file):
    # Retrieve FlateDecode stream objects
    stream = re.compile(rb'.*?FlateDecode.*?stream(.*?)endstream', re.S)

    # Extract FlateDecode stream objects
    for i, s in enumerate(stream.findall(open(pdf_file, 'rb').read())):
        s = s.strip(b'\r\n')
        try:
            with open(os.path.join('generated_files', output_file), 'wb') as f:
                f.write(zlib.decompress(s))
                if i == 0:
                    print(Fore.LIGHTGREEN_EX + Style.BRIGHT + f"\n [+] Object/Stream successfully extracted to" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f" generated_files/{output_file}")
                    print(Fore.LIGHTBLACK_EX + Style.BRIGHT + " This may take a few seconds...")
                else:
                    continue

        except zlib.error:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n [-] The content is not compressed with FlateDecode.")
        except Exception as e:
            print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] An error occurred: {str(e)}")

# Function to decode FlateDecode content in base64
def decode_flatedecode(pdf_file, output_file):
    try:
        # Decode content in base64
        decoded_content = base64.b64decode(open(pdf_file, 'rb').read())

        with open(os.path.join('generated_files', output_file), 'wb') as out_f:
            out_f.write(decoded_content)

        print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\n [+] Successfully decoded to" + Fore.LIGHTYELLOW_EX + Style.BRIGHT + f" generated_files/{output_file}")

    except FileNotFoundError:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n [-] The PDF file was not found.")
    except Exception as e:
        print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] An error occurred: {str(e)}")

# Main function
def main():
    print_banner()

    while True:
        print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\n Select the extraction type:")
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n  [1] ➙ Show all objects/streams")
        print("  [2] ➙ Extract all objects/streams")
        print("  [3] ➙ Extract a specific object/stream")
        print("  [4] ➙ Extract FlateDecode")
        print("  [5] ➙ Remove generated files")
        print("  [6] ➙ Quit the program")

        extraction_type = input(Fore.GREEN + "\n Option: ")

        # [1] Show all object streams
        if extraction_type == '1':
            pdf_file = input(Fore.GREEN + " Enter the name of the PDF file to analyze: ")
            if pdf_file == '':
                pdf_file = default_pdf_file

            if not os.path.exists("objects_streams_list"):
                os.makedirs("objects_streams_list")
            clear_screen()
            object_stream_list(pdf_file)

            choice = input(Fore.LIGHTBLACK_EX + "\n Press Enter to continue...")
            if choice == '':
                clear_screen()
                print_banner()
                continue
            else:
                break

        # [2] Extract all object streams
        elif extraction_type == '2':
            pdf_file = input(Fore.GREEN + " Enter the name of the PDF file to analyze: ")
            if pdf_file == '':
                pdf_file = default_pdf_file
            extract_object_stream(pdf_file, -1, os.path.join('generated_files', 'all_objects.txt'))

            choice = input(Fore.LIGHTBLACK_EX + "\n Press Enter to continue...")
            if choice == '':
                clear_screen()
                print_banner()
                continue
            else:
                break

        # [3] Extract a specific object stream
        elif extraction_type == '3':
            pdf_file = input(Fore.GREEN + " Enter the name of the PDF file to analyze: ")
            if pdf_file == '':
                pdf_file = default_pdf_file
            object_stream_number = input(Fore.GREEN + " Enter the number of the object/stream to extract: ")
            try:
                object_stream_number = int(object_stream_number)
            except ValueError:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n [-] The object/stream number must be an integer.")
                choice = input(Fore.LIGHTBLACK_EX + "\n Press Enter to continue...")
                clear_screen()
                print_banner()
                continue
            if object_stream_number <= 0:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n [-] The object/stream number must be greater than zero.")
                choice = input(Fore.LIGHTBLACK_EX + "\n Press Enter to continue...")
                clear_screen()
                print_banner()
                continue
            if object_stream_number > len(open(pdf_file, 'rb').read().split(b'endobj')):
                print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n [-] The object/stream number is greater than the number of objects/streams in this PDF.")
                choice = input(Fore.LIGHTBLACK_EX + "\n Press Enter to continue...")
                clear_screen()
                print_banner()
                continue
            try:
                extract_object_stream(pdf_file, object_stream_number, os.path.join('generated_files', f'object_stream_{object_stream_number}.txt'))
                # Ask the user if they want to view the content of the object stream
                while True:
                    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\n Do you want to view the content of the object/stream?")
                    print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n  [1] ➙ Yes")
                    print("  [2] ➙ No")
                    choice = input(Fore.GREEN + "\n Option: ")
                    if choice == '1':
                        try:
                            print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + f"\n\n Content of object/stream {object_stream_number}:" + Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n" + "-" * 80 + Fore.WHITE + Style.BRIGHT + open(os.path.join('generated_files', f'object_stream_{object_stream_number}.txt'), 'r').read() + Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n" + "-" * 80)
                            choice = input(Fore.LIGHTBLACK_EX + "\n Press Enter to continue...")
                            clear_screen()
                            print_banner()
                            break
                        except UnicodeDecodeError:
                            print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] Unable to display the content of object/stream {object_stream_number}.")
                            choice = input(Fore.LIGHTBLACK_EX + "\n Press Enter to continue...")
                            clear_screen()
                            print_banner()
                            break
                        except FileNotFoundError:
                            print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] The file 'object_stream_{object_stream_number}.txt' was not found.")
                            choice = input(Fore.LIGHTBLACK_EX + "\n Press Enter to continue...")
                            clear_screen()
                            print_banner()
                            break
                    elif choice == '2':
                        clear_screen()
                        print_banner()
                        break
                    else:
                        clear_screen()
                        print(Fore.RED + Style.BRIGHT + "\n [-] Please enter 1 or 2 to select an option.")

            except FileNotFoundError:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + "\n [-] The PDF file was not found.")
                choice = input(Fore.LIGHTBLACK_EX + "\n Press Enter to continue...")
                clear_screen()
                print_banner()
                continue
            except Exception as e:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] An error occurred: {str(e)}")
                choice = input(Fore.LIGHTBLACK_EX + "\n Press Enter to continue...")
                clear_screen()
                print_banner()
                continue

        # [4] Extract FlateDecode content
        elif extraction_type == '4':
            pdf_file = input(Fore.GREEN + " Enter the name of the PDF file to analyze: ")
            if pdf_file == '':
                pdf_file = default_pdf_file
            extract_flatedecode(pdf_file, 'raw_flatedecode.txt')

            # Ask the user if they want to decode the content of FlateDecode
            while True:
                print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\n Do you want to decode (base64) the content of the object/stream?")
                print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n  [1] ➙ Yes")
                print("  [2] ➙ No")
                choice = input(Fore.GREEN + "\n Option: ")
                if choice == '1':
                    decode_flatedecode(os.path.join('generated_files', 'raw_flatedecode.txt'), 'decoded_flatedecode.jpg')  # Change the output file extension if necessary
                    choice = input(Fore.LIGHTBLACK_EX + "\n Press Enter to continue...")
                    clear_screen()
                    print_banner()
                    break
                elif choice == '2':
                    clear_screen()
                    print_banner()
                    break
                else:
                    clear_screen()
                    print(Fore.RED + Style.BRIGHT + "\n [-] Please enter 1 or 2 to select an option.")

        # [5] Remove generated files
        elif extraction_type == '5':
            try:
                remove_files()
                print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "\n [+] Generated files have been successfully removed.")
                choice = input(Fore.LIGHTBLACK_EX + "\n Press Enter to continue...")
                clear_screen()
                print_banner()
                continue
            except Exception as e:
                print(Fore.LIGHTRED_EX + Style.BRIGHT + f"\n [-] An error occurred: {str(e)}")
                choice = input(Fore.LIGHTBLACK_EX + "\n Press Enter to continue...")
                clear_screen()
                print_banner()
                continue

        # [6] Quit the program
        elif extraction_type == '6':
            clear_screen()
            break
        else:
            clear_screen()
            print(Fore.RED + Style.BRIGHT + "\n [-] Please enter a number between 1 and 5.")

# Launch the program
if __name__ == '__main__':
    if not os.path.exists('generated_files'):
        os.makedirs('generated_files')
    main()
