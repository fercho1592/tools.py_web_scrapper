from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


loginPage = "https://zonatmo.com/login"
url = "https://zonatmo.com/library/manhwa/47049/lavidadespuesdelamuerte"

def main():
    try:
        print("Opening browser...")
        driver = webdriver.Firefox()
        driver.get(url)

        bookThumbnail = driver.find_element(By.CLASS_NAME, "book-thumbnail")
        wait = WebDriverWait(driver, timeout=5)
        wait.until(lambda d : bookThumbnail.is_displayed())

        print(f"Title page: {driver.title}")
        input("Press Enter to continue...")

        # Get last seen chapter
        buttonShowChapters = driver.find_element(By.ID, "show-chapters")
        buttonShowChapters.click()
        # Check current page
        print(f"Title page: {driver.title}")
        input("Press Enter to continue...")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
