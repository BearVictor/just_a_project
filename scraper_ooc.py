import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from responses import MyResponse
from modules import *
import config as Config

proxies = []
my_response = MyResponse(proxies=proxies, api='')

cache_dir = Config.cache_dir
except_dir = Config.except_dir

def ooc_field_found(re_compile, td2_text):
    rec_date_regex = re_compile.search(td2_text)
    rec_date = ''
    if rec_date_regex:
        rec_date = rec_date_regex.group(1).strip()
    return rec_date

def scrape_listings(inp, *, stop=9, timeout=45, cache=True, cache_read=False, request_called=True):
    url = inp.strip() if isinstance(inp, str) else inp['url'].strip()
    cache_name = str(url)
    try:
        if cache and os.path.exists('%s/%s.txt' % (cache_dir, hash_name(cache_name))):
            if cache_read is False:
                print(f'[+] {inspect.stack()[0][3]}(!cache_read): {url}')
                return
            cache = False
            parser_text = read_cache(cache_name, directory=cache_dir)
        else:
            if request_called is False:
                print(f'[+] {inspect.stack()[0][3]}(!request_used): {url}')
                return

            response = my_response.get(url, stop=stop, timeout=timeout)
            if response is None:
                return
            parser_text = response.text.replace('&nbsp;', ' ')

        parser = html.fromstring(parser_text)
        # parser = json.loads(parser_text)

        # todo: extract data
        scraped_datas = []
        listing = xpath_listing(parser, '//table[@id="searchResultsTable"]/tbody/tr')
        if listing:
            message(f'[+] {inspect.stack()[0][3]} (len)', len(listing))
            listing_len = len(listing)
            if listing_len < 51:
                sleep(3, 'listing_len (%s) ...' % listing_len)

            for ele in listing:
                description = ' '.join(xpath_strings(ele, './td[1]//text()'))

                td2_text = xpath_string(ele, './td[2]//text()')

                rec_date = ooc_field_found(re.compile(r'Rec Date:(.*)?BookPage:'), td2_text)
                legal = ooc_field_found(re.compile(r'Legal:(.*)?Doc Deed Tax:'), td2_text)

                search_for = xpath_string(parser, '//p[./strong[text()="You searched for:"]]//text()')

                grantee = ooc_field_found(re.compile(r'Grantee:(.*?)Legal:'), td2_text)
                if 'GranteeID' in search_for:
                    grantee = ooc_field_found(re.compile(r'Grantor:(.*?)Grantee:'), td2_text)

                view_image = xpath_string(ele, './/a[contains(text(), "View Image")]/@href')

                pdf_name = get_number_fstring(description) + '.pdf'

                pdf_url = re.sub(r'viewAttachment\.jsp\?docName=', '', view_image)
                pdf_url = re.sub(r'&id', '?id', pdf_url)
                pdf_url = 'https://or.occompt.com/recorder/eagleweb/downloads/{}&preview=false&noredirect=true'.format(
                    pdf_url)

                business_details = {} if isinstance(inp, str) else copy_dict(inp)
                business_details.update({
                    'description': description,
                    'rec_date': rec_date,
                    'legal': legal,
                    'grantee': grantee,
                    'pdf_name': pdf_name,
                    'pdf_url': pdf_url,
                    'parent_url': url,
                })
                scraped_datas.append(business_details)

            if cache:
                write_cache(cache_name, parser_text, directory=cache_dir)
            return scraped_datas

        # todo: notfound
        notfound = re.compile(r'___ not found ___').search(parser_text)
        if notfound:
            message('[x] %s(notfound)' % inspect.stack()[0][3], notfound.group())
            if cache:
                write_cache(cache_name, parser_text, directory=cache_dir)
            return
    except:
        trace_msg = traceback.format_exc().strip()
        error = '[*] %s\n  [+] cache name: %s' % (trace_msg, cache_name)
        print(error)

        if 'KeyboardInterrupt' not in trace_msg:
            exception_path = '/'.join([except_dir, hash_name(trace_msg)])
            write_txt(error, exception_path)

def scrape_d_docs(inp, *, stop=9, timeout=45, cache=True, cache_read=False, request_called=True):
    url = inp.strip() if isinstance(inp, str) else inp['url'].strip()
    cache_name = str(url)
    try:
        if cache and os.path.exists('%s/%s.txt' % (cache_dir, hash_name(cache_name))):
            if cache_read is False:
                print(f'[+] {inspect.stack()[0][3]}(!cache_read): {url}')
                return

            cache = False
            parser_text = read_cache(cache_name, directory=cache_dir)
        else:
            if request_called is False:
                print(f'[+] {inspect.stack()[0][3]}(!request_used): {url}')
                return

            response = my_response.get(url, stop=stop, timeout=timeout)
            if response is None:
                return

            parser_text = response.text

        parser = html.fromstring(parser_text)
        # parser = json.loads(parser_text)

        # todo: extract data

        parser_title = xpath_string(parser, '//p[@style="clear: both;"]//text()')
        if parser_title:
            message(f'[+] {inspect.stack()[0][3]}(parser_title)', parser_title)

            business_details = {} if isinstance(inp, str) else copy_dict(inp)
            mortgages_total = 0

            listing = xpath_listing(parser, '//table[@id="searchResultsTable"]/tbody/tr')
            for ele in listing:
                description = ' '.join(xpath_strings(ele, './td[1]//text()'))
                print(description)
                if not re.search(r'^Mortgage \d+$', description):
                    continue


                td2_text = xpath_string(ele, './td[2]//text()')

                grantor = ooc_field_found(re.compile(r'Grantor:(.*?)Grantee:'), td2_text)
                inp_grantee = inp.get('grantee')
                if inp_grantee != grantor:
                    continue

                rec_date = ooc_field_found(re.compile(r'Rec Date:(.*)?BookPage:'), td2_text)
                legal = ooc_field_found(re.compile(r'Legal:(.*)?Doc Deed Tax:'), td2_text)
                grantee = ooc_field_found(re.compile(r'Grantee:(.*?)Legal:'), td2_text)

                view_image = xpath_string(ele, './/a[contains(text(), "View Image")]/@href')

                pdf_name = get_number_fstring(description) + '.pdf'

                pdf_url = re.sub(r'viewAttachment\.jsp\?docName=', '', view_image)
                pdf_url = re.sub(r'&id', '?id', pdf_url)
                pdf_url = 'https://or.occompt.com/recorder/eagleweb/downloads/{}&preview=false&noredirect=true'.format(
                    pdf_url)

                business_details.update({
                    'description_mortgage': description,
                    'rec_date_mortgage': rec_date,
                    'legal_mortgage': legal,
                    'grantor_mortgage': grantor,
                    'grantee_mortgage': grantee,
                    'pdf_name_mortgage': pdf_name,
                    'pdf_url_mortgage': pdf_url,
                    'parent_url_mortgage': url,
                })
                mortgages_total += 1

            if mortgages_total == 0:
                business_details.update({
                    'description_mortgage': '',
                    'rec_date_mortgage': '',
                    'legal_mortgage': '',
                    'grantor_mortgage': '',
                    'grantee_mortgage': '',
                    'pdf_name_mortgage': '',
                    'pdf_url_mortgage': '',
                    'parent_url_mortgage': '',
                })
            business_details['mortgages_total'] = mortgages_total
            if cache:
                write_cache(cache_name, parser_text, directory=cache_dir)
            return business_details

        # todo: notfound
        notfound = re.compile(r'___ not found ___').search(parser_text)
        if notfound:
            message('[x] %s(notfound)' % inspect.stack()[0][3], notfound.group())
            if cache:
                write_cache(cache_name, parser_text, directory=cache_dir)
            return
    except:
        trace_msg = traceback.format_exc().strip()
        error = '[*] %s\n  [+] cache name: %s' % (trace_msg, cache_name)
        print(error)

        if 'KeyboardInterrupt' not in trace_msg:
            exception_path = '/'.join([except_dir, hash_name(trace_msg)])
            write_txt(error, exception_path)

if __name__ == "__main__":
    # ============= Global variables ========
    print('Start ..... ^^')


    print('Finished ......... !')

    # url = {
    #     'start_date': '01/01/2019',
    #     'end_date': '05/01/2019',
    #     'lname_fname': 'Marriot',
    #     'url': '01/01/201905/01/2019Marriot1',
    # }
    url = {
        'start_date': '08/30/2012',
        'end_date': '12/09/2020',
        'lname_fname': 'VISTANA DEVELOPMENT INC',
        'url': '08/30/201212/09/2020VISTANA DEVELOPMENT INC1',
    }
    data = scrape_listings(url, cache_read=True)
    print(json.dumps(data[0]))

    # url = {"f2_indicator": "20180672063", "f2_indicators": "20180430692, 20180672063", "f2_indicators_total": 2, "f2_first_name1": "YASUSHI", "f2_last_name1": "UEDA", "f2_first_name2": "RIKA", "f2_last_name2": "UEDA", "f2_matched_type": "last_name", "f2_wireless1": "", "f2_wireless2": "", "f2_landlines": "", "f2_address1": "1610 Nantucket Cir", "f2_address2": "#313", "f2_city": "Santa Clara", "f2_state": "CA", "f2_zipcode": "95054", "start_date": "08/20/2018", "end_date": "12/14/2018", "lname_fname": "MARRIOTT OWNERSHIP RESORTS INC", "indicator": "20180672063", "description": "Deed 20180672063", "rec_date": "11/16/2018 03:42:39 PM", "legal": "MARRIOTT OWNERSHIP RESORTS INC", "grantee": "UEDA YASUSHI, UEDA RIKA, UEDA MASAYUKI", "first_name1": "YASUSHI", "middle_name1": "", "last_name1": "UEDA", "first_name2": "RIKA", "middle_name2": "", "last_name2": "UEDA", "value": "", "page": 140, "grantee1": "YASUSHI UEDA", "grantee2": "RIKA UEDA", "matched_grantee1": "Masashi Ueda", "matched_grantee2": "Rika Ueda", "similar1": 83.3, "similar2": 100, "search_by": "grantee2", "wirelesses1": "", "wirelesses2": "", "landlines": "", "address1": "1610 Nantucket Cir", "address2": "#313", "city": "Santa Clara", "state": "CA", "zipcode": "95054", "matched_url": "https://www.truepeoplesearch.com/details?name=RIKA%20UEDA&rid=0xl", "area_codes": "", "area_codes_url": "", "mortgage_doc_id": "20180672064", "url": "20180672064"}
    # data = scrape_d_docs(url, cache_read=True, request_called=False)
    # print(json.dumps(data))




