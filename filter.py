import os

folder_path = "outputs/articles"
file_list = os.listdir(folder_path)
output_file_path = "outputs/articles.txt"

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, 'r', encoding='utf-8') as input_file:
            file_content = input_file.read()
            index = file_content.find('\n\n')
            if index != -1:
                output_text = file_content[:index]
            else:
                output_text = file_content
            output_file.write(output_text + '\n\n')
