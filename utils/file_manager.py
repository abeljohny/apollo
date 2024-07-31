import base64
import io
import os
import zipfile
from typing import AnyStr

import PyPDF2
import fitz

from constants import SupportedFileTypes


class FileManager(object):
    """Manages Disk read-writes and File-Type Parsing"""

    def __init__(self):
        pass

    @staticmethod
    def file_exists(filepath: str) -> bool:
        """Checks if filepath exists.
        :param filepath: file path
        """
        return os.path.exists(filepath)

    @staticmethod
    def read_file(filepath: str) -> AnyStr:
        if FileManager.file_exists(filepath):
            with open(filepath, "r") as file:
                return file.read()

    @staticmethod
    def file_extension(filename):
        _, file_extension = os.path.splitext(filename)
        return file_extension

    @staticmethod
    def remove_non_printable_chars(s):
        return "".join(c for c in s if c.isprintable())

    @staticmethod
    def base64_to_text(base64_pdf, decode=True) -> str:
        if decode:
            pdf_data = base64.b64decode(base64_pdf)
        else:
            pdf_data = base64_pdf

        pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
        text: str = ""
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

        return FileManager.remove_non_printable_chars(text).strip()

    @staticmethod
    def read_pdf(pdf_file):
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        # Extract text from each page
        pdf_text = ""
        for page in pdf_reader.pages:
            pdf_text += page.extract_text() + "\n"
        return pdf_text

    @staticmethod
    def parse_file(file) -> str:
        file_extension = FileManager.file_extension(file["file_name"])
        match file_extension:
            case SupportedFileTypes.PDF.value:
                return FileManager.base64_to_text(file["file_contents"])
            case SupportedFileTypes.ZIP.value:
                contents = []
                zip_contents = base64.b64decode(file["file_contents"])
                with zipfile.ZipFile(io.BytesIO(zip_contents), "r") as zip_ref:
                    for file_name in zip_ref.namelist():
                        if file_name.startswith(
                            "__MACOSX/"
                        ):  # ignore the __MACOSX directory (if present) appended by Apple to ZIP files
                            continue
                        with zip_ref.open(file_name) as pdf_file:
                            contents.append(FileManager.read_pdf(pdf_file))
                return "".join(contents)
