import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with

from PIL import Image
import sys

import pyocr
import pyocr.builders


driver = webdriver.Chrome() 
driver.get('https://uis.fudan.edu.cn/authserver/login?service=https%3A%2F%2Fzlapp.fudan.edu.cn%2Fa_fudanzlapp%2Fapi%2Fsso%2Findex%3Fredirect%3Dhttps%253A%252F%252Fzlapp.fudan.edu.cn%252Fsite%252Fncov%252FfudanDaily%253Ffrom%253Dhistory%26from%3Dwap') 

# time.sleep(30)
# IDとパスワード入力部分を取得
username_element = driver.find_element(By.ID, "username")
userpass_element = driver.find_element(By.ID, "password")
loginbtn_element = driver.find_element(By.ID, "idcheckloginbtn")

username = "19300806053"
userpass = "Fudan6053"

#IDとパスワードを入力
username_element.send_keys(username)
userpass_element.send_keys(userpass)
loginbtn_element.click()

# ログイン後
#表示される　「1日に1回しかできませんよ」の確認ボタンを押す
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "wapat-btn-ok"))
    )
except:
    print("「wapat-btn-ok」を持つ要素が見つからずタイムアウトしました")  

confirm_btn_element = driver.find_element(By.CLASS_NAME, "wapat-btn-ok")
confirm_btn_element.click()

# 是否在校？の部分
check_is_campus_element = driver.find_element(By.NAME, "sfzx").find_elements(By.TAG_NAME,"div")[2]
check_is_campus_element.click()

#请选择目前所在国家の部分
select_country_element = driver.find_element(By.CLASS_NAME, "select2-selection__rendered")
select_country_element.click()

selection_list_elements = driver.find_element(By.ID, "select2-szgj-results").find_elements(By.TAG_NAME,"li")

# 国のリストから日本を探してIDを返す
def searchJapanID():
    for i in selection_list_elements:
        element_id = i.get_attribute("id")
        if "日本" in element_id :
            return element_id

selection_japan_element = driver.find_element(By.ID, searchJapanID())
selection_japan_element.click()

# 提交信息の部分
submitbtn_element = driver.find_element(By.CLASS_NAME, "footers")
submitbtn_element.click()
confirm_submitbtn_element = driver.find_element(By.CLASS_NAME, "wapcf-btn-ok")
confirm_submitbtn_element.click()

# ランダムな英文字が書かれた画像を保存する
time.sleep(5) #画像が表示されるまで
cipher_img = driver.find_element(By.CLASS_NAME, "wapat-title-img").find_element(By.TAG_NAME, "img").screenshot_as_png
cipher_img_path = '/Users/yoshi/Desktop/auto-report-health/cipher/' + str(int(time.time())) + '.png'
with open(cipher_img_path, 'wb') as f:
    f.write(cipher_img)

# 画像認識
pyocr_tools = pyocr.get_available_tools()
if len(pyocr_tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = pyocr_tools[0]

analysed_text = tool.image_to_string(
    Image.open(cipher_img_path),
    lang="eng",
    builder=pyocr.builders.TextBuilder()
)
# 空白を削除
analysed_text = analysed_text.replace(' ','')
print(analysed_text)

# 解析されたテキストを入力
cipher_text_area_element = driver.find_element(By.CLASS_NAME, "wapat-title-input").find_element(By.TAG_NAME,"input")
cipher_text_area_element.send_keys(analysed_text)

time.sleep(3)
driver.find_element(By.CLASS_NAME,"wapat-btn-ok").click()



time.sleep(10)
print("完了")
