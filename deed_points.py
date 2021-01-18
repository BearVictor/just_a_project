from modules import *
points_regexs = [
    re.compile(r'by (\d[\d,]+) Points', re.IGNORECASE),
    re.compile(r'by (\d[\d,]+) Paints,', re.IGNORECASE),
    re.compile(r'by (\d[\d,]+) Poinis,', re.IGNORECASE),
    re.compile(r'by (\d{1,3}\.\d{3}) Points', re.IGNORECASE),
]

except_regexes = [
    re.compile(r'^$'),
    re.compile(r'^[\d,.]+,[^0]00$'),
    re.compile(r'^[\d,.]+,0[^0]0$'),
    re.compile(r'^[\d,.]+,00[^0]$'),
    re.compile(r'^[\d,.]+[6432],000$'),
    re.compile(r'^[\d,.]+,\d{4,}$'),
    re.compile(r'^\d+$'),
]

def get_regex_points(txt):
    points = ''
    for points_re in points_regexs:
        found = points_re.search(txt)
        if found:
            points = found.group(1).strip()
            break

    re_complie = re.compile(r'^(\d{1,3})\.(\d{3})$')
    found = re_complie.search(points)
    if found:
        points = found.group(1) + ',' + found.group(2)

    return points

def get_manual_points():
    listing = """
    
    """
    lines = listing.split('\n')
    regex = re.compile(r'^(.*?)\|(.*?)$')
    data = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        found = regex.search(line)
        data[found.group(1)] = try_excetp_re(found, 2)
    return data



manual_points = get_manual_points()

if __name__ == '__main__':

    # points = get_regex_points('by 60.000 Points')
    # print(points)
    # sleep(90)

    except_points_dir = 'except_points'
    raw_points = 'raw_points'
    write_txt('', raw_points)
    for fname in os.listdir(except_points_dir):
        indicator = re.sub(r'\.txt$', '', fname)
        if '.txt' in fname:
            fpath = f'{except_points_dir}/{fname}'
            txt = read_txt(fpath)
            points = get_regex_points(txt)

            # todo: manual_values
            manual_points = manual_points
            for key in manual_points:
                if key in fname:
                    points = manual_points[key]
                    break

            # todo: save exceptions
            for except_re in except_regexes:
                except_found = except_re.search(points)
                if except_found:
                    print(except_found)
                    except_str = '%s|%s' % (indicator, except_found.group())
                    append_txt(except_str, raw_points)
                    break


