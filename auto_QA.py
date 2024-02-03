import os
import re
import sys
from datetime import datetime

def process_text_for_xiaoetong(text):
    processed_text = re.sub(r'(\d+)(?:\.|、)(?!\d)', r'\1.[单选题]', text)
    processed_text = re.sub(r'(C\..+?)(\n|$)', r'\1\n答案：\n', processed_text, flags=re.DOTALL)
    return processed_text

def process_text_for_jinshuju(text):
    processed_text = re.sub(r'\d+(?:\.|、)(?!\d)', r'\n\n[单选题]', text).strip()
    processed_text = re.sub(r'\n{3,}', r'\n\n', processed_text)
    processed_text = processed_text.lstrip('\n')
    return processed_text

def process_file(input_file_path, output_dir_path):
    original_filename = os.path.splitext(os.path.basename(input_file_path))[0]
    current_date = datetime.now().strftime('%Y-%m-%d')

    with open(input_file_path, 'r', encoding='utf-8') as file:
        original_text = file.read()

    processed_text_xiaoetong = process_text_for_xiaoetong(original_text)
    processed_text_jinshuju = process_text_for_jinshuju(original_text)

    header = f"{original_filename}（默认标题，可修改）\n{current_date}（默认描述，可修改）\n\n"
    processed_text_jinshuju = header + processed_text_jinshuju

    with open(os.path.join(output_dir_path, f'{original_filename}_xiaoe.txt'), 'w', encoding='utf-8') as file:
        file.write(processed_text_xiaoetong)

    with open(os.path.join(output_dir_path, f'{original_filename}_jinshuju.txt'), 'w', encoding='utf-8') as file:
        file.write(processed_text_jinshuju)

def main():
    if len(sys.argv) < 2:
        print("Usage: python auto_QA.py <input_file>")
        sys.exit(1)

    input_arg = sys.argv[1]
    output_dir_path = "C:\\Users\\recker\\Downloads"

    if input_arg.lower() == '全部':
        for filename in os.listdir(output_dir_path):
            if filename.endswith('.txt') and not filename.startswith('.') and not filename.endswith('_xiaoe.txt') and not filename.endswith('_jinshuju.txt'):
                input_file_path = os.path.join(output_dir_path, filename)
                process_file(input_file_path, output_dir_path)
    else:
        input_file_path = os.path.join(output_dir_path, f'{input_arg}.txt')
        if os.path.exists(input_file_path):
            process_file(input_file_path, output_dir_path)
        else:
            print(f"文件未找到，请检查名称是否正确")

if __name__ == "__main__":
    main()
