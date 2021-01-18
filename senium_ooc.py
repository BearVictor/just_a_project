from responses import MyBrowser
from modules import *
import proxies as Proxies
import scraper_ooc as scraper
import deed_values
import deed_points
import regex_legal
import config as Config
import two_captcha

captcha = two_captcha.CaptchaAPI('a011a2e8a800726c0e565109a144169d')
proxies = Proxies.proxies
my_browser = MyBrowser(proxies=proxies)

parent_dir = Config.parent_dir

except_dir = Config.except_dir
except_values_dir = Config.except_values_dir
except_points_dir = Config.except_points_dir

download_dir = Config.download_dir + '_marriot'  # todo: download_marriot

cache_dir = Config.cache_dir
session_dir = Config.session_dir

stored_listings = 'stored/stored_listings'
stored_d_2grantees = 'stored/stored_d_2grantees'
stored_d_clean_legals = 'stored/stored_d_clean_legals'
stored_d_clean_names = 'stored/stored_d_clean_names'
stored_d_values = 'stored/stored_d_values'
stored_details = 'stored/stored_details'

stored_d_docs = 'stored/stored_d_docs'

excepted_values = 'stored/excepted_values'

def scrape_cache_listings(inp, *, stop=9, timeout=45, cache=True, headless=True):
    url = inp.strip() if isinstance(inp, str) else inp['url'].strip()
    start_date = inp['start_date'].strip()
    end_date = inp['end_date'].strip()
    search_by = inp['search_by'].strip()
    lname_fname = inp['lname_fname'].strip()
    cache_name = ''.join([start_date, end_date, lname_fname])
    retries = 0
    while retries < stop:
        if retries > 0:
            message('[!] %s(retrieve - %s)' % (inspect.stack()[0][3], retries), cache_name)

        driver = my_browser.chrome(url, headless=headless, timeout=timeout, session_dir=session_dir)
        if driver is None:
            return
        try:
            driver_title = drive_str(driver, '//*[contains(text(), "Comptroller Home")]')
            if driver_title:
                message('[+] %s(driver_title)' % inspect.stack()[0][3], driver_title)

                # todo: actions on browser

                def search_form(driver):
                    # """
                    try:
                        drive_click(driver, '//input[@value="I Acknowledge"]')
                        sleep(1, 'click "I Acknowledge" ...')
                    except:
                        pass

                    drive_find(driver, '//input[@id="RecordingDateIDStart"]').send_keys(start_date)
                    drive_find(driver, '//input[@id="RecordingDateIDEnd"]').send_keys(end_date)

                    # todo: lname_fname
                    drive_find(driver, f'//input[@id="{search_by}IDSearchString"]').send_keys(lname_fname)

                    # todo: Search Type
                    drive_click(driver, f'//select[@id="{search_by}IDSearchType"]/option[@value="{inp["search_type"]}"]')

                    drive_click(driver, '//input[@id="allTypesCB"]')

                    # todo: Select doc type(s)
                    drive_click(driver, f'//select[@name="__search_select"]/option[text()="{inp["doc_type"]}"]')

                    legal = inp['legal']
                    if legal:
                        drive_click(driver, '//li/a[text()="Advanced"]')
                        drive_find(driver, '//input[@id="LegalRemarks"]').send_keys(legal)

                    drive_click(driver, '//input[@value="Search"]')
                    sleep(1, 'Search ...')

                    previous_page = None
                    while True:
                        try:
                            active_page_xpath = '(//span[@class="pagelinks"])[1]/strong'
                            next_page_xpath = '(//span[@class="pagelinks"])[1]/strong/following-sibling::a[1]'

                            active_page = drive_str(driver, active_page_xpath)
                            if active_page != previous_page:
                                previous_page = active_page
                                if cache:
                                    write_cache('%s%s' % (cache_name, active_page), driver.page_source.replace('&nbsp;', ' '), directory=cache_dir)
                            else:
                                sleep(3, '%s (page %s) | ERROR active_page == previous_page...' % (
                                    cache_name, active_page))

                                active_page = drive_str(driver, active_page_xpath)
                                if active_page != previous_page:
                                    previous_page = active_page
                                    if cache:
                                        write_cache('%s%s' % (cache_name, active_page), driver.page_source.replace('&nbsp;', ' '), directory=cache_dir)
                                else:
                                    driver.quit()
                                    return

                            sleep(0, 'active_page is %s...' % active_page)
                            try:
                                drive_click(driver, next_page_xpath)
                                sleep(1, 'click next page %s...')
                            except:
                                break
                        except:
                            break

                search_form(driver)

                listing = drive_finds(driver, '//table[@id="searchResultsTable"]/tbody/tr')
                sleep(1, 'len %s' % len(listing))

                parser_text = driver.page_source.replace('&nbsp;', ' ')
                if cache:
                    write_cache(cache_name, parser_text, directory=cache_dir)
            driver.quit()
        except:
            trace_msg = traceback.format_exc().strip()
            error = '[*] %s\n  [+] Cache name "%s"' % (trace_msg, cache_name)
            print(error)

            if 'KeyboardInterrupt' not in trace_msg:
                exception_path = '/'.join([except_dir, hash_name(trace_msg)])
                driver.save_screenshot(exception_path + '.png')
                write_txt(error, exception_path, alert=False)

            driver.quit()
            retries += 1
            continue
        # todo: break while
        break

def cache_docs(inp, *, stop=9, timeout=45, headless=True):
    url = inp.get('url', '') if isinstance(inp, dict) else inp
    url = url.strip()
    for retries in range(stop):
        raw_caches = inp['caches'] if isinstance(inp, dict) else []
        caches = []
        for cache in raw_caches:
            if os.path.exists('%s/%s.txt' % (cache_dir, hash_name(cache))):
                print('"%s" existed....' % cache)
                continue
            caches.append(cache)
        if not caches:
            return

        if retries > 0:
            message('[!] %s(retrieve - %s)' % (inspect.stack()[0][3], retries), url)

        proxies = Proxies.proxies
        browser = MyBrowser(proxies=proxies)

        if 'nnd2890' in os.getcwd():
            driver = browser.chrome(url, headless=headless, timeout=timeout)
        else:
            driver = browser.phantomjs(url, timeout=timeout)

        if driver is None:
            return

        try:
            driver_title = drive_str(driver, '//*[contains(text(), "Comptroller Home")]')
            if not driver_title:
                sleep(0, 'not driver_title ....')
                driver.quit()
                continue

            message('[+] %s(driver_title)' % inspect.stack()[0][3], driver_title)
            drive_click(driver, '//input[@value="I Acknowledge"]')
            sleep(1, 'click "I Acknowledge" ...')

            previous = None
            driver_is_error = False
            caches_len = len(caches)
            for cache_index, cache in enumerate(caches):
                if os.path.exists('%s/%s.txt' % (cache_dir, hash_name(cache))):
                    print('"%s" existed....' % cache)
                    continue
                try:
                    drive_find(driver, '//input[@id="DocumentID"]').clear()
                except:
                    data_sitekey = drive_attribute(driver, '//*[@data-sitekey]', 'data-sitekey', 20)
                    sleep(9, f'captcha data_sitekey "{data_sitekey} "...')

                    driver.quit()
                    driver_is_error = True
                    break

                    # data_sitekey = drive_attribute(driver, '//*[@data-sitekey]', 'data-sitekey', 20)
                    # textarea = drive_find(driver, '//*[@id="g-recaptcha-response"]', 20)
                    #
                    # captcha_response = captcha.solve_recaptcha(**{'data_sitekey': data_sitekey, 'pageurl': url})
                    # if captcha_response is None:
                    #     print('[!]captcha_response(None): retries...')
                    #     if driver:
                    #         driver.quit()
                    #         return
                    #
                    # driver.execute_script("arguments[0].style.display = 'block';", textarea)
                    # textarea.send_keys(captcha_response)
                    # driver.execute_script("arguments[0].style.display = 'none';", textarea)
                    #
                    # drive_click(driver, '//input[@value="Submit"]')
                    # sleep(3, 'submit captcha....')
                    #
                    # # todo: clear DocumentID input again
                    # drive_find(driver, '//input[@id="DocumentID"]').clear()

                drive_find(driver, '//input[@id="DocumentID"]').send_keys(cache)

                drive_click(driver, '//input[@value="Search"]')
                sleep(1, 'Search ...')

                found = drive_str(driver, '//p[@style="clear: both;"]')
                if found == previous:
                    sleep(0, 'ERROR found == previous (%s | %s)....' % (found, previous))
                    driver_is_error = True
                    break
                previous = found
                sleep(random.choice([5,6,7,8,9,10,11,12,13,14,15]), found)

                parser_text = driver.page_source.replace('&nbsp;', ' ')
                write_cache(cache, parser_text, directory=cache_dir)
                sleep(0, 'save cache (%s) len (%s | %s)...' % (cache, caches_len, cache_index))

                last_idex = caches_len - 1
                if cache_index < last_idex:
                    drive_click(driver, '(//a[@class="iconic modifySearch"])[1]')
                    sleep(1, 'click modifySearch ...')

            if driver_is_error:
                driver.quit()
                continue
        except:
            trace_msg = traceback.format_exc().strip()
            error = '[*] %s\n  [+] Cache name "%s"' % (trace_msg, url)
            print(error)

            if 'KeyboardInterrupt' not in trace_msg:
                exception_path = '/'.join([except_dir, hash_name(trace_msg)])
                driver.save_screenshot(exception_path + '.png')
                write_txt(error, exception_path, alert=False)

            driver.quit()
            continue

        driver.quit()
        break  # todo: if not error, break the loop

def dowload2(inp, *, timeout=45, headless=True):
    my_browser = MyBrowser(proxies=[inp['ip']])
    for pdf in inp['pdfs']:
        fname = os.path.join(download_dir, pdf['fname'])
        print(fname)

        if os.path.isfile(fname):
            print('%s existed' % fname)
            continue

        url = pdf.strip() if isinstance(pdf, str) else pdf['url'].strip()
        driver = my_browser.chrome_dowload_PDFViewer(url, headless=headless, timeout=timeout, session_dir=session_dir, download_dir=download_dir)
        sleep(3, 'downloading...')

        if os.path.isfile(fname):
            sleep(3, f'downloaded ({fname})...')

        if driver is None:
            return

        driver.quit()

def download_pdfs(inp, *, stop=9, timeout=45, headless=True, download_dir=None):
    url = inp.get('url', '') if isinstance(inp, dict) else inp
    url = url.strip()
    for retries in range(stop):
        fname = os.path.join(download_dir, inp['fname'])
        if os.path.isfile(fname):
            print('%s existed' % fname)
            return

        if retries > 0:
            message('[!] %s(retrieve - %s)' % (inspect.stack()[0][3], retries), url)

        proxies = Proxies.proxies
        browser = MyBrowser(proxies=proxies)

        driver = browser.firefox_pdf(url, headless=headless, timeout=timeout, download_dir=download_dir)

        if driver is None:
            return

        try:
            driver_title = drive_str(driver, '//*[contains(text(), "Comptroller Home")]')
            if not driver_title:
                sleep(0, 'not driver_title ....')
                driver.quit()
                continue

            message('[+] %s(driver_title)' % inspect.stack()[0][3], driver_title)

            drive_click(driver, '//input[@value="I Acknowledge"]')
            sleep(3, 'click "I Acknowledge" ...')

            if os.path.isfile(fname):
                sleep(random.choice([3,4,5,6,7]), f'downloaded ({fname})...')
            else:
                trace_msg = 'not dowloaded'
                error = '[*] %s\n  [+] Cache name "%s"' % (trace_msg, url)
                print(error)

                exception_path = '/'.join([except_dir, hash_name(trace_msg)])
                driver.save_screenshot(exception_path + '.png')
                write_txt(error, exception_path, alert=False)
                driver.quit()
                continue
        except:
            trace_msg = traceback.format_exc().strip()
            error = '[*] %s\n  [+] Cache name "%s"' % (trace_msg, url)
            print(error)

            if 'KeyboardInterrupt' not in trace_msg:
                exception_path = '/'.join([except_dir, hash_name(trace_msg)])
                driver.save_screenshot(exception_path + '.png')
                write_txt(error, exception_path, alert=False)

            driver.quit()
            continue

        driver.quit()
        break  # todo: if not error, break the loop


def pool_store_data(data, *, func, stored_file, threads):
    sleep(1, '\n[*] %s(len): %s' % (inspect.stack()[0][3], len(data)))
    if stored_file:
        write_txt('', stored_file)
    pool(func, data, threads)

def store_listings(pdata):
    output = scraper.scrape_listings(pdata, cache_read=True)
    if output:
        append_txt(json.dumps(output), stored_listings)

def store_d_docs(pdata):
    output = scraper.scrape_d_docs(pdata, cache_read=True)
    if output:
        append_txt(json.dumps(output), stored_d_docs)
    else:
        business_details = copy_dict(pdata, [])
        business_details.update({
            'description_mortgage': '',
            'rec_date_mortgage': '',
            'legal_mortgage': '',
            'grantor_mortgage': '',
            'grantee_mortgage': '',
            'pdf_name_mortgage': '',
            'pdf_url_mortgage': '',
            'parent_url_mortgage': '',
            'mortgages_total': '',
        })
        append_txt(json.dumps(business_details), stored_d_docs)

def store_dowload_pdfs(inp):
    download_pdfs(inp, download_dir=download_dir, headless=True)

def store_txts(row):
    fname = row['pdf_name']
    pdf_fname = download_dir + '/' + fname
    txt_fname = re.sub(r'\.pdf$', '.txt', pdf_fname)
    if not os.path.isfile(txt_fname):
        try:
            write_txt(extract_scanded_pdf(pdf_fname, deed_values.value_regexs), txt_fname)
        except:
            trace_msg = traceback.format_exc().strip()
            if 'KeyboardInterrupt' not in trace_msg:
                print(trace_msg)
                print(row)
                delete_file(pdf_fname)
                sleep(3)
            pass
    else:
        print('%s existed....' % txt_fname)

def store_txts_MARRIOT(row):
    fname = row['pdf_name_mortgage']
    pdf_fname = download_dir + '/' + fname
    txt_fname = re.sub(r'\.pdf$', '.txt', pdf_fname)
    if not os.path.isfile(txt_fname):
        try:
            write_txt(extract_scanded_pdf(pdf_fname, deed_values.value_regexs), txt_fname)
        except:
            trace_msg = traceback.format_exc().strip()
            if 'KeyboardInterrupt' not in trace_msg:
                print(trace_msg)
                print(row)
                delete_file(pdf_fname)
                sleep(3)
            pass
    else:
        print('%s existed....' % txt_fname)

def do_cache_listings(search_input):
    scrape_cache_listings(search_input, headless=True)

def do_listings(threads, search_input, start, stop):
    start_date = search_input['start_date']
    end_date = search_input['end_date']
    lname_fname = search_input['lname_fname']
    data = []

    for i in range(start, stop):
        page = i
        adding = copy_dict(search_input)
        adding['page'] = page
        adding['url'] = '%s%s%s%s' % (start_date, end_date, lname_fname, page)
        data.append(adding)
    pool_store_data(data, func=store_listings, stored_file=stored_listings, threads=threads)

    # todo: filter 2 grantees
    listing = list_txt(stored_listings)
    write_txt('', stored_d_2grantees)
    for row in listing:
        row.pop('parent_url')

        grantee = row['grantee']
        grantee = re.sub(r'VACATION TRUST INC, VACATION TRUST INC$'
                         r'|VACATION TRUST INC$'
                         r'|I DRIVE RESORTS LLC$'
                         r'|BLUEGREEN VACATIONS CORPORATION$'
                         r'|BLUEGREEN VACATIONS UNLIMITED INC$'
                         r'|VACATION TRUST$'
                         r'|VACATION TRUST INC,$', '', grantee).strip()

        grantees = grantee.split(',')
        grantees = [i.strip() for i in grantees]
        if len(grantees) < 2:
            continue

        row['grantee'] = grantee
        append_txt(json.dumps(row), stored_d_2grantees)
    print('len(listing): %s' % len(list_txt(stored_d_2grantees)))

def do_clean_legals():
    listing = list_txt(stored_d_2grantees)
    write_txt('', stored_d_clean_legals)
    for row in listing:
        raw_legal = row['legal']
        legal_regexs = regex_legal.legal_regexs
        legal = raw_legal
        for legal_regex in legal_regexs:
            found = legal_regex.search(raw_legal)
            if found:
                legal = try_excetp_re(found, 'legal')
                break

        more_filters = regex_legal.more_filters
        if legal in more_filters:
            legal = ''

        adding = copy_dict(row, [])
        adding['origin_legal'] = raw_legal
        adding['legal'] = legal
        append_txt(json.dumps(adding), stored_d_clean_legals)

def do_clean_names(fname):
    listing = list_txt(stored_d_clean_legals)
    write_txt('', stored_d_clean_names)
    for row in listing:
        if row['grantee'] in ['CHICAGO TITLE TIMESHARE LAND TRUST INC, FLEX VACATIONS TRUST']:
            continue

        grantee = row['grantee'].split(',')
        grantee = [i.strip() for i in grantee]

        grantee1 = grantee[0]
        grantee2 = grantee[1]

        correct_grantee1 = separate_first_last_middle_name(grantee1)
        correct_grantee2 = separate_first_last_middle_name(grantee2)

        adding = copy_dict(row)
        adding['first_name1'] = correct_grantee1['first']
        adding['middle_name1'] = correct_grantee1['middle']
        adding['last_name1'] = correct_grantee1['last']

        adding['first_name2'] = correct_grantee2['first']
        adding['middle_name2'] = correct_grantee2['middle']
        adding['last_name2'] = correct_grantee2['last']

        append_txt(json.dumps(adding), stored_d_clean_names)

    fname = 'clean_names-occompt-%s' % fname
    write_dicts_xlsx(list_txt(stored_d_clean_names), fname)

def do_pdfs(threads, fpath):
    data = []
    for row in read_dicts_xlsx(fpath):
        fname = os.path.join(download_dir, row['pdf_name'])

        if os.path.isfile(fname):
            print('%s existed' % fname)
            continue

        adding = {
            'fname': row['pdf_name'],
            'url': row['pdf_url'],
        }
        data.append(adding)
    for i in range(3):
        pool_store_data(data, func=store_dowload_pdfs, stored_file='', threads=threads)

def do_pdfs_MARRIOT(threads):
    data = []
    for row in list_txt_gen(stored_d_docs):
        pdf_name_mortgage = row['pdf_name_mortgage']
        if not pdf_name_mortgage:
            continue

        fname = os.path.join(download_dir, row['pdf_name_mortgage'])
        if os.path.isfile(fname):
            print('%s existed' % fname)
            continue

        adding = {
            'fname': row['pdf_name_mortgage'],
            'url': row['pdf_url_mortgage'],
        }
        data.append(adding)

    for i in range(3):
        pool_store_data(data, func=store_dowload_pdfs, stored_file='', threads=threads)

def do_write_texts(threads, fpath):
    data = read_dicts_xlsx(fpath)
    pool_store_data(data, func=store_txts, stored_file='', threads=threads)

def do_write_texts_MARRIOT(threads):
    data = []
    for row in list_txt_gen(stored_d_docs):
        pdf_name_mortgage = row['pdf_name_mortgage']
        if not pdf_name_mortgage:
            continue
        adding = copy_dict(row, [])
        data.append(adding)

    pool_store_data(data, func=store_txts_MARRIOT, stored_file='', threads=threads)

def do_values(excel_fname):
    listings = read_dicts_xlsx(excel_fname)
    write_txt('', stored_details)
    delete_dir(except_values_dir)
    for row in listings:
        fname = row['pdf_name']
        adding = copy_dict(row, [])
        if fname:
            pdf_fname = download_dir + '/' + fname
            txt_fname = re.sub(r'\.pdf$', '.txt', pdf_fname)
            txt = read_txt(txt_fname)

            value = deed_values.get_regex_value(txt)

            # todo: manual_values
            manual_values = deed_values.manual_values
            for key in manual_values:
                if key in fname:
                    value = manual_values[key]
                    break

            # todo: save exceptions
            for except_re in deed_values.except_regexes:
                except_found = except_re.search(value)
                if except_found:
                    # todo: copy value exceptions
                    create_dir(except_values_dir)
                    pdf_src = f'{download_dir}/{fname}'
                    pdf_dst = f'{except_values_dir}/{fname}'
                    copyfile(pdf_src, pdf_dst)
                    copyfile(re.sub(r'\.pdf$', '.txt', pdf_src), re.sub(r'\.pdf$', '.txt', pdf_dst))
                    break
            value = re.sub(r'^-$', '', value)
            adding['value'] = value
        append_txt(json.dumps(adding), stored_details)  # todo: different "stored_details"

def do_values_MARRIOT():
    listings = list_txt_gen(stored_d_docs)
    write_txt('', stored_d_values)
    delete_dir(except_values_dir)
    for row in listings:
        fname = row['pdf_name_mortgage']
        adding = copy_dict(row, [])
        if fname:
            pdf_fname = download_dir + '/' + fname
            txt_fname = re.sub(r'\.pdf$', '.txt', pdf_fname)
            txt = read_txt(txt_fname)

            value = deed_values.get_regex_value(txt)

            # todo: manual_values
            manual_values = deed_values.manual_values
            for key in manual_values:
                if key in fname:
                    value = manual_values[key]
                    break

            # todo: save exceptions
            for except_re in deed_values.except_regexes:
                except_found = except_re.search(value)
                if except_found:
                    # todo: copy value exceptions
                    create_dir(except_values_dir)
                    pdf_src = f'{download_dir}/{fname}'
                    pdf_dst = f'{except_values_dir}/{fname}'
                    copyfile(pdf_src, pdf_dst)
                    copyfile(re.sub(r'\.pdf$', '.txt', pdf_src), re.sub(r'\.pdf$', '.txt', pdf_dst))
                    break
            value = re.sub(r'^-$', '', value)
            adding['value'] = value
        append_txt(json.dumps(adding), stored_d_values)  # todo: different "stored_d_values"

def do_points_MARRIOT():
    listings = list_txt_gen(stored_d_values)
    write_txt('', stored_details)
    delete_dir(except_points_dir)
    for row in listings:
        fname = row['pdf_name_mortgage']
        adding = copy_dict(row, [])
        adding['points'] = ''
        if fname:
            pdf_fname = download_dir + '/' + fname
            txt_fname = re.sub(r'\.pdf$', '.txt', pdf_fname)
            txt = read_txt(txt_fname)

            points = deed_points.get_regex_points(txt)

            # todo: manual_values
            manual_points = deed_points.manual_points
            for key in manual_points:
                if key in fname:
                    points = manual_points[key]
                    break

            # todo: save exceptions
            for except_re in deed_points.except_regexes:
                except_found = except_re.search(points)
                if except_found:
                    # todo: copy value exceptions
                    create_dir(except_points_dir)
                    pdf_src = f'{download_dir}/{fname}'
                    pdf_dst = f'{except_points_dir}/{fname}'
                    copyfile(pdf_src, pdf_dst)
                    copyfile(re.sub(r'\.pdf$', '.txt', pdf_src), re.sub(r'\.pdf$', '.txt', pdf_dst))
                    break
            points = re.sub(r'^-$', '', points)
            adding['points'] = points
        append_txt(json.dumps(adding), stored_details)

def do_ouput(fname):
    data = []
    for row in list_txt(stored_details):
        adding = copy_dict(row, ['pdf_name', 'pdf_url'])
        data.append(adding)

    output_name = re.sub(r'^.*?/output_truepeoplesearch', 'output_pdfs/output-pdfs', fname)
    write_dicts_xlsx(data, output_name)

def do_ouput_MARRIOT(fname):
    data = []
    # for row in list_txt(stored_details):
    for row in list_txt(stored_d_docs):
        adding = copy_dict(row, ['pdf_name', 'pdf_url', 'pdf_name_mortgage', 'pdf_url_mortgage'])
        data.append(adding)

    output_name = re.sub(r'^.*?/output_truepeoplesearch', 'output_pdfs/output-pdfs', fname)
    write_dicts_xlsx(data, output_name)

def separate_first_last_middle_name(grantee):
    grantee = re.sub(r'\s+', ' ', grantee).strip()
    grantee = re.sub(r'HILTON RESORTS CORPORATION$', '', grantee).strip()
    grantee_regexs = [
        # todo: Suffix
        re.compile(r'^(?P<last>.*?) (?P<first>.*?) (?P<middle>.*) (?P<chars>JR|SR|I+|IV)$', re.I),
        re.compile(r'^(?P<last>.*?) (?P<first>.*?) (?P<chars>JR|SR|II+|IV)$', re.I),

        # todo: 4 words
        re.compile(r'^(?P<last>[A-Z]{2,}?) (?P<first>[A-Z]{2,}?) (?P<middle>[A-Z]{2} [A-Z]{2})$', re.I),  # todo: DIAZ XIOMARA RE AL
        re.compile(r'^(?P<last>[A-Z]{2,}?) (?P<first>[A-Z]{2,}?) (?P<middle>[A-Z] [A-Z]{2,})$', re.I),  # todo: MILLS MELISSA D SHONNE
        re.compile(r'^(?P<last>[A-Z]+?) (?P<first>[A-Z]{2,}?) (?P<middle>[A-Z] [A-Z])$', re.I),  # todo: CALLO STEPHEN E A
        re.compile(r'^(?P<last>[A-Z]+? [A-Z]+?) (?P<first>[A-Z]+?) (?P<middle>[A-Z]+)$', re.I),

        # todo: 3 words
        re.compile(r'^(?P<last>.*?) (?P<first>.*?) (?P<middle>.*)$'),

        # todo: 2 words
        re.compile(r'^(?P<last>.*?) (?P<first>.*?)$'),
    ]

    name = {
        'first': '',
        'middle': '',
        'last': '',
    }
    for index, grantee_regex in enumerate(grantee_regexs):
        re_found = grantee_regex.search(grantee)
        if re_found:
            first = try_excetp_re(re_found, 'first')
            middle = try_excetp_re(re_found, 'middle')
            last = try_excetp_re(re_found, 'last')
            chars = try_excetp_re(re_found, 'chars')

            last = last + ' ' + chars
            last = last.strip()

            name['first'] = first
            name['middle'] = middle
            name['last'] = last
            break
    return name

def job_names(threads, search_input, start=1, stop=200):
    start_date = re.sub(r'/', '_', search_input['start_date'])
    end_date = re.sub(r'/', '_', search_input['end_date'])
    fname = '%s-%s-to-%s' % (search_input['short_name'], start_date, end_date)

    do_listings(threads, search_input, start, stop)
    do_clean_legals()
    do_clean_names(fname)

def do_cache_docs(threads, fpath):
    caches = []
    for row in read_dicts_xlsx(fpath):
        indicator = re.search(r'\d+$', row['description']).group()
        indicator = int(indicator)
        mortgage_doc_id = str(indicator + 1)

        if os.path.exists('%s/%s.txt' % (cache_dir, hash_name(mortgage_doc_id))):
            print('"%s" existed....' % mortgage_doc_id)
            continue
        caches.append(mortgage_doc_id)

    data = []
    for chunk in chunks_gen(caches, 2):
        inp = {
            'caches': chunk,
            'url': 'https://or.occompt.com/recorder/eagleweb/docSearch.jsp?searchId=2'
        }
        data.append(inp)
    pool_store_data(data, func=cache_docs, stored_file='', threads=threads)

def do_d_docs(threads, fpath):
    data = []
    for row in read_dicts_xlsx(fpath):
        indicator = re.search(r'\d+$', row['description']).group()
        indicator = int(indicator)
        mortgage_doc_id = str(indicator + 1)
        adding = copy_dict(row, [])
        adding['mortgage_doc_id'] = mortgage_doc_id
        adding['url'] = mortgage_doc_id
        data.append(adding)

    pool_store_data(data, func=store_d_docs, stored_file=stored_d_docs, threads=threads)

def job_pdfs(threads, fpath):
    do_pdfs(threads, fpath)
    deleteFiles(download_dir, '.crdownload')

def job_pdfs_MARRIOT(threads):
    do_pdfs_MARRIOT(threads)
    deleteFiles(download_dir, '.crdownload')

def job_values(fname):
    do_values(fname)
    do_ouput(fname)





if __name__ == "__main__":

    # ============= Global variables ========
    print('Start....^^')

    # todo: var
    search_by = 'Grantor'
    lname_fname = 'VISTANA DEVELOPMENT INC'
    short_name = 'VDI'
    search_type = 'Exact Match'
    doc_type = 'Deed'
    legal = 'TS'
    ranges = [
        {'start_date': '08/30/2012', 'end_date': '12/09/2020'},
    ]
    for date_range in ranges:
        search_input = copy_dict(date_range, [])
        search_input.update({
            'search_by': search_by,
            'lname_fname': lname_fname,
            'short_name': short_name,
            'search_type': search_type,
            'doc_type': doc_type,
            'legal': legal,
            'url': 'https://or.occompt.com/recorder/eagleweb/docSearchResults.jsp?searchId=0',
        })

        # do_cache_listings(search_input)

        # job_names(1, search_input)

    # todo START PDFs deed (ex: MARRIOT) ------------------
    # for i in range(1):
    #     try:
    #         dirpath = 'SFV_output'
    #         for index, fname in enumerate(os.listdir(dirpath)):
    #             fpath = f'{dirpath}/{fname}'
                # if not index == 8:
                # if index < 8:
                #     continue

                # sleep(0, f'index {index}\n{fpath} ... \n')
                # # todo: cache docs
                # do_cache_docs(2, fpath)
                #
                # # todo: store docs
                # do_d_docs(1, fpath)

                # # todo: pdfs mortgage
                # job_pdfs_MARRIOT(3)
                #
                # # todo: txts mortgage
                # do_write_texts_MARRIOT(1)
                #
                # # todo: values mortgage
                # do_values_MARRIOT()
                #
                # # todo: points mortgage
                # do_points_MARRIOT()

                # todo: do output
                # do_ouput_MARRIOT(fpath)
        # except:
        #     pass


    # todo END PDFs deed ------------------

    # todo: ------------------------------------------------------------------------------------------------------------------------------------------------

    # todo START PDFs Deed Mortgage (ex: HILTON) ------------------
    dirpath = 'BG_output'
    for idex, fname in enumerate(os.listdir(dirpath)):
        fpath = f'{dirpath}/{fname}'
        if not idex == 0:
            continue

        sleep(3, fpath)

        # todo: pdfs
        job_pdfs(3, fpath)

        # todo: txts
        do_write_texts(1, fpath)

        # todo: do_values
        do_values(fpath)

        # todo: do output
        do_ouput(fpath)

    # todo END PDFs Deed Mortgage ------------------

    print('Finished....!')

    # url = {
    #     'start_date': '08/07/2018',
    #     'end_date': '08/01/2019',
    #     'lname_fname': 'grantor hilton',
    #     'url': 'https://or.occompt.com/recorder/eagleweb/docSearchResults.jsp?searchId=0',
    # }
    # delete_cache(url['url'], cache_dir)
    # data = scrape_cache_listings(url,  headless=False)
    # print(data[0])

    # inp = {
    #     'pdfs': [
    #         {'fname': '20180484832.pdf', 'url': 'https://or.occompt.com/recorder/eagleweb/downloads/20180484832?id=DOC2452S3966.A0&parent=DOC2452S3966&preview=false&noredirect=true'}
    #     ],
    #     'ip': '45.72.57.14:8800'
    # }
    # delete_file(os.path.join(download_dir, '20180484832.pdf'))
    # dowload2(inp, headless=True)

    # inp = {
    #     'caches': ['20180672063'],
    #     'url': 'https://or.occompt.com/recorder/eagleweb/docSearch.jsp?searchId=2'
    # }
    # delete_cache('20180672063', cache_dir)
    # cache_docs(inp, headless=False)

    # inp = {
    #     'fname': '20180484832.pdf',
    #     'url': 'https://or.occompt.com/recorder/eagleweb/downloads/20180484832?id=DOC2452S3966.A0&parent=DOC2452S3966&preview=false&noredirect=true'
    # }
    # delete_file(os.path.join(download_dir, '20180484832.pdf'))
    # download_pdfs(inp, download_dir=download_dir, headless=False)



















