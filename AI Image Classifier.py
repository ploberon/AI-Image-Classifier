import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import unicodedata
import re
import os
import shutil

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
        completion_message = f"{keyword_entry.get()}와 일치하는 이미지 {classified_image_count}장 분류되었습니다."
        classification_results.append(completion_message)
        if show_message:  # 추가된 조건문
            messagebox.showinfo("분류 완료", completion_message)

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
        messagebox.showinfo("모든 분류 완료", "\n".join(classification_results))
    keyword_entry.delete(0, tk.END)  # 여기에 추가

    # 모든 분류 완료 메시지만 남기기
    if classification_results:
        messagebox.showinfo("모든 분류 완료", "\n".join(classification_results))

def load_and_classify_with_wildcards():
    global classification_results
    classification_results = []
    keywords = load_keywords_from_file('wildcards.txt')
    for keyword in keywords:
        keyword_entry.delete(0, tk.END)
        keyword_entry.insert(tk.END, keyword)
        classify_images(show_message=False)  # 수정됨
    if classification_results:
        messagebox.showinfo("모든 분류 완료", "\n".join(classification_results))
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

def show_help():
    help_text = (
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
    )
    messagebox.showinfo("도움말", help_text)    

root = tk.Tk()
root.title("AI 이미지 분류기")
root.geometry("500x500")

# 이제 안전하게 StringVar() 객체를 초기화할 수 있습니다.
classification_type = None

image_folder_label = tk.Label(root, text="이미지 폴더:")
image_folder_label.pack()

folder_path_entry = tk.Entry(root, width=50)
folder_path_entry.pack()

folder_button = tk.Button(root, text="폴더 선택하기", command=select_folder)
folder_button.pack()

keyword_label = tk.Label(root, text="키워드 입력:")
keyword_label.pack()

keyword_entry = tk.Entry(root, width=30)
keyword_entry.pack()

# 버튼을 가로로 배치하기 위한 프레임 생성
button_frame = tk.Frame(root)
button_frame.pack(pady=10)  # y축 패딩으로 버튼과 위젯 사이 간격 조정

# 이미지 분류 버튼
classify_button = tk.Button(button_frame, text="이미지 분류", command=classify_images)
classify_button.pack(side=tk.LEFT, padx=5)

# 와일드카드 풀로드 버튼
reload_and_classify_button = tk.Button(button_frame, text="와일드카드 풀로드", command=load_and_classify_with_wildcards)
reload_and_classify_button.pack(side=tk.LEFT, padx=5)

# 하이퍼 로드 버튼
hyper_load_and_classify_button = tk.Button(button_frame, text="하이퍼 로드", command=hyper_load_and_classify)
hyper_load_and_classify_button.pack(side=tk.LEFT, padx=5)

keywords = load_keywords_from_file('wildcards.txt')

keyword_listbox = tk.Listbox(root)
keyword_listbox.pack()

for keyword in keywords:
    keyword_listbox.insert(tk.END, keyword)

keyword_listbox.bind('<<ListboxSelect>>', on_select)

# 와일드카드 리로드 버튼 (와일드카드 텍스트 박스 바로 아래에 위치)
reload_wildcards_button = tk.Button(root, text="와일드카드 리로드", command=reload_keywords)
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
