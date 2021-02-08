import selenium.webdriver as SW

with open('password.txt', 'r') as f:
    password = f.read()

options = SW.ChromeOptions()
options.add_argument('--disable-inforbars')
# options.add_argument('--kiosk ')
browser = SW.Chrome(options=options)
browser.get("https://www.facebook.com")

# css_selector
input_username = browser.find_element_by_css_selector('input#email')
input_username.send_keys("andychen208@gmail.com")
input_username = browser.find_element_by_css_selector('input#pass')
input_username.send_keys(password)
input_username.send_keys('\n')

# sometime will encounter the situation of fb'AB_test
# input_username = browser.find_element_by_css_selector('input[name="email"]')
# input_username = browser.find_element_by_css_selector('input[name="pass"]')
