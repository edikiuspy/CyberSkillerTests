from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from random import choice, sample
from json import dump, load
import sys
from time import sleep
from itertools import combinations
from datetime import datetime

path = "./chromedriver.exe"
timeout = 10

options = webdriver.ChromeOptions()
options.add_argument("headless")
options.add_argument("window-size=1920x1080")
options.add_argument("disable-gpu")

print("1.Widoczna przeglądarka")
print("2.Ukryta przeglądarka")
answer = input("Wybierz opcje: ")

while answer not in ["1", "2"]:
    print("Nie ma takiej opcji.")
    answer = input("Wybierz opcje: ")
if answer == "1":
    driver = webdriver.Chrome(path)
else:
    driver = webdriver.Chrome(path, options=options)
driver.get("https://technischools.cyberskiller.com/student/courses/")
print("1.Zmień danne użytkownika")
print("2.Wyjście")
with open("config.json", "r") as file:
    json = load(file)
    if json["login"] == "" or json["password"] == "":
        print("Ostrzeżenie! Login lub hasło nie są zapisane w pliku config.json")
        answoptions = ["1", "2"]
    else:
        answoptions = ["1", "2", "3"]
        print("3.Kontynuuj z zapisanym loginem i hasłem")

while True:
    option = input("Wprowadź cyfrę opcji: ")
    if not option in answoptions:
        print("Zły numer!")
    else:
        if option == "1":
            with open("config.json", "w") as file:
                dump({"login": input("Login: "), "password": input("Hasło: ")}, file)
            file.close()
            break
        if option == "2":
            driver.close()
            sys.exit()
        if option == "3":
            break
try:
    with open("config.json", "r") as file:
        json = load(file)
    file.close()
    elem = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.NAME, "username"))
    )
    elem.clear()
    elem.send_keys(json["login"])
    elem = driver.find_element(By.NAME, "password")
    elem.click()
    elem.clear()
    elem.send_keys(json["password"])
    elem.send_keys(Keys.ENTER)
    if (
        len(
            WebDriverWait(driver, timeout).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, "//*[contains(text(),'Dashboard')]")
                )
            )
        )
        != 0
    ):
        pass
except:
    print("Nieprawidłowy login lub hasło")
    while True:
        try:
            elem = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            elem.clear()
            username = input("Login: ")
            elem.send_keys(username)
            elem = driver.find_element(By.NAME, "password")
            elem.click()
            elem.clear()
            password = input("Hasło: ")
            elem.send_keys(password)
            elem.send_keys(Keys.ENTER)
            if (
                len(
                    WebDriverWait(driver, timeout).until(
                        EC.presence_of_all_elements_located(
                            (By.XPATH, "//*[contains(text(),'Dashboard')]")
                        )
                    )
                )
                != 0
            ):
                with open("config.json", "w") as f:
                    dump({"username": username, "password": password}, f)
                f.close()
                break
        except Exception as e:
            print("Nieprawidłowa nazwa użytkownika lub hasło")

def first():
    global name
    WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "course-name"))
    )
    elem = driver.find_elements(By.CLASS_NAME, "course-name")
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "theme-hinvalid"))
        )
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "theme-hinvalid"))
            ),
        )
    except:
        pass
    name = {}
    print("\n")
    for i, j in enumerate(elem):
        print(str(i + 1) + "." + j.text)
        name[i + 1] = j.text
    print("\n")
    while True:
        try:
            nazwa = input("Nazwa/numer kursu: ")
            if nazwa.isdigit():
                nazwa = name[int(nazwa)]
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') ,'{nazwa.lower()}')]",
                    )
                )
            )
            elem = driver.find_elements(
                By.XPATH,
                f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') ,'{nazwa.lower()}')]",
            )[0]
            elem = elem.find_element(By.XPATH, "..")
            elem = elem.find_element(By.TAG_NAME, "a")
            break
        except:
            print("Nie ma kursu o takiej nazwie/numerze")
    driver.execute_script(
        "arguments[0].click();",
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(elem)),
    )
    second()

def two_right(all_questions_and_answers, i, nazwa, right_answers, questons, start):
    for r in range(len(list(all_questions_and_answers.values())[i])):
        try:
            elem = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//*[contains(text(),'{list(all_questions_and_answers.keys())[i].lstrip('0123456789')}')]",
                    )
                )
            )
        except:
            elem = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//*[normalizespace(contains(string(),'{list(all_questions_and_answers.keys())[i].lstrip('0123456789')}'))]",
                    )
                )
            )
        elem = elem.find_element(By.XPATH, "..")
        elem = elem.find_elements(By.TAG_NAME, "label")
        elem_text = [u.text for u in elem]
        combinations_list_text = [list(comb) for comb in combinations(elem_text, 2)]
        for a in combinations_list_text:
            for b in a:
                elem = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located(
                        (By.XPATH, f"//*[contains(text(),'{b.lstrip('0123456789')}')]")
                    )
                )
                elem = elem.find_element(By.XPATH, "..")
                elem = elem.find_elements(By.TAG_NAME, "label")
                for c in elem:
                    if c.text == b:

                        driver.execute_script(
                            "arguments[0].click();",
                            WebDriverWait(driver, timeout).until(
                                EC.element_to_be_clickable(c)
                            ),
                        )
            driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "theme-hprimary"))
                ),
            )
            driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "modal-button"))
                ),
            )
            amount = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(),'Poprawne odpowiedzi')]")
                )
            )
            amount = amount.find_element(By.TAG_NAME, "b").text
            driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "text-lg"))
                ),
            )
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') ,'{nazwa.lower()}')]",
                    )
                )
            )
            elem = driver.find_elements(
                By.XPATH,
                f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') ,'{nazwa.lower()}')]",
            )[0]
            elem = elem.find_element(By.XPATH, "..")
            driver.execute_script("arguments[0].scrollIntoView();", elem)
            driver.execute_script("arguments[0].click();", elem)
            driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(driver, timeout).until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "exercise-control-button")
                    )
                )[-1],
            )
            driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "mark-button"))
                ),
            )
            if amount == "1":
                right_answers[questons[i]] = a
                print(
                    "'\rProgress: {0}{1}".format(
                        str(len(right_answers.keys()))
                        + "/"
                        + str(len(all_questions_and_answers.keys())),
                        " " + str(datetime.now() - start),
                    ),
                    end="",
                )
                return right_answers


def second():
    WebDriverWait(driver, timeout).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.topic-title"))
    )
    elem = driver.find_elements(By.CSS_SELECTOR, "span.topic-title")
    print("\n")
    name = {}
    i = 0
    print("0.Powrót do kursów")
    for j in elem:
        if j.text != "":
            i += 1
            print(str(i) + "." + j.text.capitalize())
            name[i] = j.text
    print("\n")

    while True:
        try:
            nazwa = input("Nazwa/numer tematu: ")
            if nazwa.isdigit():
                if nazwa == "0":
                    driver.find_element(By.CLASS_NAME, "typcn-chevron-left").click()
                    first()
                else:
                    nazwa = name[int(nazwa)]
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') ,'{nazwa.lower()}')]",
                    )
                )
            )
            elem = driver.find_elements(
                By.XPATH,
                f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') ,'{nazwa.lower()}')]",
            )[0]
            elem = elem.find_element(By.XPATH, "..")
            break
        except:
            print("Nie ma tematu o takiej nazwie/numerze")
    driver.execute_script("arguments[0].scrollIntoView();", elem)
    driver.execute_script("arguments[0].click();", elem)

    driver.execute_script(
        "arguments[0].click();",
        WebDriverWait(driver, timeout).until(
            EC.presence_of_all_elements_located(
                (By.CLASS_NAME, "exercise-control-button")
            )
        )[-1],
    )
    driver.execute_script(
        "arguments[0].click();",
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "mark-button"))
        ),
    )
    sleep(1)
    driver.execute_script(
        "arguments[0].click();",
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.TAG_NAME, "h6"))
        ),
    )
    e = driver.find_elements(By.TAG_NAME, "h6")
    k = 0
    for i in e:
        for j in range(3):
            if i.text[0:j].isdigit():
                k = i.text[0:j]
    answers = []
    answers_list = []
    questons = []
    all_questions_and_answers = {}
    right_answers = {}
    wrong = []
    start = datetime.now()

    for i in range(1, int(k) + 1):
        elem = driver.find_element(
            By.XPATH,
            f"/html/body/root/quiz-page/div/div/div/quiz-exercise-page/page-standard-layout/div/div/div/quiz-form/form/box/div/div[{i}]",
        )
        questons.append(elem.find_element(By.TAG_NAME, "h6").text)
    for i in range(1, int(k) + 1):
        elem = driver.find_element(
            By.XPATH,
            f"/html/body/root/quiz-page/div/div/div/quiz-exercise-page/page-standard-layout/div/div/div/quiz-form/form/box/div/div[{i}]",
        )
        for j in elem.find_elements(By.TAG_NAME, "label"):
            answers.append(j.text)
        answers_list.append(answers)
        answers = []
    for i in range(len(questons)):
        all_questions_and_answers[questons[i]] = answers_list[i]
    for i in range(len(questons)):
        for j in range(len(list(all_questions_and_answers.values())[i])):
            try:
                elem = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            f"//*[contains(text(),'{list(all_questions_and_answers.keys())[i].lstrip('0123456789')}')]",
                        )
                    )
                )
            except:
                elem = WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located(
                        (
                            By.XPATH,
                            f"//*[normalizespace(contains(string(),'{list(all_questions_and_answers.keys())[i].lstrip('0123456789')}'))]",
                        )
                    )
                )
            elem = elem.find_element(By.XPATH, "..")
            elem = elem.find_elements(By.TAG_NAME, "label")
            rand_elem = choice(elem)
            rand_elem_text = rand_elem.text
            while rand_elem_text in wrong:
                rand_elem = choice(elem)
                rand_elem_text = rand_elem.text
            wrong.append(rand_elem_text)
            driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable(rand_elem)
                ),
            )

            driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "theme-hprimary"))
                ),
            )
            driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "modal-button"))
                ),
            )
            amount = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(text(),'Poprawne odpowiedzi')]")
                )
            )
            amount = amount.find_element(By.TAG_NAME, "b").text
            driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "text-lg"))
                ),
            )
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') ,'{nazwa.lower()}')]",
                    )
                )
            )
            elem = driver.find_elements(
                By.XPATH,
                f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') ,'{nazwa.lower()}')]",
            )[0]
            elem = elem.find_element(By.XPATH, "..")
            driver.execute_script("arguments[0].scrollIntoView();", elem)
            driver.execute_script("arguments[0].click();", elem)
            driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(driver, timeout).until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "exercise-control-button")
                    )
                )[-1],
            )
            driver.execute_script(
                "arguments[0].click();",
                WebDriverWait(driver, timeout).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "mark-button"))
                ),
            )

            if amount == "1":
                right_answers[questons[i]] = rand_elem_text
                wrong = []
                print(
                    "'\rProgress: {0} {1}".format(
                        str(len(right_answers.keys()))
                        + "/"
                        + str(len(all_questions_and_answers.keys())),
                        " " + str(datetime.now() - start),
                    ),
                    end="",
                )
                break
            elif j == len(list(all_questions_and_answers.values())[i]) - 1:
                two_right(
                    all_questions_and_answers, i, nazwa, right_answers, questons, start
                )

    for i in list(right_answers.keys()):
        elem = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[contains(text(),'{i.lstrip('0123456789')}')]")
            )
        )
        elem = elem.find_element(By.XPATH, "..")
        elem = elem.find_elements(By.TAG_NAME, "label")
        for j in elem:
            if type(right_answers[i]) == list:
                for k in right_answers[i]:
                    if k == j.text:
                        driver.execute_script(
                            "arguments[0].click();",
                            WebDriverWait(driver, timeout).until(
                                EC.element_to_be_clickable(j)
                            ),
                        )
            elif right_answers[i] == j.text:
                driver.execute_script(
                    "arguments[0].click();",
                    WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(j)),
                )
    try:
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "theme-hprimary"))
            ),
        )
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "text-lg"))
            ),
        )
    except:
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "modal-button"))
            ),
        )
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "text-lg"))
            ),
        )

    print("\n")
    print("1.Powrót do kursów")
    print("2.Zmiana tematu")
    print("3.Wyjście")
    print("\n")
    opcja = input("Wybierz opcje: ")
    while opcja not in ["1", "2", "3"]:
        print("Nie ma takiej opcji")
        opcja = input("Wybierz opcje: ")
    if opcja == "1":
        driver.execute_script(
            "arguments[0].click();",
            WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "typcn-chevron-left"))
            ),
        )
        first()
    if opcja == "2":
        second()
    if opcja == "3":
        driver.close()
        sys.exit()


first()
