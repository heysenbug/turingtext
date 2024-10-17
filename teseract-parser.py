import os
import json
import argparse
import pytesseract
from PIL import Image
from groq import Groq

api_token = os.environ.get("GROQ_API_KEY")
llama_model = 'llama3-8b-8192'
system_content = 'You are a receipt infromation parser. \
I will sumbit scanned receipt text and you will return the following data in \
json format: store name, store address, store city, store country, a list \
of items with their name and price, the total price, taxes paid, and \
tips if any given.'

def get_all_files(directory):
    files_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            files_list.append(os.path.join(root, file))
    return files_list

def parse_image(image):
    # Load image and apply OCR
    print(f'Getting text for {image}')
    img = Image.open(image)
    img = img.convert('RGB')
    text = pytesseract.image_to_string(img)
    return text

# Ask groq about the receipt data
def parse_receipt_text(llm, text):
    r_messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": text }
    ]

    response = llm.chat.completions.create(messages=r_messages, model=llama_model)
    print(response.choices[0].message.content)

def parse_receipts(dir):
    print(f'Getting images from {dir}')
    # Get all images from directory
    images = get_all_files(dir)

    print('Initializing Groq client...')
    client = Groq(
        api_key=api_token
    )

    # Parse each image
    # for img in images:
    #     print(f'Parsing {img}')
    #     image_text = parse_image(img)
    #     print(f'Asking llama about the receipt')
    #     parse_receipt_text(llama, image_text)
    image_text = parse_image(images[0])
    parse_receipt_text(client, image_text)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parse receipts and get their information')
    parser.add_argument('dir', type=str, nargs='?',
                        help='Directory containing receipt images')
    args = parser.parse_args()

    src_dir = 'unorganized'
    if args.dir:
        src_dir = args.dir

    parse_receipts(src_dir)