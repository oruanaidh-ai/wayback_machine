import re


if __name__ == '__main__':

    year2txt = {}
    with open('oruanaidh.bib') as fp:
        txt = ''
        for line in fp:
            if line.strip() != '':

                txt += line

            else:
                m = re.match(r'^\@\S+\{(.|\n)*?year\s*=\s*\{(?P<year>\d+)(.|\n)*\}', txt, re.I|re.M)
                year = m.group('year') if m else '8888'

                if year not in year2txt:
                    year2txt[year] = []
                year2txt[year].append(txt)
                txt = ''



        years = sorted( year2txt.keys() )

        for year in years:
            for entry in year2txt[year]:
                print(entry)
