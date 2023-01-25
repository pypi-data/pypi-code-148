import os
import PyPDF2
from PIL import Image
import regex as re
import shutil
import keras
from keras.saving.save import load_model
from PIL import Image
from zipfile import ZipFile


import tensorflow as tf
import boto3


class ImagesExtractor(object):

    _save_to: str
    _page_counter: int
    _image_counter: int
    _file_name_only: str

    _COLOR_SPACES = {
        '/DeviceRGB': "RGB",
        '/DeviceCMYK': "CMYK",
        '/DeviceGray': "L"
    }

    _FILTER_TO_EXTENSION = {
        '/DCTDecode': '.jpg',
        '/JPXDecode': '.jp2'
    }

    def extract_dir(self, folder: str, save_to: str):
        """
        Extracts images from all PDF-files in a folder
        """
        assert os.path.isdir(folder), f"Not a folder: {folder}"

        files = os.listdir(folder)
        files = [os.path.join(folder, f) for f in files]
        files.sort()
        files = [f for f in files if f.lower().endswith('.pdf')]
        for f in files:
            print(f"File: {f}")
            self.extract_file(f, save_to)

    def extract_file(self, file: str, save_to: str):
        """
        Extracts images from single PDF-file
        """
        self._page_counter = 0
        self._image_counter = 0
        self._file_name_only = os.path.basename(file)

        assert os.path.isdir(save_to), f"Not a folder: {save_to}"
        self._save_to = save_to

        with open(file, "rb") as f:
            input1 = PyPDF2.PdfReader(f)
            for page in input1.pages:
                self._page_counter += 1
                try:
                    self._work_obj(page['/Resources']['/XObject'])
                except KeyError:
                    pass

    def _parse_image(self, obj):

        # All objects we need has dict as one of parent classes.
        if not isinstance(obj, dict):
            return

        try:
            subtype = obj['/Subtype']
        except (KeyError, TypeError) as e:
            return

        if subtype != '/Image':
            return

        size = (obj['/Width'], obj['/Height'])
        data = obj.get_data()
        cs = obj['/ColorSpace']
        try:
            mode = self._COLOR_SPACES[cs]
        except KeyError as e:
            raise ValueError(f'Unknown color space: {repr(cs)}')

        name_only = f"{self._file_name_only}_p{self._page_counter:03}_i{self._image_counter:05}-{mode}"
        full_name_wo_ext = os.path.join(self._save_to, name_only)

        filter_ = obj['/Filter']
        if filter_ == '/FlateDecode':
            img = Image.frombytes(mode, size, data)
            full_name = full_name_wo_ext + ".jpg"
            img.save(full_name, quality=95)
            img.close()
        elif filter_ in self._FILTER_TO_EXTENSION:
            ext = self._FILTER_TO_EXTENSION[filter_]
            full_name = full_name_wo_ext + ext
            with open(full_name, "wb") as save_file:
                save_file.write(data)
                save_file.close()
        else:
            raise ValueError(f"Unknown '/Filter' value: {repr(filter_)}")

        self._image_counter += 1
        print(f" - Saved {full_name}")


    def _work_obj(self, obj):
        self._parse_image(obj)
        if isinstance(obj, dict):
            for v in obj.keys():
                self._work_obj(obj[v])


class ClassifyFiles(object):
    def __init__(self, SAVE_IMAGES_HERE, classification_zip):
        self.SAVE_IMAGES_HERE = SAVE_IMAGES_HERE
        self.classification_zip = classification_zip
        self.images = []
        for i in os.listdir(self.SAVE_IMAGES_HERE):
            if i.endswith("jpg"):
                self.images.append(i)

        
        with ZipFile(self.classification_zip, 'r') as zObject:
            # Extracting all the members of the zip 
            # into a specific location.
            zObject.extractall(
            path = os.getcwd())
        self.model = load_model(f"{os.getcwd()}/classification")
        
        # print(self.images)

    def detectText(self, local_file):
        textract = boto3.client('textract', region_name='ap-south-1', aws_access_key_id = 'AKIAQQPQBRYJELWOPV7A', aws_secret_access_key= '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')

        with open(local_file,'rb') as document:
            response = textract.detect_document_text(Document={'Bytes': document.read()})
        text = ""
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                text = text + " " + item["Text"]
        
        return text


    def detect_pan(self, text):
        try:
            return re.search(r'\b[A-Z]{3}[PCHABGJLFT][A-Z]\d{3}[1-9][A-Z]\b', text).group(0)
        except AttributeError:
            None

    def detect_aadhaar(self, text):
        try:
            return re.search(r'\b[2-9]{1}\d{3}\s\d{4}\s\d{4}\b', text).group(0)
        except AttributeError:
            None

    def detect_passport(self, text):
        try:
            # return re.search(r'\b[A-PR-WY][1-9][0-9][0 ]\d{4}[1-9]\b', text).group(0)
            return re.search(r'\b[A-Z][ ][0-9][0-9]\d{4}[1-9]\b', text).group(0)
        except AttributeError:
            None

    def detect_driving_licence(self, text):
        try:
            return re.search(r'\b(([A-Z]{2}[0-9]{2})( )|([A-Z]{2}-[0-9]{2}))((19|20)[0-9][0-9])[0-9]{7}', text).group(0)
        except AttributeError:
            None

    def detect_cheque_leaf(self, text):
        try:
            return re.search(r'\b\d{6}\s\d{9}\s\d{6}\s\d{2}\b', text).group(0)
        except AttributeError:
            None

    def detect_voter_id(self, text):
        try:
            return re.search(r'\b[A-Z]{3}\d{7}\b', text).group(0)
        except AttributeError:
            None

    def classify(self):
        for img in self.images:
            # print(img)
            extracted_text = self.detectText(img)
            # print(extracted_text)
            # detected_text = self.detect_pan(extracted_text)
            
            try:
                l = self.detect_pan(extracted_text)
                if len(l) > 1 and "INCOME TAX DEPARTMENT" in l:
                    print(img, "PAN it is")
                    src_path = f"{self.SAVE_IMAGES_HERE}/{img}"
                    dst_path = f"{self.SAVE_IMAGES_HERE}/PAN/{img}"
                    try:
                        shutil.move(src_path, dst_path)
                    except:
                        os.mkdir(f"{self.SAVE_IMAGES_HERE}/PAN/{img}")
                        shutil.move(src_path, dst_path)

            except TypeError:
                None

            try:
                if len(self.detect_aadhaar(extracted_text)) > 1:
                    print(img, "Aadhaar it is")
                    src_path = f"{self.SAVE_IMAGES_HERE}/{img}"
                    dst_path = f"{self.SAVE_IMAGES_HERE}/Aadhaar/{img}"
                    try:
                        shutil.move(src_path, dst_path)
                    except:
                        os.mkdir(f"{self.SAVE_IMAGES_HERE}/Aadhaar/")
                        shutil.move(src_path, dst_path)

            except TypeError:
                None

            try:
                if len(self.detect_passport(extracted_text)) > 1:
                    print(img, "Passport it is")
                    src_path = f"{self.SAVE_IMAGES_HERE}/{img}"
                    dst_path = f"{self.SAVE_IMAGES_HERE}/Passport/{img}"
                    try:
                        shutil.move(src_path, dst_path)
                    except:
                        os.mkdir(f"{self.SAVE_IMAGES_HERE}/Passport/")
                        shutil.move(src_path, dst_path)

            except TypeError:
                None

            try:
                if len(self.detect_driving_licence(extracted_text)) > 1:
                    print(img, "Licence it is")
                    src_path = f"{self.SAVE_IMAGES_HERE}/{img}"
                    dst_path = f"{self.SAVE_IMAGES_HERE}/Licence/{img}"
                    try:
                        shutil.move(src_path, dst_path)
                    except:
                        os.mkdir(f"{self.SAVE_IMAGES_HERE}/Licence/")
                        shutil.move(src_path, dst_path)

            except TypeError:
                None

            try:
                if len(self.detect_cheque_leaf(extracted_text)) > 1:
                    print(img, "Cheque leaf it is")
                    src_path = f"{self.SAVE_IMAGES_HERE}/{img}"
                    dst_path = f"{self.SAVE_IMAGES_HERE}/Cheque_leaf/{img}"
                    try:
                        shutil.move(src_path, dst_path)
                    except:
                        os.mkdir(f"{self.SAVE_IMAGES_HERE}/Cheque_leaf/")
                        shutil.move(src_path, dst_path)

            except TypeError:
                None

            try:
                if len(self.detect_voter_id(extracted_text)) > 1:
                    print(img, "Voter ID it is")
                    src_path = f"{self.SAVE_IMAGES_HERE}/{img}"
                    dst_path = f"{self.SAVE_IMAGES_HERE}/Voter_ID/{img}"
                    try:
                        shutil.move(src_path, dst_path)
                    except:
                        os.mkdir(f"{self.SAVE_IMAGES_HERE}/Voter_ID/")
                        shutil.move(src_path, dst_path)

            except TypeError:
                None


    def classify_DL(self, img_path):

        self.decoder = {0: 'Aadhaar',
            1: 'Bank Statement',
            2: 'Cheque Leaf',
            3: 'Licence',
            4: 'ITR_Form 16',
            5: 'PAN',
            6: 'Passport',
            7: 'salary slip',
            8: 'utility',
            9: 'Voter_ID'}

        def preprocess(path):
            size = 200
            try:
                im = Image.open(path).resize((size,size)).convert("RGB")
                print(im)
            except:
                pass
                print("Went except")
            X = tf.keras.utils.img_to_array(im)
            return tf.reshape(X,[X.shape[0]//size,size,size,3])

        return self.decoder[self.model.predict(preprocess(img_path)).argmax()]
    
    def classify_left_over_imgs(self):
        left_over_imgs = []
        for i in os.listdir():
            if i.endswith("jpg"):
                left_over_imgs.append(i)
        
        for img in left_over_imgs:
            label = self.classify_DL(img)
            print(f"{img}, {label} it is")
            src_path = f"{self.SAVE_IMAGES_HERE}/{img}"
            dst_path = f"{self.SAVE_IMAGES_HERE}/{label}/{img}"
            try:
                shutil.move(src_path, dst_path)
            except:
                os.mkdir(f"{self.SAVE_IMAGES_HERE}/{label}/")
                shutil.move(src_path, dst_path)


class extract_info(object):
    def __init__(self, img_path):
        self.img_path = img_path

    def detectText(self, local_file):
        textract = boto3.client('textract', region_name='ap-south-1', aws_access_key_id = 'AKIAQQPQBRYJELWOPV7A', aws_secret_access_key= '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')

        with open(local_file,'rb') as document:
            response = textract.detect_document_text(Document={'Bytes': document.read()})
        text = ""
        for item in response["Blocks"]:
            if item["BlockType"] == "LINE":
                text = text + " " + item["Text"]
        return text
    def detect_pan(self, text):
        try:
            return re.search(r'\b[A-Z]{3}[PCHABGJLFT][A-Z]\d{3}[1-9][A-Z]\b', text).group(0)
        except AttributeError:
            None

    def detect_aadhaar(self, text):
        try:
            return re.search(r'\b[2-9]{1}\d{3}\s\d{4}\s\d{4}\b', text).group(0)
        except AttributeError:
            None

    def detect_passport(self, text):
        try:
            # return re.search(r'\b[A-PR-WY][1-9][0-9][0 ]\d{4}[1-9]\b', text).group(0)
            return re.search(r'\b[A-Z][ ]{0, 1}[0-9][0-9]\d{4}[1-9]\b', text).group(0)
        except AttributeError:
            None

    def detect_driving_licence(self, text):
        try:
            return re.search(r'\b(([A-Z]{2}[0-9]{2})( )|([A-Z]{2}-[0-9]{2}))((19|20)[0-9][0-9])[0-9]{7}', text).group(0)
        except AttributeError:
            None

    def detect_cheque_leaf(self, text):
        try:
            return re.search(r'\b\d{6}\s\d{9}\s\d{6}\s\d{2}\b', text).group(0)
        except AttributeError:
            None

    def detect_voter_id(self, text):
        try:
            return re.search(r'\b[A-Z]{3}\d{7}\b', text).group(0)
        except AttributeError:
            None

    def detect_date(self, text):
        try:
            # x = re.search("^([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])$|^([0-9][0-9]|19[0-9][0-9]|20[0-9][0-9])(\.|-|/)([1-9]|0[1-9]|1[0-2])(\.|-|/)([1-9]|0[1-9]|1[0-9]|2[0-9]|3[0-1])$",date)
            # x = re.search('\d{1,2}/\d{1,2}/\d{4}|\d{1,2}-\d{1,2}-\d{4}', text)
            x = re.search('\d{1,2}/\d{1,2}/\d{4}|\d{1,2}-\d{1,2}-\d{4}|\d{1,2}\.\d{1,2}\.\d{4}', text)
            return x.group()
        except:
            None

    def return_info(self):
        methods = [self.detect_date, self.detect_voter_id, self.detect_cheque_leaf, self.detect_driving_licence, 
                   self.detect_passport, self.detect_aadhaar, self.detect_pan]
        for i in methods:
            returner = i(self.detectText(self.img_path))
            if returner != None:
                print(f"{(str(i)).split(' ')[2].split('_')[-1].upper()} : {returner}")