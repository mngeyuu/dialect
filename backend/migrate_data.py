import pandas as pd
import sqlite3
from django.core.management.base import BaseCommand
import os

class Command(BaseCommand):
    help = '从Excel导入数据到SQLite'

    def handle(self, *args, **options):
        # 连接SQLite数据库
        conn = sqlite3.connect('db.sqlite3')

        # 读取Excel文件
        df = pd.read_excel('data.xlsx')

        # 将数据写入SQLite表
        df.to_sql('core_DialectWord', conn, if_exists='replace', index=False)

        # 处理音频文件路径
        cursor = conn.cursor()
        cursor.execute('SELECT id, audio_file FROM dialect_app_dialectword')
        for row in cursor.fetchall():
            id, audio_path = row
            if audio_path:
                # 设定正确的 media 目录相对路径
                local_path = f'media/{os.path.basename(audio_path)}'
                cursor.execute('UPDATE dialect_app_dialectword SET audio_file = ? WHERE id = ?', (local_path, id))

        conn.commit()
        conn.close()

        self.stdout.write(self.style.SUCCESS('成功导入数据，并修正音频文件路径'))
