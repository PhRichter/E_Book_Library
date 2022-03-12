#!/usr/bin/python3

import subprocess

class VIEWER:
    def __init__(self, pdf_viewer="", epub_viewer=""):
        self.__pdf_viewer = pdf_viewer
        self.__epub_viewer = epub_viewer
        
    def open_pdf(self, path):
        subprocess.Popen("{} {}".format(self.__pdf_viewer, path))
        
    def open_epub(self, path):
        subprocess.Popen("{} {}".format(self.__epub_viewer, path))
        