import time
import requests
import re

class CaptchaAPI:
    def __init__(self, api_key, sleep=5, timeout=120):
        self.api_key = api_key
        self.sleep = sleep
        self.timeout = timeout
        self.url = 'http://2captcha.com/in.php'

    def solve_recaptcha(self, **kwargs):
        captcha_id = self.get_recaptcha_id(**kwargs)

        start_time = time.time()
        waiting = 0
        while time.time() < start_time + self.timeout:
            from_time = time.time()

            answer_token = self.get_answer_token(captcha_id)
            if 'CAPCHA_NOT_READY' in answer_token:
                print('resp(%ds): %s' % (waiting, answer_token))
                time.sleep(self.sleep)
                waiting += (time.time() - from_time)
            else:
                print('resp(%ds): %s' % (waiting, answer_token))
                return answer_token

    def solve_hcaptcha(self, **kwargs):
        captcha_id = self.get_hcaptcha_id(**kwargs)

        start_time = time.time()
        waiting = 0
        while time.time() < start_time + self.timeout:
            from_time = time.time()

            answer_token = self.get_answer_token(captcha_id)
            if 'CAPCHA_NOT_READY' in answer_token:
                print('resp(%ds): %s' % (waiting, answer_token))
                time.sleep(self.sleep)
                waiting += (time.time() - from_time)
            else:
                print('resp(%ds): %s' % (waiting, answer_token))
                return answer_token

    def get_recaptcha_id(self, **kwargs):
        payload = {
            'key': self.api_key,
            'method': 'userrecaptcha',
            'googlekey': kwargs['data_sitekey'],
            'pageurl': kwargs['pageurl']
        }
        proxy = kwargs.get('proxy', '')
        if proxy:
            payload['proxy'] = proxy
        print(payload)

        response = requests.post(self.url, data=payload, timeout=20)
        response_text = re.sub(r'^OK\|', '', response.text)
        return response_text

    def get_hcaptcha_id(self, **kwargs):
        payload = {
            'key': self.api_key,
            'method': 'hcaptcha',
            'sitekey': kwargs['data_sitekey'],
            'pageurl': kwargs['pageurl'],
        }
        proxy = kwargs.get('proxy', '')
        if proxy:
            payload['proxy'] = proxy
        print(payload)

        response = requests.post(self.url, data=payload, timeout=20)
        response_text = re.sub(r'^OK\|', '', response.text)
        return response_text

    def get_answer_token(self, captcha_id):
        get_url = 'https://2captcha.com/res.php?key=%s&action=get&id=%s' % (self.api_key, captcha_id)
        response = requests.get(get_url, timeout=20)
        response_text = re.sub(r'^OK\|', '', response.text)
        return response_text

    def demo_recaptcha(self):
        # API_KEY = '***'
        # captcha = CaptchaAPI(API_KEY)

        """
        data_sitekey = drive_attribute(driver, '//*[@data-sitekey]', 'data-sitekey', 20)
        textarea = drive_find(driver, '//*[@id="g-recaptcha-response"]', 20)

        captcha_response = captcha.solve_recaptcha(**{'data_sitekey': data_sitekey, 'pageurl': url})
        if captcha_response is None:
            print('[!]captcha_response(None): retries...')
            if driver:
                driver.quit()
            retries += 1
            continue

        driver.execute_script("arguments[0].style.display = 'block';", textarea)
        textarea.send_keys(captcha_response)
        driver.execute_script("arguments[0].style.display = 'none';", textarea)

        drive_click(driver, '//form[@id="bot-check"]//button[@type="submit"]')
        sleep(3, 'submit captcha....')
        """

        """
        data_sitekey = drive_attribute(driver, '//*[@data-sitekey]', 'data-sitekey', 20)
        g_textarea = drive_find(driver, '//*[@name="g-recaptcha-response"]', 20)
        h_textarea = drive_find(driver, '//*[@name="h-captcha-response"]', 20)

        captcha_response = captcha.solve_hcaptcha(**{'data_sitekey': data_sitekey, 'pageurl': url})
        if captcha_response is None:
            print('[!]captcha_response(None): retries...')
            driver.quit()
            retries += 1
            continue

        driver.execute_script("arguments[0].style.display = 'block';", g_textarea)
        g_textarea.send_keys(captcha_response)
        sleep(9, 'g_textarea  display=block...')
        driver.execute_script("arguments[0].style.display = 'none';", g_textarea)
        sleep(9, 'g_textarea  display=none...')

        driver.execute_script("arguments[0].style.display = 'block';", h_textarea)
        h_textarea.send_keys(captcha_response)
        sleep(9, 'h_textarea  display=block...')
        driver.execute_script("arguments[0].style.display = 'none';", h_textarea)
        sleep(9, 'h_textarea display=none...')
        
        drive_click(driver, '//*[@id="hcaptcha_submit"]')
        sleep(5, 'submit captcha....')
        """

if __name__=="__main__":
    print('Testing ...')
    API_KEY = '***'
    captcha = CaptchaAPI(API_KEY)

