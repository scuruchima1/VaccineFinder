import requests
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.common.exceptions import NoSuchElementException        
import time
import pprint
import config 
import discord

# zocdoc - https://www.zocdoc.com/vaccine/search/IL?flavor=state-search
# cvs - https://www.cvs.com/immunizations/covid-19-vaccine
# walmart - https://www.walmart.com/pharmacy/clinical-services/immunization/scheduled?imzType=covid&action=PswdReset&rm=x
# sam's club - https://www.samsclub.com/pharmacy/immunization?imzType=covid
# walgreens - https://www.walgreens.com/findcare/vaccination/covid-19/location-screening
# uic - https://mychart-openscheduling.et1085.epichosted.com/MyChart/SignupAndSchedule/EmbeddedSchedule?id=30301&dept=10127001&vt=1055
# costco #1 - https://book-costcopharmacy.appointment-plus.com/cttc019c/?e_id=5439#/
# costco #2 - https://book-costcopharmacy.appointment-plus.com/cttb5n42/?e_id=5435#/ 
# jewel-osco - https://www.mhealthappointments.com/covidappt
# mariano's - https://www.marianos.com/rx/covid-eligibility

#Check for vaccines, send message through discord
client = discord.Client()

def zocdocCheck(driver):
    driver.get("https://www.zocdoc.com/vaccine")
    Select(driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/section/div/div/div/div/div/div/select')).select_by_visible_text('Illinois')
    driver.find_element_by_xpath('//*[@id="main"]/div/div[1]/section/div/div/div/div/button').click()
    driver.find_element_by_xpath('//*[@id="age-input"]').send_keys('50')
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div[1]/button').click()
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div[2]/div[1]/div[2]/div[1]/label/span[1]/input').click()
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div[2]/div[2]/div[2]/div[1]/label/span[1]/input').click()
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div[2]/div[3]/div[2]/div[1]/label/span[1]/input').click()
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div[2]/button').click()
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div[6]/div[1]/div[2]/div[2]/label/span[1]/input').click()
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div[6]/div[2]/div[2]/div[2]/label/span[1]/input').click()
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div[6]/div[3]/div[2]/div[2]/label/span[1]/input').click()
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div[6]/div[4]/div[2]/div[2]/label/span[1]/input').click()
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div[6]/button').click()
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div[8]/div/div/div/label/input').click()
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[3]/div/div[8]/button').click()

    # Cycling through all providers in ZocDoc
    for articleNumber in range(1,18):
        path = '//*[@id="main"]/div[1]/main/div/div[2]/div/div/div/div/section/article[' + str(articleNumber) + ']/div/div[2]/div/div'
        if driver.find_element_by_xpath(path).text != "No upcoming appointments available":
            print("ZocDoc Ran")         
            return True
    driver.find_element_by_xpath('//*[@id="main"]/div[1]/main/div/nav/span[2]/a').click()
    if driver.find_element_by_xpath('//*[@id="main"]/div[1]/main/div/div[2]/div/div/div/div/section/article/div/div[2]/div/div').text != "No upcoming appointments available":
        print("ZocDoc Ran")  
        return True
    print("ZocDoc Ran")
    return False

def cvsCheck(driver):
    driver.get("https://www.cvs.com/immunizations/covid-19-vaccine?icid=cvs-home-hero1-link2-coronavirus-vaccine")
    driver.find_element_by_xpath('/html/body/content/div/div/div/div[3]/div/div/div[2]/div/div[5]/div/div/div/div/div/div[1]/div[2]/div/div[2]/div/div/div/div/div[1]/ul/li[11]/div/a/span').click()
    if driver.find_element_by_xpath('/html/body/div[2]/div/div[17]/div/div/div/div/div/div[1]/div[2]/div/div/div[2]/div/div[6]/div/div/table/tbody/tr[2]/td[2]/span').text != "Fully Booked":
        print("CVS Ran")
        return True
    print("CVS Ran")
    return False

#Needs Firefox profile to have walmart sign in
def walmartCheck(driver):
    driver.get('https://www.walmart.com/pharmacy/clinical-services/immunization/scheduled?imzType=covid')
    if driver.find_element_by_xpath('/html/body/div/div/div[1]/article/section[3]/section/div[2]/div/div[2]/h1').text != 'Not available in this area - yet':
        print('Walmart Ran')
        return True
    print('Walmart Ran')
    return False

#Can't click on box, fix later, lower priority
def samsclubCheck(driver):
    driver.get('https://www.samsclub.com/pharmacy/immunization/form?imzType=covid')
    time.sleep(10)
    driver.find_element_by_xpath('//*[@id="inputbox1"]').click()
    driver.find_element_by_xpath('//*[@id="inputbox1"]').send_keys('Chicago')
    driver.find_element_by_xpath('//*[@id="main"]/div/div/div[1]/div[2]/div/div/div/div/form/div[2]/button').click()
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[2]/div/div/div[1]/div[2]/div/div/div[2]/button').click()
    action = ActionChains(driver)
    action.click_and_hold(on_element=driver.find_element_by_xpath('/html/body'))
    action.perform()
    time.sleep(5)
    action.release()
    return None

def walgreensCheck(driver):
    driver.get('https://www.walgreens.com/findcare/vaccination/covid-19/location-screening')
    driver.find_element_by_xpath('//*[@id="inputLocation"]').clear()
    driver.find_element_by_xpath('//*[@id="inputLocation"]').send_keys('Chicago')
    driver.find_element_by_xpath('//*[@id="wag-body-main-container"]/section/section/section/section/section[2]/div/span/button').click()
    #//*[@id="wag-body-main-container"]/section/section/section/section/section[2]/p for vaccine available
    try:
        driver.find_element_by_xpath('//*[@id="wag-body-main-container"]/section/section/section/section/section[1]/p')
    except NoSuchElementException:
        print('Walgreens Ran')
        return True
    print('Walgreens Ran')
    return False

def uicCheck(driver):
    return None

def costcooneCheck(driver):
    driver.get('https://book-costcopharmacy.appointment-plus.com/cttc019c/?e_id=5439#/')
    driver.find_element_by_xpath('//*[@id="page-content"]/div/div[2]/div[3]/ul/li/a').click()
    time.sleep(1)
    if driver.find_element_by_xpath('//*[@id="SelectEmployeeView"]/div[1]/div/div[2]/p').text != "We're sorry, but no clinics are available for the you selected. Please choose another clinic.":
        print('Costco 1 Ran')
        return True
    print('Costco 1 Ran')
    return False

def costcotwoCheck(driver):
    driver.get('https://book-costcopharmacy.appointment-plus.com/cttb5n42/?e_id=5435#/book-appointment/select-date-and-time?_qk=feid9i3ede')
    if driver.find_element_by_xpath('//*[@id="page-content"]/div/div[2]/div/div[3]/div/span[1]').text != "We’re sorry, but there are not available times.  Please select either a new":
        print('Costco 2 Ran')
        return True
    print('Costco 2 Ran')
    return False

def jeweloscoCheck(driver):
    return None

def marianosCheck(driver):
    return None

@client.event
async def on_ready():
    while True:
        driver = webdriver.FirefoxProfile(config.firefoxprofpath)
        driver.set_preference('dom.webdriver.enabled',False)
        driver = webdriver.Firefox(executable_path=config.geckopath,firefox_profile=driver)
        driver.implicitly_wait(15)
        if zocdocCheck(driver) == True:
            await client.guilds[0].channels[2].send(f"**Vaccine Found!**\nhttps://www.zocdoc.com/vaccine/search/IL?flavor=state-search")
        if cvsCheck(driver) == True:
            await client.guilds[0].channels[2].send(f"**Vaccine Found!**\nhttps://www.cvs.com/immunizations/covid-19-vaccine?icid=cvs-home-hero1-link2-coronavirus-vaccine")
        if walmartCheck(driver) == True:
            await client.guilds[0].channels[2].send(f"**Vaccine Found!**\nhttps://www.walmart.com/pharmacy/clinical-services/immunization/scheduled?imzType=covid")
        driver.implicitly_wait(2)
        if walgreensCheck(driver) == True:
            await client.guilds[0].channels[2].send(f"**Vaccine Found!**\nhttps://www.walgreens.com/findcare/vaccination/covid-19/location-screening")
        driver.implicitly_wait(15)

        driver.quit()
        time.sleep(80)

client.run(config.discordbotapikey)