import numpy as np

from Baidu_Text_transAPI import createRequest
from image_loader import ImageLoader

import pandas as pd
import os, time, sys
from concurrent.futures import ThreadPoolExecutor
from tkinter import messagebox

def load_lexicon():
    try:
        s_time = time.time()
        # == 使用 pandas 加载 Excel 文件 ==
        df = pd.read_csv('KU.csv', encoding='utf-8',low_memory=False)
        print(f"加载词库耗时: {time.time() - s_time:.2f}s")
        df.columns = df.columns.str.strip()

        # == 验证必要列 ==
        required_columns = ['ID', '词', '图', '词性', 'NUM', 'explain']
        missing_columns = list(set(required_columns) - set(df.columns))
        if missing_columns:
            raise ValueError(f"词库文件缺失必要列: {', '.join(missing_columns)}")

        # == 数据预处理 ==
        df['NUM'] = pd.to_numeric(df['NUM'], errors='coerce').fillna(9999).astype(int)
        df['词性'] = df['词性'].fillna('').str.upper().str.strip()
        df['图'] = df['图'].fillna('')
        df['eng_text'] = df.get('eng_text', '').fillna('')
        image_loader = ImageLoader()  # 初始化图片加载器
        lexicon = {}

        def process_row(row):
            word = str(row.词)
            image_names = str(row.图).split(',')
            image_paths = [f"TU/{img.strip()}.png" for img in image_names if img.strip()]
            images = image_loader.load_silent(image_paths)

            return word, {
                'word': word,
                'pos': row.词性,
                'images': images,
                'id': str(row.ID).strip(),
                'num': row.NUM,
                'img_names': image_names,
                'explain': str(row.explain).strip(),
                'eng_text': str(row.eng_text).strip(),
                'jp_text': str(row.jp_text).strip(),
                'ara_text': str(row.ara_text).strip(),
                'fr_text': str(row.fr_text).strip(),
                'de_text': str(row.de_text).strip(),
                'pt_text': str(row.pt_text).strip(),
                'spa_text': str(row.spa_text).strip(),
                'ru_text': str(row.ru_text).strip(),
            }

        # == 并行处理行数据和加载图像 ==
        s_time = time.time()

        # with ThreadPoolExecutor(max_workers=8) as executor:
        #     results = list(executor.map(process_row, df.itertuples(index=False)))
        #
        # for word, entry in results:
        #     lexicon.setdefault(word, []).append(entry)

        with ThreadPoolExecutor(max_workers=8) as executor:
            for word, entry in executor.map(process_row, df.itertuples(index=False)):
                lexicon.setdefault(word, []).append(entry)
        print(f"处理库耗时: {time.time() - s_time:.2f}s")

        return lexicon

    except FileNotFoundError:
        messagebox.showerror("文件错误", "未找到 KU.xlsx 文件")
        sys.exit(1)
    except Exception as e:
        messagebox.showerror("词库错误", f"加载词库失败: {str(e)}")
        sys.exit(1)
if __name__ == '__main__':
    df=pd.read_excel('wt.xlsx')
    df.to_csv('KU.csv', index=False)
# applist=[]
# sol=[]
# for i in range(18495,len(df['词']),1000):
#     if i+1000>len(df['词']):
#         sol_i=df['词'][i:].apply(str).tolist()
#     else:
#         sol_i=df['词'][i:i+1000].apply(str).tolist()
#     print(i)
#     sol.extend(createRequest('\n'.join(sol_i),'zh','en'))
#     pd.DataFrame(sol).to_csv('KU2.csv', index=False)
# df['jp_text']=np.array(sol)
# df.to_excel('KU1.xlsx', index=False)
