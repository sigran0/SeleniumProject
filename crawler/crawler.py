
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep

from bs4 import BeautifulSoup

#   dealymdtype : p 고정
select_id_list = ['dealtype', 'bldtype', 'cmbSgg', 'cmbEmd', 'deal_y', 'deal_q']

##  dealtype : buy, rent
##  bldtype : apt, mhouse, shouse, office, land
##  cmbSgg : number
##  cmbEmd : number
##  deal_y : 2017 ~ 2005
##  deal_p : 1 ~ 12

select_value_list = [
    ['buy'],
    ['apt'],
    ['28710', '28245', '28170', '28200', '28140', '28237', '28260', '28185', '28720', '28110'],
    None,
    [y for y in range(2005, 2017 + 1)],
    [p for p in range(1, 4 + 1)]
]

dealtype = 0
bldtype = 1
cmbSgg = 2
cmbEmd = 3
deal_y = 4
deal_q = 5

selected_value = ['buy', 'apt', '28710', '28710250', '2017', '4']

counter = 0

quarter = 0
year = 0
dong = ''
gu = ''

def make_selector(id, msg):
    return '# ' + id + ' > ' + msg


def traval_deal_q(f):
    select = Select(driver.find_element_by_id('deal_q'))


    for index in range(0, len(select_value_list[deal_q])):
        select.select_by_value(str(select_value_list[deal_q][index]))

        global quarter

        quarter = str(select_value_list[deal_q][index])

        global counter

        counter += 1
        #print(counter)

        click_search_button()

        souping(f)

def traval_deal_y(f):
    select = Select(driver.find_element_by_id('deal_y'))

    for index in range(0, len(select_value_list[deal_y])):
        select.select_by_value(str(select_value_list[deal_y][index]))

        global year

        year = str(select_value_list[deal_y][index])

        traval_deal_q(f)


def traval_cmbEmd(f):
    select = Select(driver.find_element_by_id('cmbEmd'))

    driver.implicitly_wait(1)
    sleep(1)

    for index in range(0, len(select_value_list[cmbEmd])):
        select.select_by_value(str(select_value_list[cmbEmd][index]))

        txt = select.first_selected_option.text

        global dong

        dong = txt
        traval_deal_y(f)


def traval_cmbSgg(f):
    select = Select(driver.find_element_by_id('cmbSgg'))

    for index in range(0, len(select_value_list[cmbSgg])):
        select.select_by_value(str(select_value_list[cmbSgg][index]))

        txt = select.first_selected_option.text

        global gu

        gu = txt

        driver.implicitly_wait(1)
        sleep(1)

        reload_cmbEmd()
        traval_cmbEmd(f)


def traval_bldtype(f):
    select = Select(driver.find_element_by_id('bldtype'))

    for index in range(0, len(select_value_list[bldtype])):
        select.select_by_value(str(select_value_list[bldtype][index]))
        traval_cmbSgg(f)


def traval_dealtype(f):
    select = Select(driver.find_element_by_id('dealtype'))

    for index in range(0, len(select_value_list[dealtype])):
        select.select_by_value(str(select_value_list[dealtype][index]))
        traval_bldtype(f)


def reload_cmbEmd():

    select_value_list[3] = get_select_item_values('cmbEmd')


def start_travel(f):
    select = Select(driver.find_element_by_id('dealymdtype'))
    select.select_by_value('q')
    reload_cmbEmd()

    traval_dealtype(f)


def select_option():

    for c in range(0, len(select_id_list)):
        select = Select(driver.find_element_by_id(select_id_list[c]))
        select.select_by_value(selected_value[c])


def get_select_item_values(_id):
    el = driver.find_element_by_id(_id)
    result = []
    for option in el.find_elements_by_tag_name('option'):
        if option.get_attribute('value') != '':
            result.append(option.get_attribute('value'))
    return result


def click_search_button():
    driver.find_element_by_css_selector("button.btn").click()

    driver.implicitly_wait(2)
    sleep(2)

get_id = lambda tr : tr.get('id')

def find_title(tr):
    selector = make_selector(get_id(tr), 'td.danji > a')
    return tr.select(selector)

def get_title(str):
    good = str.split(' ')
    title = ' '.join(a for a in good[0:-2]).strip()
    bunji = good[-2]
    area = good[-1]

    return (title, bunji, area)


def souping(f):
    tbody = driver.find_element_by_css_selector('#list_result > tbody:nth-child(2)')
    #print(tbody.text)

    strs = tbody.text.split('\n')

    saver = []
    title = ''
    bunji = ''
    area = ''

    for str in strs:

        if str != '':
            saver.append(str)
        else:
            if len(saver) > 3:
                _title, bunji, area = get_title(saver[0])
                title = _title
                saver = saver[1:]

            if len(saver) > 0:
                try:
                    date = saver[0].split('.')

                    month = date[0]
                    day = date[1]

                    won = ''.join(a for a in saver[1].split(','))
                    floor = saver[2]
                    result = gu + '\t' + dong + '\t' + year + '\t' + quarter + '\t' + month + '\t' + day + '\t' + title + '\t' + bunji + '\t' + won + '\t' + floor + '\t' + area + '\n'

                    f.write(result)

                    print(gu, dong, year, month, day, quarter, title, bunji, won, floor, area)
                except IndexError:
                    print(saver)

            saver = []


with open('good.txt', 'w') as f:
    f.write('구\t동\t연도\t분기\t월\t일\t건물이름\t번지\t가격\t층\t면적\n')

    driver = webdriver.Chrome('../driver/chromedriver')
    driver.implicitly_wait(3)
    driver.get('http://imap.incheon.go.kr/land/rtmsinfo.jsp')
    start_travel(f)


#   https://nid.naver.com/nidlogin.login
#   http://imap.incheon.go.kr/land/rtmsinfo.jsp

#   select = Select(driver.find_element_by_id('bldtype'))
#   select.select_by_value('office')

#driver.find_element_by_xpath("//select[@id='bldtype']/option[text()='mhouse']").click()