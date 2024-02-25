AI Image Classifier 는 WEB UI  또는 NAI를 통해 생성된 PNG, JPG, JPEG, WEBP 파일을 특정한 키워드를 입력하거나 와일드카드(프로그램과 동일한 위치에 존재하는 wildcards.txt)를 사용해 일괄적으로 분류할 수 있게 하는 프로그램입니다. 영어, 한국어, 중국어, 일본어를 지원합니다.
f1 키로 도움말, f2 키로 영어, f3 키로 한국어, f4키로 일본어, f5키로 중국어로 변경할 수 있습니다. 기본 언어는 영어로 되어있습니다.언어 설정을 하면 파일과 동일한 디렉토리에 config.json 파일이 생성되며, 이 파일이 존재하는 동안 변경된 언어 설정이 유지됩니다. 

폴더 선택하기: 분류할 이미지가 있는 폴더를 선택합니다.
키워드 입력: 분류할 키워드를 입력합니다.
이미지 분류: 입력한 키워드로 분류합니다.
와일드카드 텍스트: 파일과 동일한 경로에 존재하는 wildcards.txt의 데이터를 보여줍니다.
와일드카드 리로드: wildcards.txt의 데이터를 새로고침합니다.
와일드카드 풀로드: wildcards.txt의 데이터를 사용해 분류합니다.
하이퍼 로드: 선택한 폴더에 있는 모든 txt 파일의 데이터를 사용해 분류합니다.

프로그램 사용법
'폴더 선택하기' 버튼을 눌러 분류하고 싶은 이미지가 있는 폴더를 선택합니다.
2. 키워드 입력 부분에 키워드를 입력하여 '이미지 분류' 버튼을 눌러 분류를 실행합니다.
2-1. 파일과 같은 경로에 있는 wildcards.txt에 있는 단어들로 분류를 실행하는 '와일드카드 풀로드' 버튼을 눌러 분류를 실행할 수 있습니다.
2-2. 폴더를 선택해 해당 폴더에 있는 모든 텍스트 파일의 내용으로 분류를 실행하는 '하이퍼 로드' 기능으로 분류를 실행할 수 있습니다.
3. 분류가 완료되면 메시지가 뜹니다.

단축키
Home: 와일드카드 풀로드
INS: 폴더 선택하기
END: 하이퍼 로드
Enter: 이미지 분류
키보드 왼쪽 키: 동일한 위치의 폴더 중 분류상 더 위에 있는 폴더로 경로 변경
키보드 오른쪽 키: 동일한 위치의 폴더 중 분류상 더 아래에 있는 폴더로 경로 변경


The AI Image Classifier is a program that allows users to classify PNG, JPG, JPEG, and WEBP files generated through WEB UI or NAI by entering specific keywords or using wildcards (wildcards.txt located in the same directory as the program). It supports English, Korean, Chinese, and Japanese languages.

"Pressing the F1 key will bring up the help, F2 key will switch to English, F3 key to Korean, F4 key to Japanese, and F5 key to Chinese. The default language is English. When you set the language, a config.json file will be created in the same directory as the file, and the changed language setting will be maintained as long as this file exists."

Folder path: Shows the path of the currently selected image folder. You can switch to another folder in the same path using the left and right arrow keys on the keyboard. (For example, if you have folders 06-10, 06-11, and 06-06 in folder X, and you've selected folder 06-10 for sorting, you can switch to 06-06 or 06-11 using the left or right arrow keys.) Select folder: A button to set the path of the image folder. It can also be activated with the INS key. Enter keyword: You can enter a keyword in this field and press the image classify button to sort the images. If you want to narrow down the search with multiple keywords, you can separate them with a comma. Classify image: A button that classifies images based on the entered keyword. It can be activated with the enter key. Wildcard fullroad: Classifies batches using the data inside the wildcards.txt file located in the same location as the program. It can also be activated with the home key. Hyper load: Classifies using the data inside all text files in the selected folder. It can be activated with the END key. Below the Wildcard fullroad and Hyper load buttons is a box for the wildcard list, which displays the data inside the wildcards.txt file located in the same location as the program. Clicking on the data in this box will input that data into the Enter Keyword field. Reload Wildcards: Use this when you have modified the data in the wildcards.txt file to update the wildcard list without closing the program.
