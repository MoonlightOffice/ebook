import os
import shutil
import pyautogui
from PIL import Image
from PyPDF2 import PdfFileMerger

PATH_TMP_DIR = './__tmp_dir'

def createTmpDir():
    try:
        if os.path.exists(PATH_TMP_DIR):
            shutil.rmtree(PATH_TMP_DIR)
        os.mkdir(PATH_TMP_DIR)
    except OSError as e:
        print(e)
        exit()

def removeTmpDir():
    if os.path.exists(PATH_TMP_DIR):
        shutil.rmtree(PATH_TMP_DIR)

def getCropsizeFromInput() -> tuple[int]:
    try:
        cropsize = tuple(map(int, input("Left, Top, Right, Bottom: ").split(' ')))
    except:
        print("Invalid input.")
    
    return cropsize

# Generate and save cropped image in tmp directory from given image
def cropImageAndSaveAsPDF(c: tuple[int], rawImgPath: str, newPDFPath: str):
    img =Image.open(rawImgPath)
    if img.mode == 'RGBA':
        img = img.convert('RGB')

    width, height = img.size

    cropsize = (c[0], c[1], width-c[2], height-c[3])

    croppedImg = img.crop(cropsize)

    croppedImg.save(newPDFPath, 'PDF', resolution = 100)


def mergePdf(files: list[str]):
    merger = PdfFileMerger()
    for f in files:
        merger.append(f)

    merger.write('./output.pdf')
    merger.close()

def getSortedImgFilePaths(dir: str) -> list[str]:
    images = os.listdir(dir)
    images = sorted(images)

    imagePaths: list[str] = []

    for img in images:
        splitted_path = img.split('.')

        if len(splitted_path) != 2:
            continue

        if splitted_path[-1] not in ['PNG', 'jpg', 'jpeg']:
            continue

        imagePaths.append(f"{dir}/{img}")

    return imagePaths

def work(dir: str):
    createTmpDir()
    
    img_file_paths = getSortedImgFilePaths(dir)

    for i in range(0, len(img_file_paths)):
        cropImageAndSaveAsPDF((30, 70, 30, 93), img_file_paths[i], f"{PATH_TMP_DIR}/{i}.pdf")

    pdfPaths: list[str] = []

    for i in range(0, len(img_file_paths)):
        pdfPaths.append(f"{PATH_TMP_DIR}/{i}.pdf")

    mergePdf(pdfPaths)

    removeTmpDir()

def demo_pyautogui():
    pyautogui.screenshot('./sample.png')
    pyautogui.press('Enter')
    print(pyautogui.KEY_NAMES)


if __name__ == '__main__':
    pass
