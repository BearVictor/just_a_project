from modules import *
value_regexs = [
            re.compile(r'[\s_"](\$\d*,\d[\d,.]+\d)[.,/”]? [“~_)|}.:-]+ ?, [wW]hich indebtedness'),
            re.compile(r'[\s_"](\$\d*,\d[\d,.]+\d)[.,/”]? [“~_)|}.:-]? ?, [wW]hich indebtedness'),
            re.compile(r'[\s_"](\$\d*,\d[\d,.]+\d)[.,/”]? \), [wW]hich indebtedness'),

            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? [“~_)|}.:-]+ ?[,.)]+ [wW]hich indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? [“~_)|}.:-]+ ?[,.)]+ [wW]hich indebiedness'),

            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? [,.:~] \), [wW]hich indebtedness'),

            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? [”),;|.-]+ [wW]hich indebtedness'),

            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]?___\), [wW]hich indebtedness'),

            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? __° _\), which indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? Js which indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]?____\), which indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? \), whict lebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? \|, which indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? \. which indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? \),-which indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? 7 \), which indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? \* \), which indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? \), whic! lebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? , which indebtednéss'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]?\* , which indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]?\) , which indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]? hs which indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]?_—_\), Which indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]?__\), which indebtedness'),
            re.compile(r'\(\$(\d[\d,.]+\d)[.,/”]? ___\), which indebtedness'),
            re.compile(r'[\s_"](\d[\d,.]+\d)[.,/”]?__\), which indebtedness'),
            re.compile(r'[\s_"\'-](\d[\d,.]+\d)[.,/”]?__\), which indebtedness'),
            re.compile(r'[\s_"\'-](\d[\d,.]+\d)[.,/”]?_—_\), Which indebtedness'),
            re.compile(r'[\s_"\'-](\d[\d,.]+\d)[.,/”]?—_\), which indebtedness'),
            re.compile(r'[\s_"\'-](\d[\d,.]+\d)[.,/”]?____—_\), which indebtedness'),
            re.compile(r'Cents \(\$(\d[\d,.]+\d)\) providing'),
            re.compile(r'Dollars \(\$(\d[\d,.]+\d)\), providing'),
            re.compile(r'—(\d[\d,.]+\d)[.,/”]?__\), which indebtedness'),
            re.compile(r'\*(\d[\d,.]+\d)[.,/”]?__\), which indebtedness'),
            re.compile(r'[\s_"\'-](\d[\d,.]+\d)[.,/”]?[_-]+\), which indebtedness'),
            re.compile(r'[\'](\d[\d,.]+\d)_——_\), which indebtedness'),
            re.compile(r'[\s_"\'-](\d[\d,.]+\d)[_-]+\), which indebtedness'),
            re.compile(r'_(\d[\d,.]+\d)___—_\), which indebtedness'),
            re.compile(r'_(\d[\d,.]+\d) \+\), which indebtedness'),
            re.compile(r'_(\d[\d,.]+\d)_+—+_+\), which indebtedness'),
            re.compile(r' (\d[\d,.]+\d) \+\) which indebtedness'),
            re.compile(r'\*(\d[\d,.]+\d)[.,/”]? SS\), which indebtedness'),
            re.compile(r'd(\d[\d,.]+\d)[.,/”]? SS\), which indebtedness'),
            re.compile(r'\'(\d[\d,.]+\d), \+\), which indebtedness'),
            re.compile(r'«(\d[\d,.]+\d) _\), which indebtedness'),
            re.compile(r'd(\d[\d,.]+\d)_+\), which indebtedness'),
            re.compile(r'_(\d[\d,.]+\d)[_—~]+\), Which indebtedness'),
            re.compile(r'—(\d[\d,.]+\d)[_—~]+ \+\), which indebtedness'),
            re.compile(r'—(\d[\d,.]+\d) \+\), which indebtedness'),
            re.compile(r'=(\d[\d,.]+\d), \+\), which indebtedness'),
            re.compile(r'\*(\d[\d,.]+\d)[_—]+\), which indebtednes'),
            re.compile(r'\$(\d[\d,.]+\d) \+\), which indebtedness'),
            re.compile(r'«(\d[\d,.]+\d) SS\), which indebtedness'),
            re.compile(r'_(\d[\d,.]+\d)[_—]+\), which indebtedness'),
            re.compile(r'\(\$(\d[\d,.]+\d) ~—S_\), which indebtedness'),
            re.compile(r'—(\d[\d,.]+\d)_\), which indebtedness'),
            re.compile(r'_(\d[\d,.]+\d) [_—]+\), which indebtedness'),
            re.compile(r'-(\d[\d,.]+\d) \+\), which indebtedness'),
            re.compile(r' (\d[\d,.]+\d) which indebtedness'),
            re.compile(r' (\d[\d,.]+\d) [—_]+\), which indebtedness'),
            re.compile(r' (\d[\d,.]+\d) _+\); which indebtedness'),
            re.compile(r'\'(\d[\d,.]+\d) \+\)\. which indebtedness'),
            re.compile(r'-(\d[\d,.]+\d), SS\), which indebtedness'),
            re.compile(r'\'(\d[\d,.]+\d)[_—]+\), which indebtedness'),
            re.compile(r'\(\$(\d[\d,.]+\d) _\), which indebtedness'),
            re.compile(r'[\s_](\d[\d,.]+\d)[.,]? ?, which indebtedness'),
            re.compile(r'[\s_](\d[\d,.]+\d)[.,]? \*_\), which indebtedness'),
            re.compile(r'[\s_](\d[\d,.]+\d)[.,]? \|, which indebtedness'),
            re.compile(r'[\s_](\d[\d,.]+\d)[.,_]? \), which indebtedness'),

            re.compile(r'\(US\$(\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'\(US \$(\d{1,3},\d[\d,.]+\d)\), which Indebtedness', re.IGNORECASE),
            re.compile(r'\(US\$\$(\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'\(U\$\$(\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'\(U8\$(\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'\(US! (\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'\(USS(\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'US \$(\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'\{US\$(\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'\(US  \$(\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'\{ S\$(\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'\(Us \$(\d{1,3},\d[\d,.]+\d)\), which ihdebtedness', re.IGNORECASE),
            re.compile(r'US \$(\d{1,3},\d[\d,.]+\d)\), which/ indebtedness', re.IGNORECASE),
            re.compile(r'\(U \$(\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'Pollars Ui \$(\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'U\.S\.   \$(\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'\(US\$(\d{1,3},\d[\d,.]+\d)\), which i tedness', re.IGNORECASE),
            re.compile(r'S\$(\d{1,3},\d[\d,.]+\d)\), which indebtedness', re.IGNORECASE),
            re.compile(r'\(US\$(\d{1,3},\d[\d,.]+\d)\), which indabtedness', re.IGNORECASE),
            re.compile(r'\(US: \$(\d{1,3},\d[\d,.]+\d)\), which indebtedness ', re.IGNORECASE),
            re.compile(r'\(US\$(\d{2}, \d[\d,.]+\d)\), which indebtedness'),
            re.compile(r'\(US \$(\d{2}, \d[\d,.]+\d)}, which indebtedness'),
            re.compile(r'\(U\.S\. \$(\d{3}, \d[\d,.]+\d)\) plus interest'),

            re.compile(r'\(US \$(\d[\d,.]+\d)}, which indebtedness'),
            re.compile(r'\(US\$(\d[\d,.]+\d)}, which indebtedness'),
            re.compile(r'\(US \$(\d[\d,.]+\d)\)“which indebtedness'),
            re.compile(r'\(US\$(\d[\d,.]+\d)\)}, which indebtedness'),
            re.compile(r'\(US \$(\d[\d,.]+\d)\); which indebtedness'),
            re.compile(r'\(US\$(\d[\d,.]+\d)\); which indebtedness'),
            re.compile(r'\(US\$(\d[\d,.]+\d)\),‘which indebtedness'),
            re.compile(r'\(US \$(\d[\d,.]+\d)} which indebtedness'),
            re.compile(r'\(US\$(\d[\d,.]+\d)\)\. which indebtedness'),
            re.compile(r'\(US\$(\d[\d,.]+\d)\)..hich indebtedness'),
            re.compile(r'\(US \$(\d[\d,.]+\d)\)..which indebtedness'),
            re.compile(r'\(US\$(\d[\d,.]+\d)\), Which indebtedness'),
            re.compile(r'\(US\$(\d[\d,.]+\d)\), Which indebtedness'),
            re.compile(r'\(US\$(\d[\d,.]+\d)}\. which indebtedness'),
            re.compile(r'\(USS(\d{2}, \d[\d,.]+\d)\), which indebtedness'),
            re.compile(r'\(US \$(\d{2}, \d[\d,.]+\d)\), which indebtedness'),
            re.compile(r'\(USS(\d{2}, \d[\d,.]+\d)\), which indebtedness'),
            re.compile(r'\{US \$(\d{2}, \d[\d,.]+\d)\), which indebtedness'),
            re.compile(r'\(S8(\d{2}, \d[\d,.]+\d)\), which indebtedness'),
            re.compile(r'\(US\$(\d{2},\d{3}\. \d{2})\), which indebtedness'),
            re.compile(r'\(US\$(\d \d,\d{3}\.\d{2})\), which indebtedness'),
            re.compile(r'\(US\$(\d{1,3},\d{2} \d\.\d{2})\), which indebtedness', re.I),
            re.compile(r'\(US \$(\d{1,3},\d{3}\.\d{2})\), which indebtedhess', re.I),
            re.compile(r'\(Ws \$(\d{1,3}, \d{3}\.\d{2})\), which indebtedness', re.I),
            re.compile(r'\(US \$(\d{1,3},\d{3}\.\d{2})\), \w+hich indebtedness', re.I),
            re.compile(r'\(US\$(\d{1,3},\d{2} \d\.\d{2})\) \w+vhich indebtedness', re.I),
            re.compile(r'\(US\$(\d{1,3}, \d{3}\.\d{2})\}, which indebtedness', re.I),
            re.compile(r'\(Us\$(\d{1,3}, \d{3}\.\d{2})\), which indebtedness', re.I),
            re.compile(r'\(US\$(\d{1,3},\d{3}\.\d{2})\), which indebtedness', re.I),
            re.compile(r'\(US\$(\d{1,3},\d{3}\.\d{2})\),\.which indebtedness', re.I),
            re.compile(r'\(US \$(\d{1,3},\d{3}\.\d{2})\), which indebledness', re.I),
            re.compile(r'\(US\$(\d{1,3},\d{3}\.\d{2})\), which indebledness', re.I),
            re.compile(r'\(US\$(\d \d,\d{3}\.\d{2})\}, which indebtedness', re.I),
            re.compile(r'\(US\$(\d{1,3},\d{3}\.\d{2})\),’ which indebtedness', re.I),
            re.compile(r'\(US\$(\d{1,3},\d{3}\.\d{2})}\), which indebtedness', re.I),
            re.compile(r'\(US\$(\d{1,3},\d{3}\.\d{2})\), which indebtednass', re.I),
            re.compile(r'\(US\$(\d{1,3},\d{3}\.\d{2})\), which indebtadness', re.I),
            re.compile(r'\(US\$(\d{1,3},\d{3}\.\d{2})\), which indabtadness', re.I),
            re.compile(r'\(US\$(\d{1,3},\d{3}\.\d{2})\), which indabtednass', re.I),
            re.compile(r'\(US\$(\d{1,3},\d{3}\.\d{2})\), which iridebtedness', re.I),
            re.compile(r'\(US\s+\$(\d{1,3},\d{3}\.\d{2})\) which indebtedness', re.I),
            re.compile(r'\{US\s+\$(\d{1,3},\d{3}\.\d{2})\) which indebtedness', re.I),
            re.compile(r'\(US\s+\$(\d{1,3}\.\d{3}\.\d{2})\) which indebtedness', re.I),
            re.compile(r'\(US \$(\d{1,3}\.\d{3},\d{2})\) which indebtedness', re.I),
            re.compile(r'\(US \$(\d{1,3},\d{3},\d{2})\) which indebtedness', re.I),
            re.compile(r'\(US \$(\d{1,3} \d{3}\.\d{2})\) which indebtedness', re.I),
            re.compile(r'\(US  \$(\d{1,3},\d{3}\.\d{2})} which indebtedness', re.I),
            re.compile(r'\(US \$(\d{1,3},\d{3}\.\d{2})\) wiich indebtedness', re.I),

            re.compile(r'Dollars \(\$(\d[\d,.]+\d)\) providing'),
            re.compile(r'Cerits \(\$(\d[\d,.]+\d)\) providing'),
            re.compile(r'Cents\. \(\$(\d[\d,.]+\d)\) providing'),
            re.compile(r'Cents \(U\.S\. \$(\d[\d,.]+\d) \);'),

            re.compile(r'\(U\.S\. \$(\d[\d,.]+\d)\) plus interest'),
            re.compile(r'\(U\.S\. \$(\d[\d,.]+\d)\)  plus interest'),
            re.compile(r'\(U\.S\. \$(\d[\d,.]+\d)\) plus  interest'),
            re.compile(r'\(U\.S\. \$(\d[\d,.]+\d)  plus interest'),
            re.compile(r'\(U\.S\. \$ (\d[\d,.]+\d) \) plus interest'),
            re.compile(r'\(U\.S\. \$ (\d[\d,.]+\d) \)  plus interest'),
            re.compile(r'\(US\. \$(\d[\d,.]+\d)   plus interest'),
            re.compile(r'U\.S\. \$ (\d[\d,.]+\d) \) plus interest'),
            re.compile(r'U\.S\. \$(\d[\d,.]+\d)   plus interest'),
            re.compile(r'\$ (\d[\d,.]+\d) , plus interest'),
            re.compile(r'\(U\.S\. \$(\d[\d,.]+\d) \).*?plus interest'),
            re.compile(r'\(U\.S\. \$ (\d[\d,.]+\d) \)    plus interest'),
            re.compile(r'\(U\.S, \$(\d[\d,.]+\d)  plus interest'),

            re.compile(r'\(\$(\d[\d,.]+\d) \) together with interest'),
            re.compile(r'\(\$(\d[\d,.]+\d)\) together with interest'),
            re.compile(r'\(\$(\d[\d,.]+\d) } together with interest'),

            re.compile(r'dollars \(\$(\d[\d,.]+\d)\) as evidenced'),

            re.compile(r'\(\$\. (\d[\d,.]+\d)\),'),
            re.compile(r'\(Ss\. (\d[\d,.]+\d)\),'),
            re.compile(r'\(S\$\. (\d[\d,.]+\d)\),'),
            re.compile(r'\(\$ (\d[\d,.]+\d)\),'),
            re.compile(r'\(S\. (\d[\d,.]+\d)\),'),
            re.compile(r'&\. (\d[\d,.]+\d)\),'),
            re.compile(r'g\. (\d[\d,.]+\d)\),'),
            re.compile(r'\(S\. (\d[\d,.]+\d), which'),
            re.compile(r'\(\$s (\d[\d,.]+\d)\),'),
            re.compile(r'GS (\d[\d,.]+\d)\),'),
            re.compile(r'\(S_ (\d[\d,.]+\d) —__\),'),
            re.compile(r'\$s (\d[\d,.]+\d)\),'),
            re.compile(r'\(S\$\. (\d[\d,.]+\d) , which'),
            re.compile(r'\(Ss\. (\d[\d,.]+\d) , which'),
            re.compile(r'C3 (\d[\d,.]+\d)\),'),
            re.compile(r'\(\. (\d[\d,.]+\d)\),'),
            re.compile(r'\(S\$ (\d[\d,.]+\d)\),'),
            re.compile(r'\(\$s\. (\d[\d,.]+\d)\),'),
            re.compile(r'\(S (\d[\d,.]+\d) , which'),
            re.compile(r'\(\$\. (\d[\d,.]+\d) , which'),
            re.compile(r'\(8\. (\d[\d,.]+\d) , which'),
            re.compile(r'\(s (\d[\d,.]+\d) , which'),
            re.compile(r'gs (\d[\d,.]+\d) , which'),
            re.compile(r'\(is\. (\d[\d,.]+\d) , which'),
            re.compile(r'S\. (\d[\d,.]+\d)\. \), which'),
            re.compile(r'S\. (\d[\d,.]+\d)\. \), which'),
            re.compile(r'\(s\. (\d[\d,.]+\d) , which'),
            re.compile(r'& (\d[\d,.]+\d)\. , which'),
            re.compile(r'\(S\. (\d[\d,.]+\d) , which'),
            re.compile(r'\(8, (\d[\d,.]+\d) , which'),
            re.compile(r'\(\$ (\d[\d,.]+\d) __\)\. which'),
            re.compile(r'& (\d[\d,.]+\d) , which'),
            re.compile(r'\(\$\. (\d[\d,.]+\d) \|, which'),
            re.compile(r'\(\$\. (\d[\d,.]+\d) \|, which'),
        ]

except_regexes = [
    re.compile(r'^\d{1,3},\d{3},\.\d{2}$'),
    re.compile(r'^\d{3,}[.,]\d+$'),
    re.compile(r'^\d{2}[,.]\d{2}$'),
    re.compile(r'^\d[,.]\d{2}$'),
    re.compile(r'^\d+$'),
    re.compile(r'^$'),
]

def get_regex_value(txt):
    value = ''
    for value_re in value_regexs:
        value_found = value_re.search(txt)
        if value_found:
            value = value_found.group(1).strip()
            break

    re_complie = re.compile(r'^(\d{1,3})\.(\d{3}\.\d{2})$')
    found = re_complie.search(value)
    if found:
        value = found.group(1) + ',' + found.group(2)

    if not found:
        re_complie = re.compile(r'^(\d{1,3})\.(\d{3}),(\d{2})$')
        found = re_complie.search(value)
        if found:
            value = found.group(1) + ',' + found.group(2) + '.' + found.group(3)

    if not found:
        re_complie = re.compile(r'^(\d{1,3}),(\d{3}),(\d{2})$')
        found = re_complie.search(value)
        if found:
            value = found.group(1) + ',' + found.group(2) + '.' + found.group(3)

    if not found:
        re_complie = re.compile(r'^(\d{1,3}) (\d{3})\.(\d{2})$')
        found = re_complie.search(value)
        if found:
            value = found.group(1) + ',' + found.group(2) + '.' + found.group(3)

    value = re.sub(r'[^\d]$', '', value)
    value = re.sub(r'^\$', '5', value)
    value = re.sub(r'\s', '', value)
    return value

def get_manual_values():
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

manual_values = get_manual_values()

if __name__ == '__main__':

    # value = get_regex_value('($13.400.00) together with interest')
    # print(value)
    # sleep(90)

    except_values_dir = 'except_values'
    raw_values = 'raw_values'

    write_txt('', raw_values)
    for fname in os.listdir(except_values_dir):
        indicator = re.sub(r'\.txt$', '', fname)
        if '.txt' in fname:
            fpath = f'{except_values_dir}/{fname}'
            txt = read_txt(fpath)
            value = get_regex_value(txt)

            # todo: manual_values
            manual_values = get_manual_values()
            for key in manual_values:
                if key in fname:
                    value = manual_values[key]
                    break

            # todo: save exceptions
            for except_re in except_regexes:
                except_found = except_re.search(value)
                if except_found:
                    except_str = '%s|%s' % (indicator, except_found.group())
                    append_txt(except_str, raw_values)
                    break

    # write_txt('')
    # points_txt = read_txt('raw_points.txt')
    # for row in read_txt_lines(raw_values):
    #     if row in points_txt:
    #         adding = row + '-'
    #         append_txt(adding)
    #     else:
    #         print('else')

