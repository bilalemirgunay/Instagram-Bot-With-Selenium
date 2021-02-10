from instagramUserInfo import username, password
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

class Instagram:
    def __init__(self, username, password):
        self.driverProfile = webdriver.ChromeOptions()
        self.driverProfile.add_experimental_option('prefs', {'intl.accept_languages':'en,en_US'})
        self.driver = webdriver.Chrome('chromedriver.exe', chrome_options=self.driverProfile)
        self.username = username
        self.password = password
        self.followerList = list()
        self.followsList = list()
        self.unfollowersList = list()

    def signIn(self):
        self.driver.get("https://www.instagram.com/")
        time.sleep(2)
        unameInput = self.driver.find_element_by_xpath("//*[@id='loginForm']/div/div[1]/div/label/input")
        pwInput = self.driver.find_element_by_xpath("//*[@id='loginForm']/div/div[2]/div/label/input")
        button = self.driver.find_element_by_xpath("//*[@id='loginForm']/div/div[3]/button")

        unameInput.send_keys(self.username)
        pwInput.send_keys(self.password)
        button.click()
        time.sleep(5)

    def getFollowers(self):
        self.driver.get(f"https://www.instagram.com/{self.username}")
        time.sleep(2)
        followersBtn = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a")
        followersCount = int(followersBtn.find_element_by_tag_name("span").text) 

        followersBtn.click()
        time.sleep(3)

  
        dialog = self.driver.find_element_by_css_selector("div[role=dialog] ul")

        action = webdriver.ActionChains(self.driver)


        while True:
            dialog.click()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(2)


            newCount = len(dialog.find_elements_by_css_selector("li"))

            if  newCount+1 >= followersCount:
                break




        followers = dialog.find_elements_by_css_selector("li")
        print(f"Number of followers: {len(followers)}")

        for user in followers:
            userLink = user.find_element_by_tag_name("a").get_attribute("href")
            self.followerList.append(userLink)

        with open("followers.txt", "w", encoding="utf-8") as file:
            for follower in self.followerList:
                file.write(follower + "\n")

    def followUsers(self, usernameList):

        for username in usernameList:
            self.driver.get(f"https://www.instagram.com/{username}")
            time.sleep(3)

            followButton = self.driver.find_element_by_tag_name("button")

            if(followButton.text == "Follow" or followButton.text == "Follow Back"):
                followButton.click()
                time.sleep(3)

    def unfollowUsers(self, usernameList):

        for username in usernameList:
            self.driver.get(f"https://www.instagram.com/{username}")
            time.sleep(5)
            try:
                self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/div[1]/div[1]/div/div[2]/div/span/span[1]/button").click()
                time.sleep(3)
                self.driver.find_element_by_xpath("//button[text()='Unfollow']").click()
            except:
                print("Error!")

    def getFollows(self):

        self.driver.get(f"https://www.instagram.com/{self.username}")
        time.sleep(3)
        followsBtn = self.driver.find_element_by_xpath("//*[@id='react-root']/section/main/div/header/section/ul/li[3]/a")
        followsCount = int(followsBtn.find_element_by_tag_name("span").text)

        followsBtn.click()
        time.sleep(4)

        dialog = self.driver.find_element_by_css_selector("div[role=dialog] ul")

        action = webdriver.ActionChains(self.driver)


        while True:
            dialog.click()
            action.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            time.sleep(5)


            newCount = len(dialog.find_elements_by_css_selector("li"))
            if  newCount+1 >= followsCount:
                break




        follows = dialog.find_elements_by_css_selector("li")
        print(f"Number of follows: {len(follows)}")

        for user in follows:
            userLink = user.find_element_by_tag_name("a").get_attribute("href")
            self.followsList.append(userLink)

        with open("follows.txt", "w", encoding="utf-8") as file:
            for followed in self.followsList:
                file.write(followed + "\n")

    def getUnfollowersFromFiles(self):
        with open("followers.txt", "r", encoding="utf-8") as file:
            followers = file.readlines()
        with open("follows.txt", "r", encoding="utf-8") as file:
            follows = file.readlines()
        print(f"followers:{len(followers)}\nfollows:{len(follows)}")

        for followUser in follows:
            if(not(followUser in followers)):
                followUser = followUser.strip("\n")
                self.unfollowersList.append(followUser)

        with open("unfollowers.txt", "w", encoding="utf-8") as file:
            for unfUser in self.unfollowersList:
                file.write(unfUser + "\n")
          

instagram = Instagram(username, password)
instagram.signIn()
# instagram.getFollowers()
# instagram.getFollows()
# instagram.getUnfollowersFromFiles()
# instagram.followUsers(["ofiningilizce","bilalemirgunay"])
# instagram.unfollowUsers(["ofiningilizce","bilalemirgunay"])
time.sleep(5)
instagram.driver.close()

