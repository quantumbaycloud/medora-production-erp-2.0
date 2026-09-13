import os

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from paddleocr import PaddleOCR
except ImportError:
    PaddleOCR = None


class OCRService:

    _ocr_instance = None

    @classmethod
    def get_ocr(cls):
        if cls._ocr_instance is None and PaddleOCR is not None:
            cls._ocr_instance = PaddleOCR(use_angle_cls=True, lang="en")
        return cls._ocr_instance

    @staticmethod
    def preprocess_image(image_path: str) -> str:
        """
        Preprocess prescription image before OCR.
        Steps:
        1. Read image
        2. Convert to grayscale
        3. Remove noise
        4. Improve contrast
        5. Correct image rotation when possible
        """
        if cv2 is None:
            raise RuntimeError("OpenCV (cv2) is not installed.")

        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Unable to read image: {image_path}")

        # 1. Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 2. Noise removal
        denoised = cv2.fastNlMeansDenoising(gray, None, h=10, templateWindowSize=7, searchWindowSize=21)

        # 3. Contrast enhancement
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(denoised)

        # 4. Automatic rotation correction
        _, threshold = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        coordinates = cv2.findNonZero(threshold)

        corrected = enhanced
        if coordinates is not None:
            rect = cv2.minAreaRect(coordinates)
            angle = rect[-1]
            if angle < -45:
                angle = -(90 + angle)
            else:
                angle = -angle

            if abs(angle) > 0.5:
                height, width = enhanced.shape
                center = (width // 2, height // 2)
                matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                corrected = cv2.warpAffine(
                    enhanced, matrix, (width, height), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE
                )

        directory = os.path.dirname(image_path)
        filename = os.path.basename(image_path)
        name, extension = os.path.splitext(filename)
        processed_path = os.path.join(directory, f"{name}_processed.png")

        cv2.imwrite(processed_path, corrected)
        return processed_path

    @staticmethod
    def extract_text(image_path: str) -> str:
        ocr = OCRService.get_ocr()
        if ocr is None:
            raise RuntimeError("PaddleOCR is not available.")

        processed_image = OCRService.preprocess_image(image_path)
        result = ocr.ocr(processed_image)

        extracted_text = []
        for page in result:
            if not page:
                continue
            for line in page:
                if not line:
                    continue
                try:
                    text = line[1][0]
                    if text:
                        extracted_text.append(text)
                except (IndexError, TypeError):
                    continue

        return "\n".join(extracted_text)
