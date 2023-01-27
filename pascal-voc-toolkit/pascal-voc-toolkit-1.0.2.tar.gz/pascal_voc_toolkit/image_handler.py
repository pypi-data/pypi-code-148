import logging

import cv2


class ImageHandler:
    def __init__(self, image_file_path):
        """
        Constructor

        Parameters:
            image_file_path (pathlib.Path): Complete image file path
        """
        logging.debug("ImageHandler: ImageHandler initiated")
        if not image_file_path.exists():
            raise Exception(f"File {image_file_path} does not exist")

        self.image_file_path = image_file_path
        self.image_bgr = cv2.imread(str(image_file_path))
        self.image_rgb = cv2.cvtColor(self.image_bgr, cv2.COLOR_BGR2RGB)

    def get_image_name(self, include_extension=True):
        """
        Get the image file name

        Parameters:
            include_extension (bool): Whether to include image extension in file name
                Default=True
                Eg. Image name = image1.jpg
                    Include extension = True, returns image1.jpg
                    Include extension = False, returns image1
        """
        if include_extension:
            return self.image_file_path.name
        return self.image_file_path.stem

    def get_image_extension(self, include_dot=False):
        """
        Get the image extension

        Parameters:
            include_dot: Whether to return "jpg" or ".jpg"
                Default=False

        Eg. "image1.jpg" returns jpg, if include dot is True returns .jpg
            "image1.new.jpg" returns jpg, if include dot is True returns .jpg
        """
        if include_dot:
            return "." + self.image_file_path.name.rsplit(".", 1)[-1]
        return self.image_file_path.name.rsplit(".", 1)[-1]

    def get_bgr_image(self):
        """
        Returns the image in BGR format
        """
        return self.image_bgr

    def get_rgb_image(self):
        """
        Returns the image in RGB format
        """
        return self.image_rgb

    def save_image(self, image, save_path):
        """
        Save the image

        Parameters:
            image: The image to save
            save_path: Complete path of image where image need to be save

        Return:
            True if image saved successfully
            False if image save failed
        """
        logging.debug("ImageHandler: Save image %s", save_path)
        return cv2.imwrite(save_path, image)
