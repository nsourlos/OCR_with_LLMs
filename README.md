# OCR_with_LLMs
![Alt text](./ocr-llava-and-pytesseract.svg)


[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![forthebadge](https://forthebadge.com/images/badges/uses-badges.svg)](https://forthebadge.com)

[![Maintenance](https://img.shields.io/badge/Maintained%3F-no-red.svg)](https://github.com/nsourlos/automatic_bird_detection_in_ancient_manuscripts)


## LLaVA OCR Script [(ocr_Llava.py)](./ocr_Llava.py)


This script utilizes the LLaVA library to process images using a pre-trained model. It automates the process of extracting text from images and interacts with the LLaVA terminal interface. The script assumes a specific workflow for processing a list of images.

### Setup and Dependencies

Before running the script, ensure the following dependencies are installed:

```bash
# Clone the LLaVA repository
git clone https://github.com/haotian-liu/LLaVA.git
cd LLaVA

# Create and activate a virtual environment
conda create -n llava python=3.10 -y
conda activate llava

# Install required packages
pip install --upgrade pip
pip install -e .
pip install protobuf
pip install --upgrade transformers

#If using llava-v1.6-vicuna-7b, additional steps may be required:

# Navigate to the cloned LLaVA repository
cd LLaVA

# Update the repository
git pull

# Reinstall dependencies
pip install -e .
pip uninstall psutil
pip install psutil
```
### Usage

1. Place the script in the 'LLaVA\llava\serve' folder.

2. Update the `image_dir` variable in the script to the path containing the images to be processed.

3. Run the following command in the terminal:

```bash
python -m llava.serve.tcli --model-path liuhaotian/llava-v1.6-vicuna-7b --load-4bit
```
Note: If errors occur, consider changing time.sleep(35) to time.sleep(40).

### Workflow

1. The script collects a list of images from the specified directory and sorts them.

2. It starts the LLaVA terminal command using `subprocess.Popen`.

3. For each image in the list:

   a. It waits for the 'Image path:' prompt, then sends the image path to the LLaVA terminal.

   b. It waits for the 'USER:' prompt and sends the command 'Extract text in the image.'

   c. It waits for 35 seconds to allow processing.

   d. It prints and saves the 'ASSISTANT:' output.

   e. It waits for 2 seconds before moving to the next image.

4. The script logs the progress in the terminal and saves it to the 'output_llava.txt' file.

5. The process is terminated after processing all images, and the total time is displayed.

Note: The script assumes the LLaVA terminal interface follows specific prompts ('Image path:', 'USER:', 'ASSISTANT:'). Adjustments may be needed based on updates to LLaVA.

### Prompts
The prompt used to create the llava script can be found in the jupyter notebook [Prompt_GPT4_Llava.ipynb](./Prompt_GPT4_Llava.ipynb)


## Image Text Extraction with Pytesseract [(ocr_pytesseract.py)](./ocr_pytesseract.py)

### Purpose
The script is designed to process a folder of images, extract text from each image, rotate the image at 90-degree intervals up to 270 degrees, and extract text from the rotated images. The results are then compiled into a Microsoft Word document, with images, names, rotations, and extracted texts.

### Dependencies
Ensure the following packages are installed before running the script:
- `opencv-python`: Image processing library
- `pytesseract`: OCR (Optical Character Recognition) tool
- `Pillow`: Image processing library for opening, manipulating, and saving many different image file formats
- `tqdm`: Progress bar for iteration
- `python-docx`: Library for creating and updating Word documents
- All the requirements can be found in the file [requirements.txt](./requirements.txt) and the sudo commands that should be installed can be found in [this file](./sudo_commands.txt)

### External Dependencies and Commands
- Additional system dependencies and commands are provided in the comments at the beginning of the script.
- These include updating the system, installing necessary libraries, setting up Tesseract OCR, and installing required Python packages.

### Script Workflow

#### 1. Rotate Image Function (`rotate_image`):
   - Takes an image and a rotation angle in degrees.
   - Applies rotation to the image using OpenCV's `warpAffine` function.
   - Returns the rotated image.

#### 2. Resize Image Function (`resize_image`):
   - Takes an image and a scale factor.
   - Resizes the image while maintaining the original aspect ratio.
   - Returns the resized image.

#### 3. Text Extraction Function (`extract_text`):
   - Uses pytesseract to extract text from an image.
   - Returns the extracted text.

#### 4. Add Image to Document Function (`add_image_to_doc`):
   - Takes a Word document (`doc`), image path, image name, extracted text, rotated image, and rotation angle.
   - Sanitizes text to remove problematic characters.
   - Adds a paragraph to the document with image name, rotation angle, and sanitized text.
   - Resizes the rotated image, converts it to a format suitable for Word (`PIL` to `BytesIO`), and adds it to the document.
   - Adds a line break between images.

#### 5. Main Function (`main`):
   - Accepts a folder path as a command-line argument.
   - Verifies the existence of the folder.
   - Gets a list of image files in the folder.
   - Initializes a Word document.
   - Iterates through each image, rotating it at 90-degree intervals and extracting text.
   - Saves the Word document with processed information on the desktop.

#### 6. Command-Line Execution:
   - The script can be executed from the command line with the folder path as an argument.
   - Example: `python script.py /path/to/image/folder`

### Notes
- The script may display an error message related to XML compatibility. It handles this issue by modifying the `add_image_to_doc` function.
- The script saves the Word document on the desktop with the folder name and "_word.docx" appended.
- Images are not cropped to fit the original dimensions but are adapted to their new size when added to the Word document.
- The script provides a progress bar using `tqdm`.
- The execution time is printed at the end of the script.