from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select


class DriverManager():

    def __init__(self, base_url: str, hidden_browser_option: bool = False):
        """
        브라우저 드라이버 생성
        셀레니움 드라이버를 래핑하 특정 기능만 활성화 및 커스텀
        현재 크롬만 지원

        Args:
            base_url (str): 초기 URL 
            hidden_browser_option (bool, optional): 브라우저 숨기기 옵션
        """
        driver_option = webdriver.ChromeOptions()
        driver_option.add_experimental_option(
            'excludeSwitches', ['enable-logging'])
        # 창 숨기는 옵션
        if hidden_browser_option:
            driver_option.add_argument("headless")
        self.driver = webdriver.Chrome(options=driver_option)
        self.driver.get(base_url)

    def move_to(self, url: str, wait_time: int = 3):
        """
        특정 사이트로 이동

        Args:
            url (str): 이동할 URL
            wait_time (int): Defaults to 3.
        """
        self.driver.get(url)
        self.driver.implicitly_wait(wait_time)
        
    def find_element_by_id(self, id: str):
        """
        특정 id를 가진 html 요소 반환

        Args:
            id (str): 찾고자 하는 태그 id
        """
        return self.driver.find_element(By.ID, id)
    
    def find_element_by_class(self, class_name: str) -> WebElement:
        """
        특정 class를 가진 html 요소 반환

        Args:
            class_name (str): 찾고자 하는 클래스 이름
        """
        return self.driver.find_element(By.CLASS_NAME, class_name)
    
    def find_elements_by_class(self, class_name: str) -> list[WebElement]:
        """
        특정 class를 가진 html 요소들 반환

        Args:
            class_name (str): 찾고자 하는 클래스 이름
        """
        return self.driver.find_elements(By.CLASS_NAME, class_name)
    
    def find_select_element_by_id(self, id: str) -> Select:
        """
        웹 선택형 UI를 제어하기 위해 Select 객체로 반환  

        Args:
            id (str): 찾고자 하는 태그 id

        Returns:
            Select: 드롭박스 (선택자) 객체 반환
        """
        return Select(self.find_element_by_id(id))
    
    def close(self):
        """ 브라우저 닫기 """
        self.driver.close()
        
    def switch_to_tab(self, index: int):
        """
        브라우저 탭 전환

        Args:
            index (int): 이동할 탭 번호 (첫 번째 탭: 0) 
        """
        self.driver.switch_to.window(self.driver.window_handles[index])
        
    def make_new_tab(self, url: str = 'www.google.com'):
        """
        브라우저 탭 생성
        
        Args: 
            url (str): 생성된 브라우저 초기 url
        """
        self.driver.execute_script(f'window.open({url});')
    
    
    
    @property
    def page_source(self) -> str:
        """ html 반환 """
        return self.driver.page_source

    @property
    def url(self) -> str:
        """ 현재 url 반환 """
        return self.driver.current_url