from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pickle
from selenium.webdriver.chrome.options import Options

# take the link to the facebook post
post = input("please input a link to the facebook post you want to scrap: ")
if post[:25] == "https://www.facebook.com/":
    pass
elif post[:17] == "www.facebook.com/":
    post = "https://" + post
elif post[:17] == "https://fb.watch/":
    pass  #WJgMKdq@:=4&=*B
else:
    print("link is not correct")


# setup the chrome driver
opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("--disable-extensions")
opt.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
driver = webdriver.Chrome(options=opt)

try:  # try to get cookies

    driver.get(post)
    cookies = pickle.load(open("cookies.txt", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()

except FileNotFoundError:  # when there is no cookies try to log in

    driver.get("https://www.facebook.com")
    email = driver.find_element_by_xpath('//*[@id="email"]')
    user_mail = input("please enter your mail to login to facebook: ")
    email.send_keys(user_mail)
    password = driver.find_element_by_xpath('//*[@id="pass"]')
    user_password = input("please enter password: ")
    password.send_keys(user_password)
    password.send_keys(Keys.RETURN)
    time.sleep(3)
pickle.dump(driver.get_cookies(), open("cookies.txt", "wb"))   # save cookies

# proceed to the target page
driver.get(post)
time.sleep(5)

# open reaction bar
try:
    num_of_likes = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div[4]/div[1]/div/div/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div')
except:
    try:
        num_of_likes = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div/div[1]/div/div[1]/div/span/div')
    except:
        try:

            num_of_likes = driver.find_element_by_xpath('//*[@id="watch_feed"]/div/div[1]/div[1]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div')
        except:
            num_of_likes = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[3]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[1]/div/div[1]/div/span/div')
num_of_likes.click()

# make sure that all reactions are loaded
time.sleep(5)
reaction_body = driver.find_element_by_xpath('//*[@id="mount_0_0"]/div/div[1]/div[1]/div[4]/div/div/div[1]/div/div[2]/div/div/div/div[3]')
for i in range(1000):
    driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', reaction_body)


# get the link of the user
time.sleep(7)
people = reaction_body.find_elements_by_tag_name('a')
links = []
ids = []
for person in people:
    links.append(person.get_attribute('href'))


# extract the id from the links
for link in links:
    if link[:33] == "https://www.facebook.com/stories/":
        continue
    elif link[:33] == "https://www.facebook.com/profile.":
        if link[40:55] + "\n" not in ids:
            ids.append(link[40:55] + "\n")
    elif "https://www.facebook.com/" in link:
        if link[25:link.index("?")] + "\n" not in ids:
            ids.append(link[25:link.index("?")] + "\n")
    else:
        print(link)

# save the ids in a txt file
ids_file = open("ids.txt", "w")
ids_file.writelines(ids)
ids_file.close()

driver.close()
