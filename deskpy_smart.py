import os
from PyPDF2 import PdfReader
import re
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

        self.readable_doc_c2 = False
        self.fields_aux_mode = False

        for st in self.subtree:
            _st = st.lower()
            if _st.__contains__('aff'):
                self.reading_doc = f'{self.working_folder}/{st}'

        self._pdf = open(self.reading_doc, 'rb')
        _reader = PdfReader(self._pdf)
        _pages = _reader.pages
        _length = _pages.__len__()

        for n in range(_length):
            _raw_text = _pages[n].extract_text().replace('\n',' ')
            _raw_text = _raw_text.lower()

            # INFORMED CONSENT.
            if _raw_text.__contains__('consentimiento informado') and _raw_text.__contains__('constan en este documento') and _raw_text.__contains__('me encuentro conforme') and _raw_text.__contains__('derecho a solicitar'): self.is_doc_cons.append(n)
            elif _raw_text.__contains__('consentimiento') and _raw_text.__contains__('informado') and _raw_text.__contains__('empresas asociadas') and _raw_text.__contains__('base de datos'): self.is_doc_cons.append(n)
            elif _raw_text.__contains__('consentimiento informado') and _raw_text.__contains__('para lo dispuesto') and _raw_text.__contains__('h)') and _raw_text.__contains__('me encuentro conforme'): self.is_doc_cons.append(n)

            # CONTRACT.
            elif _raw_text.__contains__('objeto del presente mandato') and _raw_text.__contains__('generar y custodiar los valores') and _raw_text.__contains__('poder especial') and _raw_text.__contains__('la firma de este documento'): self.is_doc_cntr.append(n)
            elif _raw_text.__contains__('presente contrato') and _raw_text.__contains__('respectivo certificado') and _raw_text.__contains__('forma definitiva') and _raw_text.__contains__('intereses correspondientes'): self.is_doc_cntr.append(n)
            elif _raw_text.__contains__('contrato inversion smart') or _raw_text.__contains__('contrato inversión smart'): self.is_doc_cntr.append(n)
            elif _raw_text.__contains__('quinta') and _raw_text.__contains__('octava') and _raw_text.__contains__('novena'): self.is_doc_cntr.append(n)
            elif _raw_text.__contains__('contrato') and _raw_text.__contains__('cuenta smart') and _raw_text.__contains__('certificados') and _raw_text.__contains__('expresa e'): self.is_doc_cntr.append(n)

            # KYC.
            elif _raw_text.__contains__('formulario') and _raw_text.__contains__('conozca a su cliente'):
                self.is_doc_fkyc.append(n)
                self._data_set_from_kyc = _pages[n].extract_text().replace('\xa0','').split('\n')

            elif _raw_text.__contains__('declaro') and _raw_text.__contains__('juramento') and _raw_text.__contains__('todas las consecuencias') and _raw_text.__contains__('expresamente acepto que'): self.is_doc_fkyc.append(n)
            elif _raw_text.__contains__('se hace constar que') and _raw_text.__contains__('puede llenar') and _raw_text.__contains__('no gestionar'): self.is_doc_fkyc.append(n)
            elif _raw_text.__contains__('fatca') and _raw_text.__contains__('favor completar') and _raw_text.__contains__('y firmar') and _raw_text.__contains__('llenar este formulario') and _raw_text.__contains__('expresamente acepto'):
                self.is_doc_fkyc.append(n)
                self.get_text_from_scert = True

            # CICAC
            elif _raw_text.__contains__('consulta de datos') and _raw_text.__contains__('expediente del centro') and _raw_text.__contains__('conozca a su cliente') and _raw_text.__contains__('cicac'):
                self.is_doc_ccac.append(n)
                self._data_set_from_cicac = _pages[n].extract_text().replace('\xa0','').split('\n')

            elif _raw_text.__contains__('conozca a su cliente') and _raw_text.__contains__('cicac') and _raw_text.__contains__('yo,') and _raw_text.__contains__('firma'):
                self.is_doc_ccac.append(n)
                self._data_set_from_cicac = _pages[n].extract_text().replace('\xa0','').split('\n')

            # SIGN CERTIFICATION
            elif _raw_text.__contains__('consta la siguiente') and _raw_text.__contains__('generada a partir de la firma') and _raw_text.__contains__('para verificar la identidad') and _raw_text.__contains__('prueba documental'): self.is_doc_scrt.append(n)
            elif _raw_text.__contains__('firmante') and _raw_text.__contains__('cado mediante') and _raw_text.__contains__('contenido a firmar') and _raw_text.__contains__('url'): self.is_doc_scrt.append(n)
            elif _raw_text.__contains__('firmante') and _raw_text.__contains__('cado mediante') and _raw_text.__contains__('seguridad pin'): self.is_doc_scrt.append(n)

            # UNKNOWN PAGES.
            else: self.is_doc_unkn.append(n)

        if not self.readable_doc_c2:
            try:
                for kt in self._data_set_from_cicac:
                    _kt = kt.lower()
                    if _kt.__contains__('yo') and _kt.__contains__('portador de') and _kt.__contains__('de forma expresa'):
                        self._data_set_from_cicac = kt
                        break

                self._data_set_from_cicac = self._data_set_from_cicac.split(',')
                self._data_set_from_cicac[0] = self._data_set_from_cicac[0].replace('Yo ','').replace('yo ','')

                self.result_id = ''

                for char in self._data_set_from_cicac[1]:
                    n = char.isnumeric()
                    if n: self.result_id += char

                self.result_fn = self._data_set_from_cicac[0]
                self.result_fn = self.result_fn.upper().replace('  ',' ')
                self.result_fn = self.result_fn.split(' ')

            except:
                for kt in self._data_set_from_kyc:
                    _kt = kt.lower()
                    if _kt.__contains__('yo') and _kt.__contains__('portador de') and _kt.__contains__('de forma expresa'):
                        self._data_set_from_kyc = kt
                        break

                self._data_set_from_kyc = ' '.join(self._data_set_from_kyc)
                self._data_set_from_kyc = self._data_set_from_kyc.split('-20')
                self._data_set_from_kyc = self._data_set_from_kyc[1]
                self._data_set_from_kyc = self._data_set_from_kyc.lower()
                self._data_set_from_kyc = self._data_set_from_kyc.split(' ')

                for rd in self._data_set_from_kyc:
                    x = re.search(r'\d{9,}', rd)
                    if x:
                        self.result_id = rd
                        break

                self._data_set_from_kyc = ' '.join(self._data_set_from_kyc)
                self._data_set_from_kyc = self._data_set_from_kyc.split(' 20')
                self._data_set_from_kyc = self._data_set_from_kyc[0]
                self._data_set_from_kyc = self._data_set_from_kyc.split(' ')
                self._data_set_from_kyc = self._data_set_from_kyc[1:]

                self.result_fn = []

                for string in self._data_set_from_kyc:
                    if string.strip() != '': self.result_fn.append(string)

        else:
            self.result_fn = f'{self._data_set_from_cicac[17]} {self._data_set_from_cicac[18]}'
            self.result_fn = self.result_fn.split(' ')
            self.result_id = self._data_set_from_cicac[20]
            self.result_id = self.result_id.split(' ')
            self.result_id = self.result_id[0]

        try:
            sz = len(self.result_fn)
            if sz == 2: self.result_fn = self.result_fn.reverse()
            elif sz == 3: self.result_fn = f'{self.result_fn[-2]} {self.result_fn[-1]} {self.result_fn[0]}'
            elif sz == 4: self.result_fn = f'{self.result_fn[-2]} {self.result_fn[-1]} {self.result_fn[0]} {self.result_fn[1]}'
            elif sz > 4:
                self.result_fn = f'{self.result_fn[:-2]} {self.result_fn[-2]} {self.result_fn[-1]}'
                self.result_fn = self.result_fn.replace('[','').replace(']','').replace(',','').replace("'",'')
        except Exception as e: print(e)

        self._pdf.close()

    def app_deploy(self):
        try: self.id = self.editf_id.text()
        except: print('Hint: self.id = self.editf_id.text()')

        try: self.fn = self.editf_fn.text()
        except: print('Hint: self.id = self.editf_fn.text()')

        Util.pdf_from_img(self)
        Util.build_up_folders(self)
        Util.pdf_make_merge(self)
        Util.pdf_from_pdf(self)

        try:
            if self.bt_sender == 'Uno':
                output_f = self.working_folder.split('/')
                output_f = output_f[:-2]
                output_f = '/'.join(output_f)
                output_f = f'{output_f}/{self.editf_id.text()} {self.editf_fn.text()}'
                os.rename(self.working_folder,output_f)
                self.crud_read.setDisabled(True)
                self.crud_create.setDisabled(True)
                self.crud_auto.setDisabled(True)
                notification.notify(
                    title = f'DeskPy',
                    message = f'Expediente "{self.editf_id.text()} {self.editf_fn.text()}" completado.',
                    timeout = 5
                )
            elif self.bt_sender == 'Todo':
                output_f = f'{self.sys_path.text()}{self.editf_id.text()} {self.editf_fn.text()}'
                os.rename(self.working_folder,output_f)
        except Exception as e:
            notification.notify(
                title = f'DeskPy',
                message = f'Hint: {e.__class__}\n.Function: def app_deploy(self)\nProcessing: os.rename(self.working_folder,output_f)',
                timeout = 5
            )