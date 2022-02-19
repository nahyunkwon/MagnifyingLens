from selenium import webdriver
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotInteractableException
#from selenium.common.exceptions import ElementClickInterceptedException
import time
import pandas as pd
import requests
from requests.exceptions import SSLError
from urllib3.exceptions import MaxRetryError
import re
import os
import pathlib


def get_image_urls(url):
    chromedriver_path = '/Users/kwon/PycharmProjects/MagAccess/google_scraper/chromedriver'
    driver = webdriver.Chrome(chromedriver_path)
    driver2 = webdriver.Chrome(chromedriver_path)
    driver.implicitly_wait(5)

    driver.get(url)

    result = []
    related_images_url = []

    time.sleep(20)

    thumbnail_images = driver.find_elements_by_class_name("rg_i")

    for i in range(0, 200):
        try:
            thumbnail_image = thumbnail_images[i]
            thumbnail_image.click()
            image = driver.find_elements_by_css_selector(".n3VNCb")

            time.sleep(10)
            result.clear()

            for k in image:
                src = k.get_attribute("src")
                # avoid scraping thumbnail images below the target image
                if "http" in src:
                    if "jpg" in src or "jpeg" in src or "png" in src:
                        show_more = driver.find_elements_by_css_selector(".So4Urb")[0]
                        related_url = show_more.get_attribute('href')

                        result.append([str(i), src, related_url])
                        print(result)

                        driver2.get(related_url)

                        for j in range(0, 2):

                            thumbnail_image_related = driver2.find_elements_by_class_name("rg_i")[j]
                            thumbnail_image_related.click()
                            related_images = driver2.find_elements_by_css_selector(".n3VNCb")

                            time.sleep(8)

                            related_images_url.clear()
                            for r in related_images:
                                src2 = r.get_attribute("src")
                                if "http" in src2:
                                    if "jpg" in src2 or "jpeg" in src2 or "png" in src2:
                                        related_images_url.append([str(i) + "-" + str(j), src2])
                                        print(related_images_url)

                            try:
                                result_df_2 = pd.DataFrame(related_images_url, columns=['index', 'img_url'])
                                result_df_2.to_csv("./result_google_search.csv", mode='a', header=False,
                                                 index=False)
                            except IndexError:
                                pass

            print("----")

            try:
                result_df = pd.DataFrame(result, columns=['index', 'img_url', 'related_images'])
                result_df.to_csv("./result_google_search.csv", mode='a', header=False, index=False)
            except IndexError:
                pass

            time.sleep(5)

        except ElementNotVisibleException:
            pass
        except ElementNotInteractableException:
            pass
        #except ElementClickInterceptedException:
           # pass

    driver.quit()
    driver.close()


def download_images_from_urls():

    urls = pd.read_csv("./result_google_search.csv")

    for i in range(0, len(urls)):
        print(urls.iloc[i])

        try:
            response = requests.get(urls.iloc[i][1])

            file = open("./image_light_switch/" + str(urls.iloc[i][0]) + ".jpg", "wb")
            file.write(response.content)
            file.close()
        except SSLError:
            pass
        except MaxRetryError:
            pass
        except:
            pass


def get_image_title():

    urls = pd.read_csv("./result.csv")

    title = []

    for i in range(0, len(urls)):

        url_parts = re.split("/|\?", urls.iloc[i][1])

        for part in url_parts:
            if "jpg" in part:
                title.append(part.split(".jpg")[0])
                break
            elif "jpeg" in part:
                title.append(part.split(".jpeg")[0])
                break
            elif "png" in part:
                title.append(part.split(".png")[0])
                break

    urls['title'] = title

    urls.to_csv("./result_title_added.csv", index=False)


def get_valid_images():

    images = pd.read_csv("./image-urls-duplicates-marked.csv")

    valid = []

    for i in range(len(images)):
        # valid images
        if images.iloc[i]['valid'] != 1:
            valid.append(images.iloc[i]['index'])

            try:
                response = requests.get(images.iloc[i]['image_url'])

                image_format = images.iloc[i]['image_url'].split(".")[-1]

                if "?" in image_format:
                    image_format = image_format.split("?")[0]

                file = open("./valid_images/" + str(images.iloc[i]['index']) + "." + image_format, "wb")
                file.write(response.content)
                file.close()
            except SSLError:
                pass
            except MaxRetryError:
                pass

    #os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")


def remove_dups():

    result_df = pd.read_csv("./result_related.csv")
    new_df = result_df.drop_duplicates(subset=['url'])

    print(result_df)
    print(new_df)

    new_df.to_csv("./related_images_remove_dups.csv", header=True)


if __name__ == "__main__":
    #remove_dups()
    #light_switch = 'https://www.google.com/search?q=light+switch&client=safari&rls=en&sxsrf=APq-WBvNiXuT-YkD1-cjUBgb9GY9sTKWoA:1644286047448&source=lnms&tbm=isch&sa=X&ved=2ahUKEwjA-5Dugu_1AhUYk2oFHaT6C8IQ_AUoAnoECAIQBA&biw=1427&bih=716&dpr=2'
    #get_image_urls(light_switch)
    download_images_from_urls()

