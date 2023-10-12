# Stream PDF 🇬🇧

This project is a Python script  designed for analyzing and extracting data from PDF files, with a focus in digital forensics, steganography, and CTF (Capture The Flag) challenges. I developed this script myself for the purpose of solving a RootMe challenge [PDF-Embedded](https://www.root-me.org/en/Challenges/Steganographie/PDF-Embedded).

Key features of the script include:

1. **Display Object/Stream Lists:** Users can access lists of objects and streams within a designated PDF file, allowing them to gain insights into the document's structure.

2. **Extract All Objects/Streams:** This functionality facilitates the extraction of all objects and streams from a PDF file, saving them in a generated file. (Note: This feature is not recommended for large PDF files, as it may cause the script to crash.)

3. **Extract Specific Object/Stream:** Users can extract a particular object or stream from a PDF by specifying its number.

4. **Extract FlateDecode:** The script is capable of extracting FlateDecode objects/streams from the PDF. Furthermore, users have the option to decode the content in base64 format, which is useful for revealing concealed information.

This project was developed to address the needs of those involved in digital forensics, steganography, and CTF challenges who work with PDF files and require a versatile tool for detailed analysis and data extraction.

French version [here](/README.md) 🇫🇷

## Demonstration
![](en_demo.gif)

## Installation

You can install the project by cloning the repository with the following command:

```
git clone https://github.com/CalValmar/Stream-pdf.git
```
And don't forget to install the requirements:
```
pip install -r requirements.txt
```


## Usage

To use the script, run the following command:

```
python3 stream-pdf.py
```

⚠️  Before running the script, you must move the PDF file you wish to analyze into the same directory as the script. Also, make sure to change the variable 'default_pdf_file' to the name of your PDF file to ease the process of running the script.

```
default_pdf_file = 'your_pdf_file.pdf'
```

⚠️  The 'bac2004.pdf' document is an example PDF file that can be used to test the script. You can delete it if you wish.


## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](/LICENSE) file for details.

GNU General Public License v3.0 © [CalValmar](https://github.com/CalValmar)

## Inspirations and Additional Information

- [FlateDecode](https://gist.github.com/averagesecurityguy/ba8d9ed3c59c1deffbd1390dafa5a3c2)
- [peepdf](https://eternal-todo.com/tools/peepdf-pdf-analysis-tool/)
