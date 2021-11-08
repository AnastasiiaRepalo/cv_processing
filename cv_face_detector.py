import os
import pathlib

import cv2
import docx2txt
import fitz
import mtcnn
from werkzeug.utils import secure_filename

PDF_EXT = '.pdf'
faces_detector = mtcnn.MTCNN()


class CVFaceDetector:
    def __init__(self, file):
        self.file = file
        self.filename = secure_filename(self.file.filename)
        self.filepath = os.path.join('input_files/', self.filename)
        self.images_folder_name = 'photos/' + pathlib.Path(self.filename).stem + '/'
        self._process_file()

    def _save_file(self):
        os.makedirs('input_files/', exist_ok=True)
        self.file.save(self.filepath)

    def _make_folder_for_images(self):
        os.makedirs(self.images_folder_name, exist_ok=True)

    def _is_pdf(self):
        return os.path.basename(self.filename).endswith(PDF_EXT)

    def _save_images_pdf(self):
        pdf_file = fitz.open(self.filepath)
        number_of_pages = len(pdf_file)
        image_index = 1
        for current_page_index in range(number_of_pages):
            for img_index, img in enumerate(pdf_file.getPageImageList(current_page_index)):
                xref = img[0]
                image = fitz.Pixmap(pdf_file, xref)
                if image.n < 5:
                    image.writePNG(f"{self.images_folder_name}/image{image_index}.jpg")
                else:
                    new_image = fitz.Pixmap(fitz.csRGB, image)
                    new_image.writePNG(f"{self.images_folder_name}/image{image_index}.jpg")
                image_index += 1

    def _save_images_docx(self):
        docx2txt.process(self.filepath, self.images_folder_name)

    def _process_file(self):
        self._save_file()
        self._make_folder_for_images()
        if self._is_pdf():
            self._save_images_pdf()
        else:
            self._save_images_docx()

    def _get_faces_positions(self, image_path):
        image = cv2.imread(image_path)
        faces = faces_detector.detect_faces(image)
        faces_list = []
        if faces:
            for face in faces:
                face_coords_dict = {}
                x, y, width, height = face['box']
                confidence = face['confidence']
                face_coords_dict['x0'] = x
                face_coords_dict['y0'] = y
                face_coords_dict['x1'] = x + width
                face_coords_dict['y1'] = y + height
                face_coords_dict['conf'] = f'{confidence:.2f}'
                face_coords_dict['image_width'] = image.shape[1]
                face_coords_dict['image_height'] = image.shape[0]
                faces_list.append(face_coords_dict)
        return faces_list

    def get_output_json(self):
        images_with_faces = {}
        images = os.listdir(self.images_folder_name)
        images.sort(key=lambda x: int(list(x.split('.')[0])[-1]))
        for index, image in enumerate(images):
            extracted_faces_list = self._get_faces_positions(self.images_folder_name + image)
            images_with_faces['image_' + str(index)] = extracted_faces_list
        return {'images_with_faces': [images_with_faces]}




