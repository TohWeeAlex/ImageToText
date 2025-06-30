import os
from os import listdir
from os.path import isfile, join
from pathlib import Path

from alive_progress import alive_bar    ## Package for progress bar

import pytesseract                      ## Package for image text recognition

from natsort import os_sorted           ## Package for filename sorting

from pypdf import PdfWriter             ## Package for PDF merging

import fitz                             ## Package for PDF to PNG converstion

# Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def pdf_readers(pdfFilepath):
    pdfReader = fitz.open(pdfFilepath)
    return pdfReader

def folder_create(folder_name):
    try:
        os.makedirs(folder_name)
    except FileExistsError:
        # directory already exists
        pass

def transcribing(pdf_Filepath):

    pdfReader = pdf_readers("input/" + pdf_Filepath)

    merger = PdfWriter()

    # Loop over pages and convert pages to jpg
    with alive_bar(len(pdfReader)) as bar:
        for i in range(len(pdfReader)):
            page = pdfReader.load_page(i)
            pixmap = page.get_pixmap(dpi=300)
            pixmap.save(f"compiler/output_{i:03d}.png")
            pdf = pytesseract.image_to_pdf_or_hocr(f"compiler/output_{i:03d}.png", extension='pdf')
            with open(f'compiler/output_{i:03d}.pdf', 'w+b') as f:
                f.write(pdf) # pdf type is bytes by default
                os.remove(f"compiler/output_{i:03d}.png")
            single_pdf = open(f'compiler/output_{i:03d}.pdf', "rb")
            merger.append(single_pdf)
            single_pdf.close()
            os.remove(f'compiler/output_{i:03d}.pdf')
            bar()

    merger.write("output/" + pdf_Filepath[:-4] + "_transcribed.pdf")
    merger.close()

def main():
    input_folder = [f for f in listdir("input") if (isfile(join("input", f)) and f.lower().endswith((".pdf")))]

    print(input_folder)

    # folder creation
    folder_create("output")
    folder_create("compiler")

    # Loop through pdf files
    for file in input_folder:
        print("\nNow transcribing: " + file)
        transcribing(file)
        print()

if __name__ == "__main__":
    main()
