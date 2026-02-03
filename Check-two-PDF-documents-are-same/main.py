from operator import contains
import os
import hashlib
import fitz
import difflib
from PIL import Image, ImageChops

file_path1 = "F:\\python-learning\\python-playground\\Check-two-PDF-documents-are-same\\file-sample1.pdf"
file_path2 = "F:\\python-learning\\python-playground\\Check-two-PDF-documents-are-same\\file-sample2.pdf"
file_path3 = "F:\\python-learning\\python-playground\\Check-two-PDF-documents-are-same\\sample_wrong.pdf"

class check_pdf():

    def __init__(self,arr,file_path1,file_path2,hash_file_algorithm='sha256'):
        self.arr = arr
        self.file_path1 = file_path1
        self.file_path2 = file_path2
        self.hash_file_algorithm = hash_file_algorithm
        
    def poceed(self):
        if('All' in self.arr):
            ResultArr = {}
            ResultArr['fileSizeResult'] = self.compair_file_size(self.file_path1,self.file_path2)
            ResultArr['HasFileResult'] = self.hash_file(self.file_path1,self.file_path2,self.hash_file_algorithm)
            ResultArr['TextCompResult'] = self.text_comp_by_page(self.file_path1,self.file_path2)
            ResultArr['VisualResult'] = self.visual_comparison(self.file_path1,self.file_path2)
            FinalResultMsg = {}
            FinalResultMsg['Finalresult'] = True
            for key,value in ResultArr.items():
                # Always create a dict first
                FinalResultMsg[key] = {
                    'code': value.get('code', False),
                    'msg': value.get('msg', '')
                }
                if value.get('code') == False:
                    FinalResultMsg['Finalresult'] = False
                # Optional fields
                if 'paragraf' in value:
                    FinalResultMsg[key]['paragraf'] = value['paragraf']

                if 'pages' in value:
                    FinalResultMsg[key]['pages'] = value['pages']
            return FinalResultMsg

    
    def compair_file_size(self,file_path1,file_path2):
        if os.path.exists(file_path1) and os.path.exists(file_path2):
            file_one_size = os.path.getsize(file_path1)
            file_two_size = os.path.getsize(file_path2)
            fileSizeResult = {}
            if file_one_size != file_two_size:
                fileSizeResult['code'] = False
                fileSizeResult['msg'] = 'file size are not match'
            else:
                fileSizeResult['code'] = True
                fileSizeResult['msg'] = 'file size are match'
            return fileSizeResult
    # withthis = compair_file_size(file_path1,file_path2)

    def hash_file(self,file_path1,file_path2,algorithm='sha256'):
        hash_func = hashlib.new(algorithm)
        HasFileResult = {}
        with open(file_path1,'rb') as file1:
            while chunk1 := file1.read(8192):
                hash_func.update(chunk1)
        file_one_hash = hash_func.hexdigest()
        hash_func2 = hashlib.new(algorithm)
        with open(file_path2,'rb') as file2:
            while chunk2 := file2.read(8192):
                hash_func2.update(chunk2)
        file_two_hash = hash_func2.hexdigest()
        if file_one_hash != file_two_hash:
            HasFileResult['code'] = False
            HasFileResult['msg'] = 'file hash are not match'
        else:
            HasFileResult['code'] = True
            HasFileResult['msg'] = 'file hash are match'
        return HasFileResult

    def text_comp_by_page(self,file_path1,file_path2):
        doc1 = fitz.open(file_path1)
        doc2 = fitz.open(file_path2)
        total_page = min(len(doc1),len(doc2))
        TextCompResult = {
            'code': True,
            'msg': 'Text is identical',
            'paragraf': []
        }
        for page_num in range(total_page):
            text1 = doc1[page_num].get_text().splitlines()
            text2 = doc2[page_num].get_text().splitlines()
            if text1 != text2:
                TextCompResult['code'] = False
                TextCompResult['msg'] = f"--- Difference found on Page {page_num + 1} ---"
                diff = difflib.unified_diff(text1,text2,lineterm='',fromfile=file_path1,tofile=file_path2)
                for line in diff:
                    TextCompResult['paragraf'].append(line)
                break

        doc1.close()
        doc2.close()

        return TextCompResult

    def visual_comparison(self,file_path1,file_path2):
        doc1 = fitz.open(file_path1)
        doc2 = fitz.open(file_path2)
        page_count = min(len(doc1),len(doc2))
        VisualResult = {
            'code': True,
            'msg': 'All pages are visually identical',
            'pages': []
        }
        for page_num in range(page_count):
            zoom = 2  # Adjust zoom for higher/lower precision
            mat = fitz.Matrix(zoom, zoom)

            pix1 = doc1[page_num].get_pixmap(matrix=mat)
            pix2 = doc2[page_num].get_pixmap(matrix=mat)

            img1 = Image.frombytes("RGB", [pix1.width, pix1.height], pix1.samples)
            img2 = Image.frombytes("RGB", [pix2.width, pix2.height], pix2.samples)

            diff = ImageChops.difference(img1, img2)

            bbox = diff.getbbox()

            if bbox:
                VisualResult['code'] = False
                VisualResult['pages'].append(page_num + 1)
                highlight = ImageChops.invert(diff)
                highlight.save(f"diff_page_{page_num + 1}.png")
            else:
                VisualResult['code'] = True
                VisualResult['msg'] = f"Page {page_num + 1} is visually identical."
        if not VisualResult['code']:
            VisualResult['msg'] = f"Visual differences found on pages {VisualResult['pages']}"
        doc1.close()
        doc2.close()
        return VisualResult

validate_pdf = check_pdf(['All'],file_path1,file_path2)
print(validate_pdf.poceed())