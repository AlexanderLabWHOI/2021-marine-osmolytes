from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys
import os

Gbact = 'OM-RGCv2+G - Tara Oceans Microbiome Reference Gene Catalog v2+ metaG Arctic Inside (prokaryotes)'
Geuk = 'MATOUv1+G - Marine Atlas of Tara Oceans Unigenes +metaG (eukaryotes)'
Tbact = 'OM-RGCv2+T - Tara Oceans Microbiome Reference Gene Catalog v2+ metaT Arctic Inside (prokaryotes)'
Teuk = 'MATOUv1+T - Marine Atlas of Tara Oceans Unigenes +metaT (eukaryotes)'
all_searches = [Gbact, Geuk, Tbact, Teuk]
all_searches_named = ['Gbact', 'Geuk', 'Tbact', 'Teuk']
hmm_folder = "/Users/halexand/Projects/2021-Osmolytes/tara-scraping/hmms/"
outdf = {}
KO = sys.argv[1]

for search_type, search_name in zip(all_searches, all_searches_named):
    #open webdriver 
    driver = webdriver.Firefox()
    #go to website
    driver.get("http://tara-oceans.mio.osupytheas.fr/ocean-gene-atlas")
    #get current url
    current_url = driver.current_url    
    #set the database
    select = Select(driver.find_element_by_id('DB'))
    select.select_by_visible_text(search_type)
    #set the job name
    name_element = driver.find_element_by_id("job")
    name_element.send_keys(KO+'_'+search_name)
    #select hmm and load file
    driver.find_element_by_id("HMM_radio").click()
    hmm_file = driver.find_element_by_id("hmm_file_upload")
    hmm_file.send_keys(os.path.join(hmm_folder, KO+".hmm"))
    #select abundance metric
    abd = Select(driver.find_element_by_id('normalize'))
    abd.select_by_visible_text('percent of mapped reads')
    #submit
    driver.find_element_by_id("submit_button").click()
    #wait for new website and print url
    WebDriverWait(driver, 45).until(EC.url_changes(current_url))
    
    new_url = driver.current_url
    outdf[search_name]=new_url
    print(new_url)
    driver.close()
    time.sleep(30)

with open(KO+".outfile.list", 'w') as f:
    for i in outdf:
        f.write(i)
        f.write('\t')
        f.write(outdf[i])
        f.write('\n')
f.close()
