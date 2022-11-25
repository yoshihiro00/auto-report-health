import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with


driver = webdriver.Chrome() 
driver.get('https://uis.fudan.edu.cn/authserver/login?service=https%3A%2F%2Fzlapp.fudan.edu.cn%2Fa_fudanzlapp%2Fapi%2Fsso%2Findex%3Fredirect%3Dhttps%253A%252F%252Fzlapp.fudan.edu.cn%252Fsite%252Fncov%252FfudanDaily%253Ffrom%253Dhistory%26from%3Dwap') 

# time.sleep(30)
# IDとパスワード入力部分を取得
username_element = driver.find_element(By.ID, "username")
userpass_element = driver.find_element(By.ID, "password")
loginbtn_element = driver.find_element(By.ID, "idcheckloginbtn")
# username_element = driver.find_elements(locate_with(By.id, "username"))
# userpass_element = driver.find_elements(locate_with(By.id, "password"))
username = "19300806053"
userpass = "Fudan6053"

print(username_element)
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


time.sleep(10)
print("完了")
