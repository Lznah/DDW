import re
from classes.page import Page
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

class BranchesPage(Page):
    def __init__(self, url):
        Page.__init__(self, url)
        self.id = re.search('\/([0-9]*)\/pobocky',url).group(1)
        

    def scrape(self):
        try:
            company = Page._companies[str(self.id)]
            if self.isNot404():
                branches = self._driver.find_elements_by_css_selector(".texts")
                for branch in branches:
                    title = branch.find_element_by_css_selector("a.link.ng-binding")
                    name = title.text
                    #link = title.get_attribute("href")
                    address = branch.find_element_by_css_selector(".address.ng-binding").text
                    estates_count = int(branch.find_element_by_css_selector(".estates-cnt.ng-binding .num").text.replace(' ', ''))
                    company['branches'].append({
                        "name": name,
                        "address": address,
                        "estates_count": estates_count,
                        "agents": []
                    })
                    
                if not re.match(".*strana=[0-9]*", self._url):
                    pagination_elements = Page._driver.find_elements_by_css_selector(".numero.ng-binding")
                    if len(pagination_elements) > 0:
                        delimiter = int(pagination_elements[0].text.split('–')[1])
                        total = int(pagination_elements[1].text.replace(" ", ""))
                        num_pages = int(total/delimiter)+1
                        
                        for p in range(2,num_pages+1):
                            Page._stack.append(BranchesPage(self._url+"?strana="+str(p)))

                    menu_text = Page._driver.find_element_by_css_selector(".switcher-group.agency-switcher").text
                    menu_estate_count = re.search("Inzeráty \(([0-9]*)\)", menu_text)
                    if menu_estate_count != None:
                        company['branches'].append({
                            "name": company["name"],
                            "estate_count": int(menu_estate_count.group(1)),
                            #"agents": []
                        })
                    #stack.append(AgentsPage(link+"/makleri"))
            else:
                company['branches'].append({
                    "name": company["name"],
                    "address": company["address"],
                    "estates_count": company["estates_count"],
                    #"agents" : []
                })
        
        except NoSuchElementException:
            print("Element not found!")
        except TimeoutException:
            print("Loading took too much time!")
