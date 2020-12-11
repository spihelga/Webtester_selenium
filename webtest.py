import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

# This example requires Selenium WebDriver 3.13 or newer

#Path to Chrome webdriver
PATH = "./drivers/chromedriver"
driver = webdriver.Chrome(PATH)
website = str("https://www.lhv.ee/et/liising")

def screensh():

    now = datetime.now()
    nowstr = now.strftime("%d-%m-%Y-%H-%M-%S" + ".png")
    screen_path = "./screenshots/" + nowstr
    driver.save_screenshot(screen_path)

with driver as driver:

    driver.get(website)

    #"Eraisikuna" is chosen for soovin liisingut
    if driver.find_element(By.ID, "account_type-1").is_selected() == False:
        print("Juriidilise isikuna has not been chosen")
    if driver.find_element(By.ID, "account_type-0").is_selected() == True:
        print("Eraisikuna has been chosen")
    #"Kasutusrent is chosen"
    if driver.find_element(By.ID, "kap_rent").is_selected() == True:
        print("Kapitalirent has been chosen")
    if driver.find_element(By.ID, "kas_rent").is_selected() == False:
        print("Kasutusrent has not been chosen")

    #Save the initial "Kuumakse"
    payment = driver.find_element_by_css_selector(".payment")
    payment_str = payment.text
    payment_int = int(float(payment_str))

    #Clear price field and set price
    driver.find_element(By.NAME, "price").clear()
    driver.find_element(By.NAME, "price").send_keys("17000")
    price = int(driver.find_element(By.NAME, "price").get_attribute("value"))
    pricestr = str(price)
    print("Price is set to: : " + pricestr)

    payment2 = driver.find_element_by_css_selector(".payment")
    payment_str2 = payment2.text
    payment_int2 = int(float(payment_str2))

    if payment_int != payment_int2:
        print("Payment has been changed to " + payment_str2)
    elif payment_int == payment_int2:
        print("Payment should have changed, but did not")

    #Check if vat is included
    if driver.find_element(By.ID, "vat_included").is_selected() == True:
        print("VAT is included")
    else:
        print("VAT not included")

    #Set initial percentage
    driver.find_element(By.NAME, "initial_percentage").clear()
    driver.find_element(By.NAME, "initial_percentage").send_keys("10")
    init_perc = int(driver.find_element(By.NAME, "initial_percentage").get_attribute("value"))
    init_perc_str = str(init_perc)
    print("Initial percentage is set to: " + init_perc_str)

    #Check if initial percentage sum is correct
    init_sum = int(driver.find_element(By.NAME, "initial").get_attribute("value"))
    calc_perc_sum = price * init_perc / 100
    calc_perc_sum_str = str(calc_perc_sum)

    if calc_perc_sum == init_sum:
        print("Initial sum is calculated correctly (" + calc_perc_sum_str + ")")
    else:
        print("Initial sum calculation is not correct")

    #Select 5 years, check if there are at least 6 years in list
    Select(driver.find_element(By.NAME, "years")).select_by_value("60")
    sel_years = driver.find_element(By.NAME, "years").get_attribute("value")
    print("Selected years (value in months) " + sel_years + " / 12 months")

    print("Available options for years: ")
    elements=driver.find_elements_by_name("years")
    select_box = driver.find_element_by_name("years")
    years = [x for x in select_box.find_elements_by_tag_name("option")]
    for element in years:
        print (element.get_attribute("value"))
    len_years = str(len(years))
    print("There are " + len_years + " years in list")

    #Select 1 month, check if there are 12 months
    Select(driver.find_element(By.NAME, "months")).select_by_value("1")
    sel_months = driver.find_element(By.NAME, "months").get_attribute("value")
    print("Selected months: " + sel_months)

    print("Available options for months: ")
    elements=driver.find_elements_by_name("months")
    select_box = driver.find_element_by_name("months")
    months = [x for x in select_box.find_elements_by_tag_name("option")]
    for element in months:
        print (element.get_attribute("value"))
    len_months = str(len(months))
    print("There are " + len_months + " months in list")

    #Set interest rate to 3 percent
    driver.find_element(By.NAME, "interest_rate").clear()
    driver.find_element(By.NAME, "interest_rate").send_keys("3")
    inte_rate = driver.find_element(By.NAME, "interest_rate").get_attribute("value")
    print("Interest rate is set to: " + inte_rate)

    #Set reminder percentage
    driver.find_element(By.NAME, "reminder_percentage").clear()
    driver.find_element(By.NAME, "reminder_percentage").send_keys("15")
    remin_prec = driver.find_element(By.NAME, "reminder_percentage").get_attribute("value")
    print("Reminder percent is set to: " + remin_prec)

    #Check if reminder sum is correct
    remin_sum = int(driver.find_element(By.NAME, "reminder").get_attribute("value"))
    remi_perc_int = int(remin_prec)
    rem_calc_sum = price * (remi_perc_int / 100)
    rem_calc_sum_str = str(rem_calc_sum)
    print("Reminder sum should be: " + rem_calc_sum_str)

    if remin_sum == rem_calc_sum:
        print("Reminder is calculated correctly (" + rem_calc_sum_str + ")")
    else:
        print("Reminder calculation is not correct")

    #Check once again if "kuumakse" has been changed
    payment3 = driver.find_element_by_css_selector(".payment")
    payment_str3 = payment3.text
    payment_int3 = int(float(payment_str3))

    if payment_int2 != payment_int3:
        print("Payment has been changed to " + payment_str3)
    elif payment_int2 == payment_int3:
        print("Payment should have changed, but did not")

    Check_Button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Taotle liisingut")))

    screensh()
    time.sleep(2) # wait for some time to check the result

driver.quit()
