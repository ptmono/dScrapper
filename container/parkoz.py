from baseTemplates import InfoBaseTemplateA

from lxml.cssselect import CSSSelector
#from lxml.html import fromstring, tostring


class ParkozImageContainer(InfoBaseTemplateA):
    url_format = 'http://www.parkoz.com/zboard/zboard.php?id=images2&page=%s'
    base_url = 'http://www.parkoz.com/zboard/'
    base_selector = 'tr.TRBG'
    number_selector = "td.thm8 font"
    title_selector = "td.thm9 a"
    url_selector = "td.thm9 a"

    def getTitles(self):
        result = []
        for element in self.elements:
            sel = CSSSelector(self.title_selector)
            sel_list = sel(element)
            #print tostring(sel_list[0], encoding='utf-8')
            aa = sel_list[0].text_content()
            print aa
            # text_content will returns only text part
            result.append(sel_list[0].text_content())
        return result
