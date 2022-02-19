from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
import time
import pandas as pd
import requests
from requests.exceptions import SSLError
from urllib3.exceptions import MaxRetryError


def test_driver(url):
    driver = webdriver.Chrome('/Users/kwon/PycharmProjects/MagAccess/google_scraper/chromedriver')
    driver.implicitly_wait(30)

    driver.get(url)

    result = []


    #thumbnail_image = driver.find_elements_by_class_name("rg_i")

    thumbnail_image = driver.find_elements(".rg_i")

    print(thumbnail_image)
    thumbnail_image.click()

    #print(thumbnail_image)
    #thumbnail_image.click()
    #image = driver.find_elements_by_css_selector(".n3VNCb")

    time.sleep(10)
    result.clear()



def get_image_urls(url):
    driver = webdriver.Chrome('/Users/kwon/PycharmProjects/MagAccess/google_scraper/chromedriver')
    driver.implicitly_wait(30)

    driver.get(url)

    result = []

    #time.sleep(30)

    thumbnail_images = driver.find_elements_by_class_name("rg_i")

    for i in range(1000):
        try:
            thumbnail_image = thumbnail_images[i]
            #print(thumbnail_image)
            thumbnail_image.click()
            image = driver.find_elements_by_css_selector(".n3VNCb")

            time.sleep(10)

            for k in image:
                src = k.get_attribute("src")
                # avoid scraping thumbnail images below the target image
                if "http" in src:
                    if "jpg" in src or "jpeg" in src or "png" in src:
                        result.append([str(i), src])
                        print(result)
            print("----")

            try:
                result_df = pd.DataFrame(result, columns=['index', 'img_url'])
                result_df.to_csv("./result.csv", mode='a', header=False, index=False)
            except IndexError:
                print('indexerror')
                pass

            time.sleep(5)

        except ElementNotVisibleException:
            pass
        except:
            pass

    driver.quit()
    driver.close()


def download_images_from_urls():

    urls = pd.read_csv("./result.csv")

    for i in range(90, len(urls)):
        print(urls.iloc[i])

        try:
            response = requests.get(urls.iloc[i][1])

            file = open("./image_with_supports/" + str(urls.iloc[i][0]) + ".jpg", "wb")
            file.write(response.content)
            file.close()
        except SSLError:
            pass
        except MaxRetryError:
            pass


if __name__ == "__main__":
    #download_images_from_urls()
    light_switch = 'https://www.google.com/search?q=light+switch&client=safari&rls=en&sxsrf=APq-WBvNiXuT-YkD1-cjUBgb9GY9sTKWoA:1644286047448&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjA-5Dugu_1AhUYk2oFHaT6C8IQ_AUoAnoECAIQBA&biw=1427&bih=716&dpr=2'
    get_image_urls(light_switch)
    #test_driver(light_switch)