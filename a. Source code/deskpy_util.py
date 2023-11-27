import os
from PIL import Image
from PyQt6.QtWidgets import QMessageBox
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
from plyer import notification

class Util():
    def pdf_from_img(self):
        self.cleanner = []
        self.ids_to_move = []
        self.wf_tree = os.listdir(self.working_folder)
        for leaf in self.wf_tree:
            _leaf = leaf.lower()
            # Formats supported: .png, .jpg, .jpeg, .svg, .gif, .webp, .bmp, .tif, .jfif
            if _leaf.__contains__('.png') or _leaf.__contains__('.jpg') or _leaf.__contains__('.jpeg') or _leaf.__contains__('.svg') or _leaf.__contains__('.gif') or _leaf.__contains__('.webp') or _leaf.__contains__('.bmp') or _leaf.__contains__('.tif') or _leaf.__contains__('.jfif'):
                if _leaf.__contains__('id.') or _leaf.__contains__('id1') or _leaf.__contains__('id2'):self.ids_to_move.append(f'{self.working_folder}/{leaf}')
                else:self.cleanner.append(f'{self.working_folder}/{leaf}')
                _img = Image.open(f'{self.working_folder}/{leaf}')
                _img = _img.convert('RGB')
                _cnv = f'{self.working_folder}/{leaf}'
                _cnv = _cnv.replace('.png','').replace('.jpg','').replace('.jpeg','').replace('.svg','').replace('.gif','').replace('.webp','').replace('.bmp','').replace('.tif','').replace('.jfif','')
                _img.save(f'{_cnv}.pdf')
        if len(self.cleanner) > 0:
            for c in self.cleanner:
                try:
                    os.remove(c)
                    _c = c.split('/')
                    _c = _c[-1]
                except Exception as e: pass

    def build_up_folders(self):
        try: os.makedirs(f'{self.working_folder}/0. OTROS DOCUMENTOS')
        except Exception as e: notification.notify(title = f'DeskPy',message = f'Hint: {e.__class__}\n.Function: def build_up_folders(self)\nDeskPy raised error while building up folder: "0. OTROS DOCUMENTOS"',timeout = 5)
        try: os.makedirs(f'{self.working_folder}/1. INFORMACIÓN GENERAL')
        except Exception as e: notification.notify(title = f'DeskPy',message = f'Hint: {e.__class__}\n.Function: def build_up_folders(self)\nDeskPy raised error while building up folder: "1. INFORMACIÓN GENERAL"',timeout = 5)
        try: os.makedirs(f'{self.working_folder}/2. INFORMACIÓN PRODUCTO')
        except Exception as e: notification.notify(title = f'DeskPy',message = f'Hint: {e.__class__}\n.Function: def build_up_folders(self)\nDeskPy raised error while building up folder: "2. INFORMACIÓN PRODUCTO"',timeout = 5)
        try: os.makedirs(f'{self.working_folder}/3. INFORMACIÓN FINANCIERA')
        except Exception as e: notification.notify(title = f'DeskPy',message = f'Hint: {e.__class__}\n.Function: def build_up_folders(self)\nDeskPy raised error while building up folder: "3. INFORMACIÓN FINANCIERA"',timeout = 5)

    def pdf_make_merge(self):
        self.ids_for_merge = []
        self.wf_tree = os.listdir(self.working_folder)
        for leaf in self.wf_tree:
            _leaf = leaf.lower()
            if _leaf.__contains__('.pdf'):
                if _leaf.__contains__('id.') or _leaf.__contains__('id1') or _leaf.__contains__('id2'):
                    self.ids_for_merge.append(leaf)
        if len(self.ids_for_merge) == 2:
            _merge = PdfMerger()
            _merge.append(f'{self.working_folder}/{self.ids_for_merge[0]}')
            _merge.append(f'{self.working_folder}/{self.ids_for_merge[1]}')
            _merged = f'{self.working_folder}/1. INFORMACIÓN GENERAL/ID {self.editf_id.text()} {self.editf_fn.text()}.pdf'
            with open(_merged,'wb') as f:
                _merge.write(f)
                _merge.close()
                f.close()
            try: os.remove(f'{self.working_folder}/{self.ids_for_merge[0]}')
            except: pass
            try: os.remove(f'{self.working_folder}/{self.ids_for_merge[1]}')
            except: pass
        for id in self.ids_to_move:
            id_output = f'{self.working_folder}/0. OTROS DOCUMENTOS/ID CARA {self.ids_to_move.index(id)+1} {self.editf_id.text()} {self.editf_fn.text()}.png'
            os.rename(id,id_output)

    def pdf_from_pdf(self):
        items = os.listdir(self.working_folder)
        self.relocate_pdf = []
        for item in items:
            _item = item.lower()
            if _item.__contains__('.pdf'):
                if not _item.__contains__('aff'): self.relocate_pdf.append(f'{self.working_folder}/{item}')
                else: self.aff = f'{self.working_folder}/{item}'
        _reader = PdfReader(self.aff)
        for n in self.is_doc_scrt:
            self.is_doc_fkyc.append(n)
            self.is_doc_ccac.append(n)
            self.is_doc_cons.append(n)
            self.is_doc_cntr.append(n)
            self.is_doc_unkn.append(n)
        try:
            _writer = PdfWriter()
            for p in self.is_doc_fkyc:
                _writer.add_page(_reader.pages[p])
                _output = f'{self.working_folder}/1. INFORMACIÓN GENERAL/KYC {self.editf_id.text()} {self.editf_fn.text()}.pdf'
                with open(_output,'wb') as f:
                    _writer.write(f)
                    f.close()
        except Exception as e: notification.notify(title = f'DeskPy',message = f'Hint: {e.__class__}\n.Function: def pdf_from_pdf(self)\nProcessing: self.is_doc_fkyc',timeout = 5)
        try:
            _writer = PdfWriter()
            for p in self.is_doc_ccac:
                _writer.add_page(_reader.pages[p])
                _output = f'{self.working_folder}/1. INFORMACIÓN GENERAL/CICAC {self.editf_id.text()} {self.editf_fn.text()}.pdf'
                with open(_output,'wb') as f:
                    _writer.write(f)
                    f.close()
        except Exception as e: notification.notify(title = f'DeskPy',message = f'Hint: {e.__class__}\n.Function: def pdf_from_pdf(self)\nProcessing: self.is_doc_ccac',timeout = 5)
        try:
            _writer = PdfWriter()
            for p in self.is_doc_cons:
                _writer.add_page(_reader.pages[p])
                _output = f'{self.working_folder}/1. INFORMACIÓN GENERAL/CONSENTIMIENTO INFORMADO {self.editf_id.text()} {self.editf_fn.text()}.pdf'
                with open(_output,'wb') as f:
                    _writer.write(f)
                    f.close()
        except Exception as e: notification.notify(title = f'DeskPy',message = f'Hint: {e.__class__}\n.Function: def pdf_from_pdf(self)\nProcessing: self.is_doc_cons',timeout = 5)
        try:
            _writer = PdfWriter()
            for p in self.is_doc_cntr:
                _writer.add_page(_reader.pages[p])
                _output = f'{self.working_folder}/2. INFORMACIÓN PRODUCTO/CONTRATO {self.editf_id.text()} {self.editf_fn.text()}.pdf'
                with open(_output,'wb') as f:
                    _writer.write(f)
                    f.close()
        except Exception as e: notification.notify(title = f'DeskPy',message = f'Hint: {e.__class__}\n.Function: def pdf_from_pdf(self)\nProcessing: self.is_doc_cntr',timeout = 5)
        if len(self.is_doc_unkn) > 2:
            QMessageBox.warning(
                self,
                'DeskPy', f'Some of the pages in the document could not be recognized by the program, yet it has been saved to protect the information and prevent loss of data (page or pages).\n\nWhen the document is not recognized, the signature certification is automatically added to it.',
                QMessageBox.StandardButton.Close)
            try:
                _writer = PdfWriter()
                for p in self.is_doc_unkn:
                    _writer.add_page(_reader.pages[p])
                    _output = f'{self.working_folder}/(unidentified document) {self.editf_id.text()} {self.editf_fn.text()}.pdf'
                    with open(_output,'wb') as f:
                        _writer.write(f)
                        f.close()
            except Exception as e: notification.notify(title = f'DeskPy',message = f'Hint: {e.__class__}\n.Function: def pdf_from_pdf(self)\nProcessing: self.is_doc_unkn',timeout = 5)
        try: os.rename(self.aff,f'{self.working_folder}/0. OTROS DOCUMENTOS/KIT {self.editf_id.text()} {self.editf_fn.text()}.pdf')
        except Exception as e: print(e)
        self.aux_a = 1
        self.aux_b = 1

        # Additional docs (just rename and relocate).
        for r in self.relocate_pdf:
            _r = r.lower()
            if _r.__contains__('id.') or _r.__contains__('id1'): os.rename(r,f'{self.working_folder}/1. INFORMACIÓN GENERAL/ID {self.editf_id.text()} {self.editf_fn.text()}.pdf')
            elif _r.__contains__('buro') or _r.__contains__('buró') or _r.__contains__('gente') or _r.__contains__('multi'): os.rename(r,f'{self.working_folder}/1. INFORMACIÓN GENERAL/BURÓ {self.editf_id.text()} {self.editf_fn.text()}.pdf')
            elif _r.__contains__('firma'): os.rename(r,f'{self.working_folder}/0. OTROS DOCUMENTOS/FIRMA REPRESENTANTE LEGAL {self.editf_id.text()} {self.editf_fn.text()}.pdf')
            elif _r.__contains__('form'): os.rename(r,f'{self.working_folder}/0. OTROS DOCUMENTOS/FORMULARIO MANUAL {self.editf_id.text()} {self.editf_fn.text()}.pdf')
            elif _r.__contains__('rep') or _r.__contains__('fs'): os.rename(r,f'{self.working_folder}/1. INFORMACIÓN GENERAL/REPORTE ONFIDO {self.editf_id.text()} {self.editf_fn.text()}.pdf')
            elif _r.__contains__('orden'):
                os.rename(r,f'{self.working_folder}/3. INFORMACIÓN FINANCIERA/ORDEN PATRONAL {self.aux_a} {self.editf_id.text()} {self.editf_fn.text()}.pdf')
                self.aux_a += 1
            elif _r.__contains__('origen'):
                os.rename(r,f'{self.working_folder}/3. INFORMACIÓN FINANCIERA/ORIGEN DE FONDOS {self.aux_b} {self.editf_id.text()} {self.editf_fn.text()}.pdf')
                self.aux_b += 1
            else:
                _r_ = _r.split('/')
                _r_ = _r_[-1]
                _r_ = _r_.replace('.pdf','').upper()
                os.rename(r,f'{self.working_folder}/{_r_} {self.editf_id.text()} {self.editf_fn.text()}.pdf')