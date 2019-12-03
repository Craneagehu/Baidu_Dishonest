
import pymysql
from DisHonest.settings import MYSQL_HOST,MYSQL_PORT,MYSQL_DB,MYSQL_USER,MYSQL_PASSWORD


class DishonestPipeline(object):
    def open_spider(self,spider):
        #创建数据库连接
        self.connection = pymysql.connect(host=MYSQL_HOST,port=MYSQL_PORT,db=MYSQL_DB,user=MYSQL_USER,password=MYSQL_PASSWORD)

        #获取操作数据库的cursor
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        #如果数据不存在，就插入数据
        #如果是自然人，就根据证件号就行判断
        #如果是企业/组织，就根据 名称 和 区域进行判断
        #如何判断是自然人和企业/组织，根据年龄进行判断，age=0就是企业/组织

        if int(item['age']) == 0:
            ##如果是企业/组织，就根据 名称 和 区域进行判断是否重复
            select_count_sql = f'select count(1) from dishonest where name = "{item["name"]}" and area = "{item["area"]}"'

        else:
            #否则就是自然人
            #为了不与百度失信爬虫的身份证号重复，故对最高人民法院爬虫的身份证号进行处理
            #如果身份证号为18位，则出生月份和天数用*号代替
            card_num = item["card_num"]
            if len(card_num) ==18:
                card_num = card_num[:-8]+"****"+card_num[-4:]
                item["card_num"] = card_num
            select_count_sql = f'select count(1) from dishonest where card_num = "{item["card_num"]}"'


        #执行查询SQL
        self.cursor.execute(select_count_sql)
        count = self.cursor.fetchone()[0]
        if count ==0:
            #如果没有数据，就插入数据
            # 获取所有的字段
            keys = dict(item).keys() #获取字段的列表
            fields = ','.join(keys)  #获取字段的字符串
            values = ','.join(['%s']*len(keys)) #获取值的格式化字符串
            insert_sql = f"insert into dishonest({fields}) values ({values})"
            self.cursor.execute(insert_sql,tuple(dict(item).values()))
            self.connection.commit()

            print('插入成功')
        else:
            #否则就重复了
            spider.logger.info("数据重复")

        return item


    def close_spider(self,spider):
        #关闭cursor,关闭数据库连接
        #1. 关闭cursor
        self.cursor.close()
        #2. 关闭数据库
        self.connection.close()