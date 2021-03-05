from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os
import glob


def downloader() :
    print("File Download Started")
    time.sleep(0.5)
    while True:
        file = glob.glob(os.path.join(download_dir,'*.part'))
        if file:
            print("...")
            time.sleep(10)
            continue
        else:
            time.sleep(30)
            print('File Downloaded')
            break

basedir = '/Users/halexand/Projects/2021-Osmolytes/tara-scraping/downloads'
ko_file = sys.argv[1]
kname = ko_file.split('.')[0]

with open (ko_file) as f:
    for line in f:
        ftype, url = line.split('\t')
        download_dir = os.path.join(basedir, kname, ftype)
        profile = webdriver.FirefoxProfile()
        profile.set_preference('browser.download.folderList', 2) # custom location
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', download_dir)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream, application/excel, application/vnd.ms-excel")
        if not os.path.exists(download_dir):
            os.makedirs(download_dir)

        driver = webdriver.Firefox(firefox_profile=profile)
        driver.get(url)
        file_download_list = ["Download abundances of the homologs and environmental data","Download alignment results file",]#"Download homolog sequences as zipped FASTA files",]#]
        for file in file_download_list:
            driver.find_element_by_link_text(file).click()
            downloader()
            list_of_files = glob.glob(os.path.join(download_dir,'*'))
            latest_file = max(list_of_files, key=os.path.getctime)
            # if latest_file.endswith('.tsv'):
            #     time.sleep(30)
            os.rename(latest_file, os.path.join(download_dir, '_'.join(os.path.basename(latest_file).split(' ')[1].split('_')[1:])))
        time.sleep(15)
        driver.close()
# while not os.path.exists(file_path):
#     time.sleep(1)
#
# if os.path.isfile(file_path):
#     # read file
# else:
#     raise ValueError("%s isn't a file!" % file_path)
#


# driver.find_element_by_partial_link_text("Download alignment results file").click()
# driver.find_element_by_partial_link_text("Download abundances of the homologs and environmental data").click()
# driver.close()
