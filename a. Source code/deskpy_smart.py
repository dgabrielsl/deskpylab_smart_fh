import os
from PyPDF2 import PdfReader
from plyer import notification
from deskpy_util import Util

class PDF():
    def pdf_srch_text(self):
        self.is_doc_fkyc = []       # KYC form.                     ✅ 2 pags
        self.is_doc_ccac = []       # CICAC.                        ✅ 1 pag.
        self.is_doc_cons = []       # Consent.                      ✅ 1 pag.
        self.is_doc_cntr = []       # Contract.                     ✅ 2 pags.
        self.is_doc_scrt = []       # Sign's certification.         ✅ 2 pags.
        self.is_doc_unkn = []       # Possible unknown pages.       ✅ aux **pags.
        self.subtree = os.listdir(self.working_folder)
        for st in self.subtree:
            _st = st.lower()
            if _st.__contains__('aff'):
                self.reading_doc = f'{self.working_folder}/{st}'
        _pdf = open(self.reading_doc, 'rb')
        _reader = PdfReader(_pdf)
        _pages = _reader.pages
        _length = _pages.__len__()
        for n in range(_length):
            _raw_text = _pages[n].extract_text().replace('\n',' ')
            _raw_text = _raw_text.lower()
            if _raw_text.__contains__('consentimiento informado') and _raw_text.__contains__('constan en este documento') and _raw_text.__contains__('me encuentro conforme') and _raw_text.__contains__('derecho a solicitar'): self.is_doc_cons.append(n)
            elif _raw_text.__contains__('objeto del presente mandato') and _raw_text.__contains__('generar y custodiar los valores') and _raw_text.__contains__('poder especial') and _raw_text.__contains__('la firma de este documento'): self.is_doc_cntr.append(n)
            elif _raw_text.__contains__('presente contrato') and _raw_text.__contains__('respectivo certificado') and _raw_text.__contains__('forma definitiva') and _raw_text.__contains__('intereses correspondientes'): self.is_doc_cntr.append(n)
            elif _raw_text.__contains__('formulario') and _raw_text.__contains__('conozca a su cliente') and _raw_text.__contains__('producto o servicio') and _raw_text.__contains__('completar y firmar'): self.is_doc_fkyc.append(n)
            elif _raw_text.__contains__('declaro') and _raw_text.__contains__('juramento') and _raw_text.__contains__('todas las consecuencias') and _raw_text.__contains__('expresamente acepto que'): self.is_doc_fkyc.append(n)
            elif _raw_text.__contains__('consulta de datos') and _raw_text.__contains__('expediente del centro') and _raw_text.__contains__('conozca a su cliente') and _raw_text.__contains__('cicac'):
                self.is_doc_ccac.append(n)
                self._data_set = _pages[n].extract_text().replace('\xa0','').split('\n')
            elif _raw_text.__contains__('consta la siguiente') and _raw_text.__contains__('generada a partir de la firma') and _raw_text.__contains__('para verificar la identidad') and _raw_text.__contains__('prueba documental'): self.is_doc_scrt.append(n)
            elif _raw_text.__contains__('firmante') and _raw_text.__contains__('autenticado mediante') and _raw_text.__contains__('contenido a firmar disponible') and _raw_text.__contains__('url'): self.is_doc_scrt.append(n)
            else: self.is_doc_unkn.append(n)
        for kt in self._data_set:
            _kt = kt.lower()
            if _kt.__contains__('yo') and _kt.__contains__('portador de') and _kt.__contains__('de forma expresa'):
                self._data_set = kt
                break
        try:
            self._data_set = self._data_set.split(',')
            self._data_set[0] = self._data_set[0].replace('Yo ','').replace('yo ','')
            self.result_id = ''
            for char in self._data_set[1]:
                n = char.isnumeric()
                if n: self.result_id += char
            self.result_fn = self._data_set[0]
            self.result_fn = self.result_fn.upper().replace('  ',' ')
            self.result_fn = self.result_fn.split(' ')
            sz = len(self.result_fn)
            if sz == 2: self.result_fn = self.result_fn.reverse()
            elif sz == 3: self.result_fn = f'{self.result_fn[-2]} {self.result_fn[-1]} {self.result_fn[0]}'
            elif sz == 4: self.result_fn = f'{self.result_fn[-2]} {self.result_fn[-1]} {self.result_fn[0]} {self.result_fn[1]}'
            elif sz > 4: self.result_fn = f'{self.result_fn[:-2]} {self.result_fn[-2]} {self.result_fn[-1]}'
            self._data_set = ''
            _pdf.close()
        except Exception as e: notification.notify(title=f'DeskPy',message=f'Hint: {e.__class__}\n.Function: def pdf_srch_text(self)\nProcessing: self._data_set',timeout=5)

    def app_deploy(self):
        self.id = self.editf_id.text()
        self.fn = self.editf_fn.text()
        Util.pdf_from_img(self)
        Util.build_up_folders(self)
        Util.pdf_make_merge(self)
        Util.pdf_from_pdf(self)
        try:
            # if self.bt_sender == 'Uno':
            #     output_f = self.working_folder.split('/')
            #     output_f = output_f[:-2]
            #     output_f = '/'.join(output_f)
            #     output_f = f'{output_f}/{self.editf_id.text()} {self.editf_fn.text()}'
            # elif self.bt_sender == 'Grupo': pass
            # elif self.bt_sender == 'Todo':
            #     output_f = f'{self.working_folder}/{self.editf_id.text()} {self.editf_fn.text()}'
            #     print(f'self.working_folder: {self.working_folder}')
            #     print(f'output_f: {output_f}')

            # os.rename(self.working_folder,output_f)

            if self.bt_sender == 'Uno':
                output_f = self.working_folder.split('/')
                output_f = output_f[:-2]
                output_f = '/'.join(output_f)
                output_f = f'{output_f}/{self.editf_id.text()} {self.editf_fn.text()}'
                print(output_f)
                os.rename(self.working_folder,output_f)
                self.crud_read.setDisabled(True)
                self.crud_create.setDisabled(True)
                self.crud_auto.setDisabled(True)
                notification.notify(title=f'DeskPy',message=f'Expediente "{self.editf_id.text()} {self.editf_fn.text()}" completado.',timeout=5)
            elif self.bt_sender == 'Todo':
                output_f = f'{self.sys_path.text()}{self.editf_id.text()} {self.editf_fn.text()}'
                os.rename(self.working_folder,output_f)
        except Exception as e: notification.notify(title=f'DeskPy',message=f'Hint: {e.__class__}\n.Function: def app_deploy(self)\nProcessing: os.rename(self.working_folder,output_f)',timeout=5)