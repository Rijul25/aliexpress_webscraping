import datetime
import time

from selenium import webdriver
import pandas as pd

from aliexpressproject.temp import fun1, get_feedbacks

browser = webdriver.Chrome(executable_path="/home/nimish/PycharmProjects/so/internship/macroproject/chromedriver")
browser1 = webdriver.Chrome(executable_path="/home/nimish/PycharmProjects/so/internship/macroproject/chromedriver")

browser1.get(
    "https://www.aliexpress.com/category/100003109/women-clothing-accessories.html?spm=2114.11010108.101.1.4343649bn2JbUY")

# browser.get("https://www.aliexpress.com/store/product/Aproms-Elegant-Gray-TurtLeneck-Irregular-Blouse-Womens-3-4-Sleeve-Casual-90s-Loose-Top-Street-Fashion/116172_32834586866.html?spm=2114.search0103.3.1.7b3d3d37WIJoiv&ws_ab_test=searchweb0_0,searchweb201602_1_10065_10068_10546_10059_10884_5726811_10548_10887_10696_100031_10084_10083_10103_10618_5726911_10307_449,searchweb201603_60,ppcSwitch_0&algo_expid=ecfb49ba-e3a2-4606-8fde-4a653908068a-0&algo_pvid=ecfb49ba-e3a2-4606-8fde-4a653908068a&priceBeautifyAB=0")

# q=browser.find_elements_by_css_selector(".son-list")[0]
listi=[]
ctr=0

for pages in range(1,3):
    products = browser1.find_elements_by_css_selector(".product")
    for product in products:
        url = product.get_attribute("href")
        row_dicti={}
        row_dicti["url"] = url
        browser.get(url)
        try:
            name = browser.find_elements_by_css_selector(".product-name")[0].text
            row_dicti["name"] = name
        except Exception as E:
            print(E)

        try:
            available = browser.find_elements_by_css_selector("#j-sell-stock-num")[0].text
            row_dicti["available"] = available
        except Exception as E:
            print(E)

        try:
            price = browser.find_element_by_css_selector(".p-price-content").text
        except Exception as E:
            print(E)

        item_specifications = {}

        try:
            ppl = browser.find_elements_by_css_selector(".product-property-list")
            lis = ppl[0].find_elements_by_css_selector("li")

            for k in lis:
                item_specifications[k.find_element_by_css_selector(".propery-title").text] = k.find_element_by_css_selector(
                    ".propery-des").text

            row_dicti["item-specs"] = str(item_specifications)

        except Exception as E:
            print(E)

        try:
            product_description = browser.execute_script('return document.querySelector(".description-content").innerHTML')
            row_dicti["product_description"] = product_description.replace("\n"," ")
        except Exception as E:
            print(E)

        try:
            store_name = browser.find_element_by_css_selector(".shop-name").text.replace("\n", " ").replace("Store:", "")
            row_dicti["store_name"] = store_name
        except Exception as E:
            print(E)

        images = []

        # try:
        #     image_li = browser.find_element_by_css_selector("#j-image-thumb-list").find_elements_by_css_selector("li")
        #     for j in image_li:
        #         j.click()
        #         images.append(browser.find_elements_by_css_selector(".ui-image-viewer-thumb-frame")[0].find_element_by_css_selector(
        #             "img").get_attribute("src"))
        #
        #     row_dicti["image_urls"] = str(images)
        # except Exception as E:
        #     print(E)

        # try:
        #     normal_price = browser.find_element_by_css_selector(".p-del-price-content").text
        #     row_dicti["normal_price"] = normal_price
        # except Exception as E:
        #     print(E)
        #
        # try:
        #     current_price = browser.find_element_by_css_selector(".p-price-content").text
        #     row_dicti["current_price"] = current_price
        # except Exception as E:
        #     print(E)

        # image_list=[]
        # for image in image_li:
        #     image_list.append(image.find_element_by_css_selector("img").get_attribute("src"))
        # color_element = None
        # size_element = None
        #
        # try:
        #     for j in browser.find_elements_by_css_selector(".p-property-item"):
        #         if "Color" in j.text:
        #             color_element = j
        #         if "Size" in j.text:
        #             size_element = j
        #
        # except Exception as E:
        #     print(E)

        # browser.find_element_by_css_selector("#j-sku-list-1").find_element_by_xpath("..")

        # colors = []
        # sizes = []
        #
        # if color_element:
        #     color_list = color_element.find_elements_by_css_selector("li a")
        #     for color in color_list:
        #         colors.append(color.get_attribute("title"))
        #
        #     row_dicti["colors"] = str(colors)
        #
        # if size_element:
        #     size_list = size_element.find_elements_by_css_selector("span")
        #     for size in size_list:
        #         sizes.append(size.text)
        #
        #     row_dicti["sizes"] = str(sizes)
        #

        try:
            all_items_of_product = []
            all_elems = browser.find_elements_by_css_selector(".sku-attr-list")
            all_items_of_product = fun1(browser,1, 0, 0.01, {}, all_items_of_product, all_elems)
            row_dicti["main_data"] = all_items_of_product
        except Exception as E:
            print(E)

        try:
            feedbacks = get_feedbacks(browser)
            row_dicti["feedbacks"] = feedbacks
        except Exception as E:
            print(E,"while feedback")



        try:
            for elem in browser.find_element_by_css_selector(".ui-switchable-nav").find_elements_by_css_selector("li"):
                if "Shipping" in elem.text:
                    break

            elem.click()
            time.sleep(1)
            table = browser.find_element_by_css_selector(".shipping-table-wrap").find_element_by_tag_name("table").get_attribute(
            "outerHTML")
            shipping_data = pd.read_html(table)[0]
            row_dicti["shipping"] = shipping_data.to_json()

        except Exception as E:
            print(E)

        try:
            star_rating = browser.find_element_by_css_selector(".percent-num").text
            row_dicti["star_rating"] = star_rating
        except:
            pass

        try:
            out_of = browser.find_element_by_css_selector(".rantings-num").text
            row_dicti["out_of"] = out_of
        except:
            pass

        listi.append(row_dicti)
        print("product no",ctr)
        ctr+=1
    # browser.find_element_by_css_selector(".ui-pagination-next")
    try:
        browser1.find_element_by_css_selector(".ui-pagination-next").click()
    except Exception as E:
        print("error frmo ",pages)
        pass

pd.DataFrame(listi).to_excel("/home/nimish/PycharmProjects/so/internship/aliexpressproject/"+str(datetime.datetime.now().isoformat())+".xlsx")