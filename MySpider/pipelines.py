# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

# useful for handling different item types with a single interface
import pymysql

# 记录错误的列数自动添加列
error_line: int


class GalgamePipelines:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', password='root', database='galgame',
                                    charset='utf8mb4')
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        # 获取需要输入数据库的元素
        title = item.get('title')
        home = item.get('home')
        images = item.get('images')
        downlinks = item.get('downlinks')
        # 开始输入数据库
        tb_galgame_id: int
        tb_galgame_otherId: int

        tb_galgame_id = self.insert_tb_galgame(title, home)
        self.conn.commit()
        tb_galgame_otherId = self.insert_tb_galgame_image(images, tb_galgame_id)
        self.conn.commit()
        self.insert_tb_galgame_downlink(downlinks, tb_galgame_id)
        self.conn.commit()
        self.cursor.execute('UPDATE tb_galgame SET g_images=%s ,g_downlink=%s WHERE g_id=%s',
                            (tb_galgame_otherId, tb_galgame_otherId, tb_galgame_id))
        return item

    def insert_tb_galgame(self, title, home):
        """该函数返回插入数据的主键"""
        try:
            self.cursor.execute('INSERT INTO galgame.tb_galgame(g_title,g_home) VALUE (%s,%s)', (title, home))
            return self.cursor.lastrowid
        except Exception as e:
            print(e, e.args)

    def insert_tb_galgame_image(self, images, tb_galgame_id):
        global error_line
        error_line = 0

        try:
            if error_line == 0:
                self.cursor.execute(
                    f'INSERT INTO galgame.tb_galgame_img (tb_galgame_id) VALUE (%s)', tb_galgame_id)
            tb_images_id = self.cursor.lastrowid
            for i in range(error_line, len(images)):
                error_line = i
                self.cursor.execute(f'UPDATE tb_galgame_img SET i{i} = %s WHERE g_img_id=%s',
                                    (images[error_line], tb_images_id))
            return tb_images_id

        except pymysql.err.OperationalError as e:
            if e.args[0] == 1054:
                self.cursor.execute(f'alter table tb_galgame_img add i{error_line} varchar(600)')
                self.insert_tb_galgame_image(images, tb_galgame_id)
            else:
                logging.error(e.args)

    def insert_tb_galgame_downlink(self, downlinks, tb_galgame_id):
        global error_line
        error_line = 0

        try:
            if error_line == 0:
                self.cursor.execute(
                    f'INSERT INTO galgame.tb_galgame_downlink (tb_galgame_id) VALUE (%s)', tb_galgame_id)
            tb_downlink_id = self.cursor.lastrowid
            for i in range(error_line, len(downlinks)):
                error_line = i
                self.cursor.execute(f'UPDATE tb_galgame_downlink SET d{i} = %s WHERE g_downlink_id=%s',
                                    (downlinks[error_line], tb_downlink_id))
            return tb_galgame_id

        except pymysql.err.OperationalError as e:
            if e.args[0] == 1054:
                self.cursor.execute(f'alter table tb_galgame_downlink add d{error_line} varchar(1000)')
                self.insert_tb_galgame_downlink(downlinks, tb_galgame_id)
            else:
                logging.error(e.args)
        pass
