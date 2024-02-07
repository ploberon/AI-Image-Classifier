import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import unicodedata
import re
import os
import shutil

# 현재 언어 설정
current_language = 'English'

languages = {
    'English': {
        'title': 'AI Image Classifier',
        'select_folder': 'Select Folder',
        'input_keyword': 'Enter Keyword:',
        'classify_images': 'Classify Images',
        'reload_wildcards': 'Reload Wildcards',
        'classification_complete': "Classification Complete",
        'all_classifications_complete': "All Classifications Complete",
        'match_images': "{keyword} - {count} images classified.",
        'hyper_load': 'Hyper Load',
        "label_text": "Language",
        'help': 'Help(F1)',
        'help_text': (
            "Function Description\n\n"
            "Select Folder: Choose the folder where the images to be classified are located.\n"
            "Input Keyword: Enter the keyword for classification.\n"
            "Classify Images: Classify images based on the entered keywords.\n"
            "Wildcard Text: Display the data from wildcards.txt located in the same path as the program.\n"
            "Reload Wildcards: Refresh the data from wildcards.txt.\n"
            "Wildcard Load: Classify images using the data from wildcards.txt.\n"
            "Hyper Load: Classify images using the data from all text files in the selected folder.\n\n"
            "Program Usage\n\n"
            "1. Click the 'Select Folder' button to choose the folder containing the images you want to classify.\n"
            "2. Enter the keywords in the input field and press the 'Classify Images' button to start classification.\n"
            "2-1. Use the 'Wildcard Load' button to classify images based on the words in wildcards.txt located in the same path as the program.\n"
            "2-2. Use the 'Hyper Load' function to classify images based on the content of all text files in the selected folder.\n"
            "3. Once classification is complete, a message will appear.\n\n"
            "Keyboard Shortcuts\n\n"
            "Home: Wildcard Load\n"
            "INS: Select Folder\n"
            "END: Hyper Load\n"
            "Enter: Classify Images\n"
            "Left Arrow Key: Move to the previous folder\n"
            "Right Arrow Key: Move to the next folder"
        ),
    },
    '한국어': {
        'title': 'AI 이미지 분류기',
        "label_text": "언어",
        'select_folder': '폴더 선택하기',
        'input_keyword': '키워드 입력:',
        'classify_images': '이미지 분류',
        'classification_complete': "분류 완료",
        'all_classifications_complete': "모든 분류 완료",
        'match_images': "{keyword}와 일치하는 이미지 {count}장 분류되었습니다.",
        'reload_wildcards': '와일드카드 리로드',
        'hyper_load': '하이퍼 로드',
        'help': '도움말(F1)',
        'help_text': (
            "기능 설명\n\n"
            "폴더 선택하기: 분류할 이미지가 있는 폴더를 선택합니다.\n"
            "키워드 입력: 분류할 키워드를 입력합니다.\n"
            "이미지 분류: 입력한 키워드로 분류합니다.\n"
            "와일드카드 텍스트: 파일과 동일한 경로에 존재하는 wildcards.txt의 데이터를 보여줍니다.\n"
            "와일드카드 리로드: wildcards.txt의 데이터를 새로고침합니다.\n"
            "와일드카드 풀로드: wildcards.txt의 데이터를 사용해 분류합니다.\n"
            "하이퍼 로드: 선택한 폴더에 있는 모든 txt 파일의 데이터를 사용해 분류합니다.\n\n"
            "프로그램 사용법\n\n"
            "1. '폴더 선택하기' 버튼을 눌러 분류하고 싶은 이미지가 있는 폴더를 선택합니다.\n"
            "2. 키워드 입력 부분에 키워드를 입력하여 '이미지 분류' 버튼을 눌러 분류를 실행합니다.\n"
            "2-1. 파일과 같은 경로에 있는 wildcards.txt에 있는 단어들로 분류를 실행하는 '와일드카드 풀로드' 버튼을 눌러 분류를 실행할 수 있습니다.\n"
            "2-2. 폴더를 선택해 해당 폴더에 있는 모든 텍스트 파일의 내용으로 분류를 실행하는 '하이퍼 로드' 기능으로 분류를 실행할 수 있습니다.\n"
            "3. 분류가 완료되면 메시지가 뜹니다.\n\n"
            "단축키\n\n"
            "Home: 와일드카드 풀로드\n"
            "INS: 폴더 선택하기\n"
            "END: 하이퍼 로드\n"
            "Enter: 이미지 분류\n"
            "키보드 왼쪽 키: 이전 폴더로 이동\n"
            "키보드 오른쪽 키: 다음 폴더로 이동"
        ),
    },
    '中文': {
        'title': 'AI 图像分类器',
        'select_folder': '选择文件夹',
        "label_text": "语言",
        'input_keyword': '输入关键词:',
        'classify_images': '分类图片',
        'reload_wildcards': '重新加载通配符',
        'classification_complete': "分类完成",
        'all_classifications_complete': "所有分类完成",
        'match_images': "{keyword}匹配的图片共{count}张已分类。",
        'hyper_load': '超级加载',
        'help': '帮助(F1)',
        'help_text': (
            "功能说明\n\n"
            "选择文件夹：选择包含要分类的图像的文件夹。\n"
            "输入关键词：输入用于分类的关键词。\n"
            "分类图片：根据输入的关键词对图像进行分类。\n"
            "通配符文本：显示与程序相同路径下的wildcards.txt文件中的数据。\n"
            "重新加载通配符：刷新来自wildcards.txt的数据。\n"
            "通配符加载：使用来自wildcards.txt的数据对图像进行分类。\n"
            "超级加载：使用所选文件夹中所有文本文件的数据对图像进行分类。\n\n"
            "程序使用\n\n"
            "1. 单击“选择文件夹”按钮选择包含要分类图像的文件夹。\n"
            "2. 在输入字段中输入关键词，然后按“分类图片”按钮开始分类。\n"
            "2-1. 使用“通配符加载”按钮根据位于与程序相同路径下的wildcards.txt文件中的单词对图像进行分类。\n"
            "2-2. 使用“超级加载”功能根据所选文件夹中所有文本文件的内容对图像进行分类。\n"
            "3. 完成分类后，将显示消息。\n\n"
            "键盘快捷键\n\n"
            "Home：通配符加载\n"
            "INS：选择文件夹\n"
            "END：超级加载\n"
            "Enter：分类图片\n"
            "左箭头键：移至上一个文件夹\n"
            "右箭头键：移至下一个文件夹"
        ),
    },
    '日本語': {
        'title': 'AI 画像分類器',
        "label_text": "言語",
        'select_folder': 'フォルダを選択',
        'input_keyword': 'キーワードを入力:',
        'classify_images': '画像を分類',
        'reload_wildcards': 'ワイルドカードをリロード',
        'classification_complete': "分類完了",
        'all_classifications_complete': "全ての分類完了",
        'match_images': "{keyword}に一致する画像{count}枚が分類されました。",
        'hyper_load': 'ハイパーロード',
        'help': 'ヘルプを(F1)',
        'help_text': (
            "機能説明\n\n"
            "フォルダを選択：分類する画像が含まれているフォルダを選択します。\n"
            "キーワードを入力：分類のためのキーワードを入力します。\n"
            "画像を分類：入力したキーワードに基づいて画像を分類します。\n"
            "ワイルドカードテキスト：プログラムと同じパスにあるwildcards.txtファイルのデータを表示します。\n"
            "ワイルドカードをリロード：wildcards.txtからデータを更新します。\n"
            "ワイルドカードを読み込む：wildcards.txtからのデータを使用して画像を分類します。\n"
            "ハイパーロード：選択したフォルダ内のすべてのテキストファイルのデータを使用して画像を分類します。\n\n"
            "プログラムの使用法\n\n"
            "1. 'フォルダを選択'ボタンをクリックして、分類したい画像が含まれているフォルダを選択します。\n"
            "2. 入力フィールドにキーワードを入力し、「画像を分類」ボタンを押して分類を開始します。\n"
            "2-1. プログラムと同じパスにあるwildcards.txtファイル内の単語に基づいて画像を分類するには、「ワイルドカードを読み込む」ボタンを使用します。\n"
            "2-2. 「ハイパーロード」機能を使用して、選択したフォルダ内のすべてのテキストファイルの内容に基づいて画像を分類します。\n"
            "3. 分類が完了すると、メッセージが表示されます。\n\n"
            "キーボードショートカット\n\n"
            "Home：ワイルドカードを読み込む\n"
            "INS：フォルダを選択\n"
            "END：ハイパーロード\n"
            "Enter：画像を分類\n"
            "左矢印キー：前のフォルダに移動\n"
            "右矢印キー：次のフォルダに移動"
        ),
    },
}

    

# 초기화 코드에 변수 추가
current_folder_list = []
current_folder_index = -1   

# 이미지 분류 결과를 저장하는 리스트
classification_results = []

def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:  # 폴더 선택 취소를 방지
        folder_path_entry.delete(0, 'end')
        folder_path_entry.insert('end', folder_path)
        update_folder_list(folder_path)

def update_folder_list(selected_folder_path):
    global current_folder_list, current_folder_index
    parent_folder = os.path.dirname(selected_folder_path)
    folder_list = [f.path for f in os.scandir(parent_folder) if f.is_dir()]
    current_folder_list = sorted([os.path.abspath(path) for path in folder_list])  # 폴더 경로를 절대 경로로 변환하고 정렬
    current_folder_index = current_folder_list.index(os.path.abspath(selected_folder_path))  # 선택한 폴더 경로도 절대 경로로 변환하여 인덱스 찾기

def navigate_folder(direction):
    global current_folder_index
    if not current_folder_list:  # 폴더 목록이 비어있으면 함수를 종료
        return
    if direction == "previous" and current_folder_index > 0:
        current_folder_index -= 1
    elif direction == "next" and current_folder_index < len(current_folder_list) - 1:
        current_folder_index += 1

    new_folder_path = current_folder_list[current_folder_index]
    folder_path_entry.delete(0, 'end')
    folder_path_entry.insert('end', new_folder_path)


def load_keywords_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            keywords = file.read().splitlines()
        return keywords
    except FileNotFoundError:
        return []

# 이미지 분류 결과를 저장하고 화면에 표시하는 함수
def classify_images(show_message=True):
    global classification_results  # 전역 변수 사용
    classified_count = 0
    classified_image_count = classify_images_internal()
    if classified_image_count > 0:
        keyword = keyword_entry.get()
        completion_message = languages[current_language]['match_images'].format(keyword=keyword, count=classified_image_count)
        classification_results.append(completion_message)
        if show_message:  # 추가된 조건문
            messagebox.showinfo(languages[current_language]['classification_complete'], completion_message)

# 내부적으로 이미지를 분류하고 실제 분류된 이미지 수를 반환하는 함수
def classify_images_internal():
    keyword = keyword_entry.get().lower()
    keywords = [kw.strip() for kw in keyword.split(',')]
    folder_path = folder_path_entry.get()

    keyword_normalized = "_".join(keywords).lower()
    keyword_folder = os.path.join(folder_path, keyword_normalized)

    classified_image_count = 0

    try:
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)

            # 이미지 파일 확장자 확인
            if file_path.lower().endswith(('.jpg', '.jpeg', '.webp')):
                with open(file_path, 'rb') as f:
                    img = Image.open(f)
                    exif_data = img._getexif()

                if exif_data and 37510 in exif_data:
                    user_comments = exif_data[37510]
                    user_comments = user_comments.replace(b'\x00', b'').decode('utf-8', errors='ignore').lower()
                    user_comments = remove_invalid_chars(user_comments)

                    # 모든 키워드가 이미지에 포함되면 분류
                    if all(keyword in user_comments for keyword in keywords):
                        if not os.path.exists(keyword_folder):
                            os.makedirs(keyword_folder)
                        destination_path = os.path.join(keyword_folder, file_name)
                        shutil.move(file_path, destination_path)
                        classified_image_count += 1

            elif file_path.lower().endswith('.png'):
                with open(file_path, 'rb') as f:
                    img = Image.open(f)
                    metadata = img.info

                if metadata:
                    keyword_found = False
                    for key, value in metadata.items():
                        value = remove_invalid_chars(str(value))
                        # 모든 키워드가 이미지에 포함되면 분류
                        if any(keyword.lower() in value.lower() for keyword in keywords):
                            keyword_found = True

                    if keyword_found:
                        if not os.path.exists(keyword_folder):
                            os.makedirs(keyword_folder)
                        destination_path = os.path.join(keyword_folder, file_name)
                        shutil.move(file_path, destination_path)
                        classified_image_count += 1

    except Exception as e:
        error_message = f"Error occurred while processing {file_name}: {str(e)}"
        print(f"Error: {error_message}")

    return classified_image_count

def on_select(event):
    widget = event.widget
    selected_index = widget.curselection()[0]
    selected_keyword = widget.get(selected_index)

    keyword_entry.delete(0, tk.END)
    keyword_entry.insert(tk.END, selected_keyword)

def remove_invalid_chars(text):
    return re.sub(r'[\\/:*?"|]', '', text)

def remove_comma(text):
    return text.replace(',', '')

def reload_keywords():
    keyword_listbox.delete(0, tk.END)
    keywords = load_keywords_from_file('wildcards.txt')

    for keyword in keywords:
        keyword_listbox.insert(tk.END, keyword)

def hyper_load_and_classify():
    global classification_results
    classification_results = []
    
    folder_path = filedialog.askdirectory()
    if not folder_path:
        return

    keywords = load_keywords_from_file('wildcards.txt')

    for file_path in os.listdir(folder_path):
        for keyword in keywords:
            keyword_entry.delete(0, tk.END)
            keyword_entry.insert(tk.END, keyword)
            classify_images(show_message=False)

    if classification_results:
        messagebox.showinfo(languages[current_language]['all_classifications_complete'], "\n".join(classification_results))
    keyword_entry.delete(0, tk.END)  # 여기에 추가

    # 모든 분류 완료 메시지만 남기기
    if classification_results:
        messagebox.showinfo(languages[current_language]['all_classifications_complete'], "\n".join(classification_results))

def load_and_classify_with_wildcards():
    global classification_results
    classification_results = []
    keywords = load_keywords_from_file('wildcards.txt')
    for keyword in keywords:
        keyword_entry.delete(0, tk.END)
        keyword_entry.insert(tk.END, keyword)
        classify_images(show_message=False)  # 수정됨
    if classification_results:
        messagebox.showinfo(languages[current_language]['all_classifications_complete'], "\n".join(classification_results))
    keyword_entry.delete(0, tk.END)  # 여기에 추가

# 키보드 이벤트 처리
def on_home_key(event):
    load_and_classify_with_wildcards()

def on_end_key(event):
    hyper_load_and_classify()

def on_ins_key(event):
    select_folder()

def on_left_key(event):
    if current_folder_index > 0:
        navigate_folder("previous")

def on_right_key(event):
    if current_folder_index < len(current_folder_list) - 1:
        navigate_folder("next")

    
root = tk.Tk()
root.title("AI Image Classifier V3")
root.geometry("500x500")


def change_language(language):
    global current_language
    current_language = language
    update_language(current_language)  # 언어 변경 시 UI 업데이트
    update_help_menu()  # 도움말 메뉴 업데이트

def create_language_menu(menubar):
    language_menu = tk.Menu(menubar, tearoff=0)
    language_menu.add_command(label="English", command=lambda: change_language("English"))
    language_menu.add_command(label="한국어", command=lambda: change_language("한국어"))
    language_menu.add_command(label="中文", command=lambda: change_language("中文"))
    language_menu.add_command(label="日本語", command=lambda: change_language("日本語"))
    menubar.add_cascade(label="Language", menu=language_menu)

def update_help_menu():
    help_menu.delete(0, tk.END)  # 기존 메뉴 항목 삭제
    help_menu.add_command(label=languages[current_language]["help"], command=show_help_in_language)

def create_help_menu(menubar):
    global help_menu  # 전역 변수로 선언하여 다른 함수에서도 사용할 수 있도록 함
    help_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Help", menu=help_menu)
    update_help_menu()  # 초기 도움말 메뉴 업데이트

def update_language(selected_language):
    global current_language
    current_language = selected_language
    # 라벨과 버튼 텍스트를 선택된 언어에 따라 업데이트
    if current_language in languages:
        # 언어 라벨 업데이트 로직 주석 처리
        # if 'language_label' not in globals():
        #     global language_label
        #     language_label = tk.Label(root, text=languages[current_language]['label_text'])
        #     language_label.pack()  # 이 부분을 주석 처리 또는 삭제
        # else:
        #     language_label.config(text=languages[current_language]['label_text'])
        root.title(languages[current_language]['title'])
        folder_button.config(text=languages[current_language]['select_folder'])
        keyword_label.config(text=languages[current_language]['input_keyword'])
        classify_button.config(text=languages[current_language]['classify_images'])
        reload_and_classify_button.config(text=languages[current_language]['reload_wildcards'])
        hyper_load_and_classify_button.config(text=languages[current_language]['hyper_load'])
    else:
        # 선택된 언어가 지원되지 않는 경우의 처리도 동일하게 적용
        # 언어 라벨 업데이트 로직 주석 처리
        # language_label.config(text=languages['English']['label_text'])
        root.title(languages['English']['title'])
        folder_button.config(text=languages['English']['select_folder'])
        keyword_label.config(text=languages['English']['input_keyword'])
        classify_button.config(text=languages['English']['classify_images'])
        reload_and_classify_button.config(text=languages['English']['reload_wildcards'])
        hyper_load_and_classify_button.config(text=languages['English']['hyper_load'])

def show_help_in_language():
    if current_language in languages:
        messagebox.showinfo("Help", languages[current_language]["help_text"])
    else:
        messagebox.showinfo("Help", languages['English']["help_text"])

menubar = tk.Menu(root)
create_help_menu(menubar)
create_language_menu(menubar)
root.config(menu=menubar)

image_folder_label = tk.Label(root, text=languages[current_language]['select_folder'])
image_folder_label.pack()

folder_path_entry = tk.Entry(root, width=50)
folder_path_entry.pack()

folder_button = tk.Button(root, text=languages[current_language]['select_folder'], command=select_folder)
folder_button.pack()

keyword_label = tk.Label(root, text=languages[current_language]['input_keyword'])
keyword_label.pack()

keyword_entry = tk.Entry(root, width=30)
keyword_entry.pack()

# 버튼을 가로로 배치하기 위한 프레임 생성
button_frame = tk.Frame(root)
button_frame.pack(pady=10)  # y축 패딩으로 버튼과 위젯 사이 간격 조정

# 이미지 분류 버튼
classify_button = tk.Button(button_frame, text=languages[current_language]['classify_images'], command=classify_images)
classify_button.pack(side=tk.LEFT, padx=5)

# 와일드카드 풀로드 버튼
reload_and_classify_button = tk.Button(button_frame, text=languages[current_language]['reload_wildcards'], command=load_and_classify_with_wildcards)
reload_and_classify_button.pack(side=tk.LEFT, padx=5)

# 하이퍼 로드 버튼
hyper_load_and_classify_button = tk.Button(button_frame, text=languages[current_language]['hyper_load'], command=hyper_load_and_classify)
hyper_load_and_classify_button.pack(side=tk.LEFT, padx=5)

keywords = load_keywords_from_file('wildcards.txt')

keyword_listbox = tk.Listbox(root)
keyword_listbox.pack()

for keyword in keywords:
    keyword_listbox.insert(tk.END, keyword)

keyword_listbox.bind('<<ListboxSelect>>', on_select)

# 와일드카드 리로드 버튼 (와일드카드 텍스트 박스 바로 아래에 위치)
reload_wildcards_button = tk.Button(root, text=languages[current_language]['reload_wildcards'], command=reload_keywords)
reload_wildcards_button.pack(pady=5)  # 버튼과 리스트 박스 사이의 간격 추가

# 키보드 바인딩
root.bind('<Return>', lambda event: classify_images())  # 엔터 키 이벤트 감지
root.bind('<Home>', on_home_key)
root.bind('<End>', on_end_key)
root.bind('<Insert>', on_ins_key)
root.bind('<Prior>', lambda event: reload_keywords())  # Page Up 버튼 이벤트 감지 ('Prior'는 Page Up 키에 해당)
root.bind('<F1>', lambda event: show_help())
root.bind('<Left>', on_left_key)
root.bind('<Right>', on_right_key)

root.mainloop()
