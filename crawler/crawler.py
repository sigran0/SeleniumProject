
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from bs4 import BeautifulSoup

#   dealymdtype : p 고정
select_id_list = ['dealtype', 'bldtype', 'cmbSgg', 'cmbEmd', 'deal_y', 'deal_p']

##  dealtype : buy, rent
##  bldtype : apt, mhouse, shouse, office, land
##  cmbSgg : number
##  cmbEmd : number
##  deal_y : 2017 ~ 2005
##  deal_p : 1 ~ 12

select_value_list = [
    ['buy', 'rent'],
    ['apt', 'mhouse', 'shouse', 'office', 'land'],
    ['28710', '28245', '28170', '28200', '28140', '28237', '28260', '28185', '28720', '28110'],
    None,
    [y for y in range(2005, 2017 + 1)],
    [p for p in range(1, 12 + 1)]
]

selected_value = ['buy', 'apt', '28710', '28710250', '2017', '1']


def start_travel():
    select = Select(driver.find_element_by_id('dealymdtype'))
    select.select_by_value('p')
    select_option()
    select_value_list[3] = get_select_item_values('cmbEmd')
    travel_select_option(5, 0)


def select_option():

    for c in range(0, len(select_id_list)):
        select = Select(driver.find_element_by_id(select_id_list[c]))

        select.select_by_value(selected_value[c])


def travel_select_option(current_position, current_cursor):

    print('fucking')

    cursour_size = len(select_value_list[current_position])

    driver.implicitly_wait(5)

    select_option()
    selected_value[current_position] = select_value_list[current_position][current_cursor]

    if current_cursor >= cursour_size:

        if current_position == 2:   #   리플레쉬 해줘야함
            select_value_list[3] = get_select_item_values('cmbEmd')
        elif current_position == 0: #   끝나는 경우
            return

        travel_select_option(current_position - 1, 0)
    else:
        print(current_position, current_cursor + 1)
        travel_select_option(current_position, current_cursor + 1)


def get_select_item_values(_id):
    el = driver.find_element_by_id(_id)
    result = []
    for option in el.find_elements_by_tag_name('option'):
        if option.get_attribute('value') != '':
            result.append(option.get_attribute('value'))
    return result

driver = webdriver.Chrome('../driver/chromedriver')
driver.implicitly_wait(3)
driver.get('http://imap.incheon.go.kr/land/rtmsinfo.jsp')
start_travel()


#   https://nid.naver.com/nidlogin.login
#   http://imap.incheon.go.kr/land/rtmsinfo.jsp

#   select = Select(driver.find_element_by_id('bldtype'))
#   select.select_by_value('office')

#driver.find_element_by_xpath("//select[@id='bldtype']/option[text()='mhouse']").click()