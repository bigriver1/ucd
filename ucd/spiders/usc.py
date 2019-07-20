# -*- coding: utf-8 -*-
import scrapy
import pymysql

connect = pymysql.connect(
    host='127.0.0.1',
    user='root',
    passwd='root',
    db='easy-a',
    charset='utf8'
)
cursot = connect.cursor()

school_name = 'University of Southern California'


#url = 'https://classes.usc.edu/term-20193/'
url = 'https://classes.usc.edu/term-20193/classes/psyc/'
class UscSpider(scrapy.Spider):

    name = 'usc'
    allowed_domains = ['usc.edu']

    def start_requests(self):

        yield scrapy.Request(url=url, dont_filter=True)
    def parse(self, response):
        data_list = []
        list_dic = []
        #列表数据
        if(len('https://classes.usc.edu/term-20193/')== len(response.url)):
            usc_list = response.xpath('//li[@data-type="department"]')
            for i in usc_list:
                school=i.xpath('@data-school').extract_first()
                code = i.xpath('@data-code').extract_first()
                title = i.xpath('@data-title').extract_first()
                a = i.xpath('a/@href').extract_first()

                sql = 'select * from dep_list where url="%s"' %a
                cursot.execute(sql)
                if cursot.rowcount == 0:
                    sql = 'insert into dep_list  (school,department,title,url) values ("%s","%s","%s","%s")'
                    data = (school_name,school,title,a)
                    cursot.execute(sql % data)
                    connect.commit()
        #详情数据
        else:
            cont = response.xpath('//div[@class="course-table"]/div')
            for i in cont:

                name = i.xpath('./div[@class="course-id"]/h3/a/text()').extract_first()
                name = str(name).rsplit()[0]
                number = i.xpath('./div[@class="course-id"]/h3/a/strong/text()').extract_first()
                name_short = str(number).split(' ')[0]
                name_search = str(number).replace(' ','')
                units = i.xpath('./div[@class="course-id"]/h3/a/span/text()').extract_first()
                units = str(units).split(' ')[0].replace('(','')
                if('-'in units):
                    units=units.split('-')[1]
                introduce = i.xpath('./div[@class="course-details"]/ul|'
                                    './div[@class="course-details"]/div').xpath('string(.)').extract()


                for y in i.xpath('./div[@class="course-details"]/table/tr'):
                    type_ke = y.xpath('./td[@class="type"]/text()').extract_first()
                    time = y.xpath('./td[@class="time"]/text()').extract_first()
                    days = y.xpath('./td[@class="days"]/text()').extract_first()
                    closed = y.xpath('./td[@class="registered"]').xpath('string(.)').extract_first()
                    instructor = y.xpath('./td[@class="instructor"]').xpath('string(.)').extract_first()
                    location = y.xpath('./td[@class="location"]').xpath('string(.)').extract_first()
                    location_url = y.xpath('./td[@class="location"]/a/@href').extract_first()
                    location_u = 'https://web-app.usc.edu%s'%location_url
                    lightbox = y.xpath('./td[@class="info"]/a/@href').extract_first()

                    if ( str(instructor) == '' ):
                        pass
                    elif (str(instructor) =='None'):
                        pass
                    elif (str(instructor) is None):
                        pass
                    else:

                        if ('of' in str(closed)):
                            closed = str(closed).split('of')[1]

                        dic = {'name':name ,'number':number,"name_short":name_short,'name_search':name_search,'units':units,'introduce':introduce,
                               'type_ke':type_ke,'time':time,'days':days,'closed':closed,'instructor':instructor,'location':location,
                               'location_u':location_u,'lightbox':lightbox}
                        if(',' in str(instructor)):
                            list_dic=data_dic(dic)
                            data_list += list_dic
                        else:
                            data_list.append(dic)

                #学校数据tuple
                school_tuple=school_data(response.url)

                for q in data_list:
                    print(q)
                    sql = 'insert into clt_easya  (school,department,name,name_short,number,number_search,units,type,time,days,registered,location,introduce,info,title,instructor,locationurl) values ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                    data = (school_tuple[0],school_tuple[2],name,name_short,)
                    cursot.execute(sql % data)
                    connect.commit()

                sql = 'update  dep_list set type = 1 where url="%s"' % response.url
                cursot.execute(sql)
                connect.commit()

        sql = 'select url from dep_list where type=0'
        cursot.execute(sql)
        for row in cursot.fetchall():
            pass
            #yield scrapy.Request(row,callback=self.parse,dont_filter=True)


#多教授循环
def data_dic(dic):
    dic_list = []
    for i in str(dic['instructor']).split(','):
        dict = {'name': dic['name'], 'number': dic['number'], "name_short": dic['name_short'], 'name_search': dic['name_search'], 'units': dic['units'],
               'introduce': dic['introduce'], 'type_ke': dic['type_ke'], 'time': dic['time'], 'days': dic['days'], 'closed': dic['closed'],
               'instructor': i, 'location': dic['location'], 'location_u': dic['location_u'], 'lightbox': dic['lightbox']}
        dic_list.append(dict)

    return dic_list

#查询学校专业信息
def school_data(url):
    sql = 'select school , title , department from dep_list where url="%s"' % url
    cursot.execute(sql)
    for row in cursot.fetchall():
        return row