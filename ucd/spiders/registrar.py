import requests
from lxml import etree
import ssl
import xlwt
import time


#设置表格样式
def set_style(name,height,bold=False):
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = name
    font.bold = bold
    font.color_index = 4
    font.height = height
    style.font = font
    return style

def ucdavis(name):
    headers = {
        'Referer': 'https://registrar-apps.ucdavis.edu/courses/search/index.cfm',
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
    }

    data = {
        'termCode': '201910',
        'course_number': '',
        'multiCourse': '',
        'course_title': '',
        'instructor': '',
        'subject': '%s'%name,
        'course_start_eval': '-',
        'course_start_time': '-',
        'course_end_eval': '-',
        'course_end_time': '-',
        'course_status': '-',
        'course_level': '-',
        'course_units': '-',
        'virtual': '-',
        'runMe': '1',
        'clearMe': '1',
        'reorder': '',
        'gettingResults': '0',
        'search': 'Search',
        '_cf_nodebug': 'true',
        '_cf_nocache': 'true'
    }

    res = requests.post("https://registrar-apps.ucdavis.edu/courses/search/course_search_results.cfm", headers=headers,
                        data=data)

    content = res.text.split('<h2>')[1].split('</h2>')[0].replace('\n', '')
    html = etree.HTML(content)
    result = etree.tostring(html)
    str_html = str(result.decode('utf-8'))
    str_html.replace('&#13;', '')
    html1 = etree.HTML(str_html)

    ucdavis_list = []
    for i in html1.xpath('//tr[@onmouseover="this.bgColor=\'#D9E0EC\'"]'):

        if i.xpath('td/strong/text()'):
            crn = i.xpath('td/strong/text()')[0]
            ucdavis_dic = {}
            ucdavis_dic.update({'crn':crn})
            ucdavis_list_a = []
            ucdavis_list_b = []
            for m in i.xpath('td/text()'):
                y = str(m).replace('\r','').strip().replace('• ','').replace('No GE Credit','').strip()
                if y:
                    ucdavis_list_a.append(y)

            for m in i.xpath('td/em/text()'):
                y = str(m).replace('\r','').strip().replace('• ','').replace('No GE Credit','').strip()
                if y:
                    ucdavis_list_b.append(y)


            ucdavis_dic.update({'course':ucdavis_list_a[0]})
            ucdavis_dic.update({'title': ucdavis_list_a[2]})
            ucdavis_dic.update({'instructor': ucdavis_list_a[len(ucdavis_list_a)-1]})
            ucdavis_dic.update({'time': ucdavis_list_b[0]})
            ucdavis_dic.update({'location': ucdavis_list_b[1]})
            ucdavis_dic.update({'units': ucdavis_list_b[len(ucdavis_list_b)-1]})

            date_day = ucdavis_dic['time'].split(' ')
            week = ''
            if len(date_day) > 3:
                print(date_day)
                time = date_day[0]+ date_day[1]+date_day[2]

                if date_day[4]:
                    week = date_day[3]+date_day[4]
                else:
                    week = date_day[3]
                ucdavis_dic.update({'time':time})
                ucdavis_dic.update({'week':week})

            titlle_list = ucdavis_dic['course'].split(' ')
            ucdavis_dic.update({'course':titlle_list[0]})
            ucdavis_dic.update({'number':titlle_list[1]})
            ucdavis_list.append(ucdavis_dic)

    print(ucdavis_list)
    excel(name, ucdavis_list)


def excel(name,dic):


    f = xlwt.Workbook()
    sheet1 = f.add_sheet('学生', cell_overwrite_ok=True)
    row0 = ["University", "Department", "Instructor", "Course title", 'Course number','Units','Type','Time','Week','Room','Footnotes','name']

    # 写第一行
    for i in range(0, len(row0)):
        sheet1.write(0, i, row0[i], set_style('Times New Roman', 220, True))
    # 写第一列
    for i in range(0, len(dic)):

        sheet1.write(i + 1, 0, 'University of California Davis', set_style('Times New Roman', 220, True))
        sheet1.write(i + 1, 2, dic[i]['instructor'], set_style('Times New Roman', 220, True))
        sheet1.write(i + 1, 3, dic[i]['course'], set_style('Times New Roman', 220, True))
        sheet1.write(i + 1, 4, dic[i]['number'], set_style('Times New Roman', 220, True))
        sheet1.write(i + 1, 5, dic[i]['units'], set_style('Times New Roman', 220, True))
        if len(dic[i]) < 6:
            sheet1.write(i + 1, 7, dic[i]['time'], set_style('Times New Roman', 220, True))
            sheet1.write(i + 1, 8, dic[i]['week'], set_style('Times New Roman', 220, True))
        sheet1.write(i + 1, 9, dic[i]['location'], set_style('Times New Roman', 220, True))
        sheet1.write(i + 1, 11, dic[i]['title'], set_style('Times New Roman', 220, True))

    f.save('%s.xls'%name)

def suoxie():
    res = requests.post("https://registrar-apps.ucdavis.edu/courses/search/index.cfm")
    html = etree.HTML(res.text)
    suo = html.xpath('//select[@name="subject"]/option/@value')
    del suo[0]
    print(suo)
    print(len(suo))
    for i in suo:
        print(i)
        ucdavis(i)
        time.sleep(5)

if __name__ == '__main__':
    #ucdavis()
    suoxie()

