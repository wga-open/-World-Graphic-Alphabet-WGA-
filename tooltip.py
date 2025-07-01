# tooltip.py
import logging
import tkinter as tk


class Tooltip:
    def __init__(self, widget, text, position='below'):
        self.widget = widget
        self.text =self.format_text( text)
        self.tooltip_window = None
        self.position = position  # 'above' 或 'below'

        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def format_text(self, text):
        # 把中英文逗号替换成换行
        # sptext = text.split('\n')
        # lang=  UIManager.current_lang
        # try:
        #     if lang=='zh':
        #         if sptext[1]=='' or 'nan' in sptext[1]:
        #             en = createRequest(sptext[1], 'zh', 'ru')[0]
        #             text=  sptext[0]+'\n'+en
        #     elif lang=='en':
        #         if sptext[0]=='' or 'nan' in sptext[0]:
        #             en = createRequest(sptext[0], 'ru', 'zh')[0]
        #             text=  en+'\n'+sptext[1]
        #     else:
        #         if self.position=='below':
        #             if sptext[0] == '' or 'nan' in sptext[0]:
        #                 zh = createRequest(sptext[0], lang, 'zh')[0]
        #                 text=  sptext[0]+'\n'+zh
        #
        #
        # except Exception as e:
        #     logging.error(e)

        if isinstance(text, list):
            text = '\n'.join(text)
        return text

    def show_tooltip(self, event=None):
        if self.tooltip_window or not self.text:
            return

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # 无边框
        tw.attributes("-topmost", True)

        font = ("Microsoft YaHei", 10)

        # 创建 Canvas 测量文本宽度
        temp_canvas = tk.Canvas(tw)
        text_font = (font[0], font[1])

        # 目标宽度 (大约15个汉字的像素宽度)，每个中文大概是 10-12pt 字体下 20像素
        target_width = 15 * 20  # 15个汉字*20px = 300px 左右

        # 动态计算 wraplength
        wraplength = target_width

        # 创建最终的 Label
        label = tk.Label(
            tw,
            text=self.text,
            background="#FFFFE0",
            relief='solid',
            borderwidth=1,
            font=text_font,
            justify='left',
            anchor='w',
            wraplength=wraplength  # 这里控制「显示宽度自动换行」
        )
        label.pack(ipadx=5, ipady=2)

        # 更新以获得真实大小
        label.update_idletasks()
        label_width = label.winfo_reqwidth()
        label_height = label.winfo_reqheight()

        # 定位
        widget_x = self.widget.winfo_rootx()
        widget_y = self.widget.winfo_rooty()
        widget_width = self.widget.winfo_width()
        widget_height = self.widget.winfo_height()

        if self.position == 'above':
            x = widget_x + 20
            y = widget_y - label_height - 5
        else:  # 'below'
            x = widget_x + widget_width
            y = widget_y + widget_height + 5

        tw.wm_geometry(f"+{x}+{y}")

    def hide_tooltip(self, event=None):
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

