## this toolkit is used to find users and validate email addresses found in user bio 

from selenium import webdriver 

from selenium.webdriver.common.keys import Keys 

from selenium.webdriver.firefox.options import Options 

from user_agent import generate_user_agent, generate_navigator


from c0nf import usrname , passwrd

import re , time 


import instaloader  

import pyautogui 




tmp_usragent = generate_user_agent()

options = Options() 
options.add_argument(f"user-agent={tmp_usragent}")
options.add_argument("--disable-popup-blocking");
#options.set_preference('dom.webnotifications.enabled', False)
#options.headless = True 




all_mails_found = [] 

usrs = [] 




def send_mail(mail):
    """
        sends a POST request to the server to be added to the database 
    """

    try:
        data = {"mail":f"{mail}"}
            
        response = requests.post("http://192.168.1.9:5000/add" , params = data )
        print (response.text , response.status_code )
    except:
        print ("Encountered an Error ")







def get_followers(acc):
    L = instaloader.Instaloader()
    
    print (L)
    # Login or load session
    L.login(usrname, passwrd)        # (login)

    # Obtain profile metadata
    profile = instaloader.Profile.from_username(L.context, acc)

    

    for i , followee in enumerate(profile.get_followers()):
        username = followee.username
        usrs.append(username)
        #print(username)
        if i > 50 :
            break

    print (f"Got {len(usrs)} followers ")
    return usrs





def sign_insta(acc):
    '''
    sign in to instagram 
    '''
    usrs.append(acc)


    gmail_reg = r"[A-Za-z0-9.]{1,}@gmail.com"

    outlook_reg = r"[A-Za-z0-9.]{1,}@outlook.com"



    browser = webdriver.Firefox(options=options)
    browser.get("https://www.instagram.com/")


    while True:
        try:

            usr_ = browser.find_element_by_css_selector("div.-MzZI:nth-child(1) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)")
            passwrd_ = browser.find_element_by_css_selector("div.-MzZI:nth-child(2) > div:nth-child(1) > label:nth-child(1) > input:nth-child(2)")
            
            usr_.send_keys(usrname)    
            passwrd_.send_keys(passwrd)
            passwrd_.send_keys(Keys.ENTER)

            break 

        except:
            time.sleep(1)


 



    while  True :
        try:
            save_info = browser.find_element_by_css_selector("html.js.logged-in.client-root.js-focus-visible.sDN5V body div#react-root section._9eogI.E3X2T main.SCxLW.o64aR div.Igw0E.rBNOH.YBx95.vwCYk div.pV7Qt.DPiy6.Igw0E.IwRSH.eGOV_._4EzTm.qhGB0.ZUqME div.Igw0E.IwRSH.eGOV_._4EzTm.MGdpg.aGBdT section.ABCxa div.JErX0 button.sqdOP.L3NKy.y3zKF")
            save_info.click()
            break
        except:

            time.sleep(5)

 



    while  True:
        try:
            notifications = browser.find_element_by_css_selector("html.js.logged-in.client-root.js-focus-visible.sDN5V body div.RnEpo.Yx5HN div.pbNvD.fPMEg div._1XyCr div.piCib div.mt3GC button.aOOlW.bIiDR")
            notifications.click()
            break
        except:
            time.sleep(5)
        

    ## grab all the followers names them check every one for emails 
    ## append evey email to a list to send to mail server 


    
    pyautogui.click(682, 195)

    for item in get_followers(acc):
        time.sleep(3)

        browser.get(f"https://www.instagram.com/{item}")
        output_ = browser.page_source

        tmp = re.findall(gmail_reg , output_) + re.findall(outlook_reg , output_)

        tmp = list(dict.fromkeys(tmp))

        print (f"Found {len(tmp)} emails  @ user {item} ")
        for item in tmp:
            all_mails_found.append(item)
            send_mail(mail=item)


    time.sleep(1)
    browser.quit()



#sign_insta(acc="m.a.m.a.s.i.t.a")

sign_insta(acc="jokezar")


for item in usrs:
    time.sleep(120)
    sign_insta(acc=item)


for item in all_mails_found:
    print (item)

print (f"Total found emails {len(all_mails_found)}")
