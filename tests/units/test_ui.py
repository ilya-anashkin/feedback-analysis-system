import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_feedback_interface():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Переходим на страницу
        driver.get("http://localhost:8000/")
        time.sleep(10)

        # Нажимаем Start
        start_button = driver.find_element(By.ID, "startBtn")
        start_button.click()

        print("Start button clicked.")

        # Ждём 20 сек
        time.sleep(20)

        # Нажимаем Stop
        stop_button = driver.find_element(By.ID, "stopBtn")
        stop_button.click()

        print("Stop button clicked.")

        logs_div = driver.find_element(By.ID, "logs")
        logs_text = logs_div.text
        assert "Started" in logs_text, "Log does not contain 'Started'"
        assert "Stopped" in logs_text, "Log does not contain 'Stopped'"

        print("Test passed.")

    except AssertionError as e:
        print(f"Test failed: {e}")

    finally:
        driver.quit()
