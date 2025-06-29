#TM.py
#contact me: familyerpro@gmail.com
import sys
import tkinter as tk
from tkinter import ttk, font, messagebox
import logging
from ui_manager import UIManager
from pagination import PaginationManager
from data_processor import DataProcessor
from lexicon_manager import load_lexicon
from image_loader import ImageLoader
from deepseek_module import DeepseekProcessor

# 日志配置
logging.basicConfig(
    level=logging.DEBUG,  # 调整日志级别为 INFO
    format='[%(asctime)s] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('tm_operation.log'),
        logging.StreamHandler()
    ]
)

# 调整 PIL 库的日志级别
import PIL
PIL_logger = logging.getLogger('PIL')
PIL_logger.setLevel(logging.INFO)

class ReadingApp:
    def __init__(self):
        # ==== 初始化配置 ====
        self.config = {
            'display_ratios': [1.0, 0.6, 0.4, 0], 
            'text_padding': 10,       # 强制左右边距
            'min_width': 60,
            'line_height': 55,        # 恢复原行高
            'para_space': 16,
            'max_line_width': 1200,
            'page_max_height': 680,
            'img_spacing': 3,         # 图母间距3像素
            'word_spacing': 15,       # 行间距12像素
            'ratio_index': 0
        }

        # ==== 主窗口初始化 ====
        self.root = UIManager.create_base_window("图母阅读器", "1280x720")
        self.custom_font = font.Font(family="Microsoft YaHei", size=14)

        # 确保 config 中包含 'font'
        self.config['font'] = self.custom_font

        # ==== 样式系统初始化 ====
        self._configure_styles()

        # ==== 核心组件 ====
        self.ds_processor = None
        self.image_loader = None
        self.lexicon = None
        self.current_page = 0
        self.pages = []
        self.word_entries = []
        self.processing_in_progress = False

        # ==== 启动流程 ====
        try:
            # 在后台初始化资源
            self._initialize_resources_in_background()
            # 立即显示输入框
            self._show_input_ui()
        except Exception as e:
            self._handle_critical_error("初始化失败", e)

    def _configure_styles(self):
        """全局样式配置（消除灰色方块）"""
        style = ttk.Style()
        style.theme_use('clam')

        # 所有容器强制白底无边框
        style.configure('.', background='white', borderwidth=0)
        style.configure(
            'Main.TFrame', 
            background='white', 
            padding=10
        )
        style.configure(
            'Content.TFrame',
            background='white'
        )
        style.configure(
            'Line.TFrame',
            background='white',
            padding=0
        )
        style.configure(
            'Word.TFrame',
            background='white',
            padding=0
        )
        style.configure(
            'ImgContainer.TFrame',
            background='white'
        )
        style.configure(
            'Text.TFrame',
            background='white'
        )

        # 分隔线样式
        style.configure(
            'VSep.TSeparator',
            background='#E0E0E0',
            width=1
        )

        # 按钮样式
        style.configure(
            'TButton',
            background='#F0F0F0',
            bordercolor='#E0E0E0',
            padding=6
        )

    def _initialize_resources_in_background(self):
        """在后台初始化资源"""
        import threading
        threading.Thread(target=self._initialize_resources, daemon=True).start()

    def _initialize_resources(self):
        """资源加载"""
        logging.info("初始化资源...")
        try:
            self.image_loader = ImageLoader()
            self.lexicon = load_lexicon()
            logging.info(f"词库加载完成，条目数：{len(self.lexicon)}")
        except Exception as e:
            self._handle_error("资源加载失败", e)

    def _show_input_ui(self):
        """显示输入界面"""
        self.clear_window()
        try:
            self.main_frame, self.text_input = UIManager.create_input_ui(
                self.root, 
                self.custom_font,
                self.start_processing
            )

        except Exception as e:
            self._handle_error("界面初始化失败", e)

    def start_processing(self, input_text=None):
        """处理用户输入"""
        lang = UIManager.LANGUAGES[UIManager.current_lang]
        if self.processing_in_progress:
            messagebox.showinfo(lang.get("info_title", "提示"), lang.get("processing", "处理正在进行中，请稍候..."))
            return

        self.processing_in_progress = True

        # 兼容直接传入文本（用于语言切换后的重新创建 UI）
        raw_text = input_text or self.text_input.get("1.0", "end").strip()
        if not raw_text:
            messagebox.showwarning(lang.get("input_error", "输入错误"), lang.get("input_empty", "请输入有效文本"))
            self.processing_in_progress = False
            return

        try:
            self.word_entries = []

            def process_callback(tokens):
                try:
                    self._process_tokens(tokens)
                except Exception as e:
                    self._handle_error(lang.get("data_error", "数据处理异常"), e)

            self.ds_processor = DeepseekProcessor()
            self.ds_processor.async_process(raw_text, process_callback)

        except Exception as e:
            self._handle_error(lang.get("startup_error", "处理启动失败"), e)
            self.processing_in_progress = False

    def _process_tokens(self, tokens):
        """处理分词结果"""
        logging.info(f"处理 {len(tokens)} 个分词...")
        for token in tokens:
            try:
                annotation = token.get('annotation', '')
                word = token.get('word', '')
                if word=='\n':
                    self.word_entries.append({
                        'text': word,
                        'images': None,
                        # 'width': width,
                        'img_names': None,
                        'eng_text': None,
                        'type': 'paragraph_end'
                    })
                    continue
                pos=token.get('pos', '')
                entry = DataProcessor.process_token(annotation,pos, self.lexicon)
                images = []
                img_names=[]
                china=[]
                english,jp,ara,fr,de,pt,spa,ru=[],[],[],[],[],[],[],[]
                lang=UIManager.current_lang
                for entryi in entry:
                    images.extend(entryi.get('images'))
                    img_names.extend(entryi.get('img_names'))
                    if entryi.get('word')=='小隔':
                        continue
                    china.append(entryi.get('word'))
                    english.append(entryi.get('eng_text'))

                    if lang=='jp':
                        jp.append(entryi.get('jp_text'))
                    elif lang=='ara':
                        ara.append(entryi.get('ara_text'))
                    elif lang=='fr':
                        fr.append(entryi.get('fr_text'))
                    elif lang=='de':
                        de.append(entryi.get('de_text'))
                    elif lang=='pt':
                        pt.append(entryi.get('pt_text'))
                    elif lang=='spa':
                        spa.append(entryi.get('spa_text'))
                    elif lang=='ru':
                        ru.append(entryi.get('ru_text'))



                china=''.join(china)
                english=' '.join(english)
                if lang=='jp':
                    jp=' '.join(jp)
                elif lang=='ara':
                    ara=' '.join(ara)
                elif lang=='fr':
                    fr=' '.join(fr)
                elif lang=='de':
                    de=' '.join(de)
                elif lang=='pt':
                    pt=' '.join(pt)
                elif lang=='spa':
                    spa=' '.join(spa)
                elif lang=='ru':
                    ru=' '.join(ru)
                width = DataProcessor.calculate_width(
                    word,
                    images,
                    {
                        'font': self.custom_font,
                        'text_padding': self.config['text_padding'],
                        'img_spacing': self.config['img_spacing'],
                        'min_width': self.config['min_width']
                    }
                )
                self.word_entries.append({
                    'text': word,
                    'images': images,
                    'width': width,
                    'img_names':img_names,
                    'china':china,
                    'english':english,
                    'jp_text':jp,
                    'ara_text':ara,
                    'fr_text':fr,
                    'de_text':de,
                    'pt_text':pt,
                    'spa_text':spa,
                    'ru_text':ru,
                    'type': 'word'
                })
            except Exception as e:
                logging.error(f"词条处理失败: {str(e)}")

        self._finalize_processing()

    def _finalize_processing(self):
        """生成分页数据"""
        try:
            if not self.word_entries:
                messagebox.showinfo("处理完成", "未生成任何内容")
                self.processing_in_progress = False
                return

            self.word_entries.append({'type': 'paragraph_end'})
            self.pages = PaginationManager.paginate_content(
                self.word_entries, 
                self.config
            )
            logging.info(f"生成 {len(self.pages)} 页内容")
            self._show_reading_ui()
            self.processing_in_progress = False
        except Exception as e:
            self._handle_error("分页失败", e)
            self.processing_in_progress = False

    def _show_reading_ui(self):
        """显示阅读界面"""
        self.clear_window()
        try:
            control_frame = UIManager.create_control_buttons(
                self.root,
                self.config['display_ratios'],
                self.config['ratio_index'],
                self._set_display_ratio,
                self._change_page,
                self._show_input_ui
            )
            control_frame.pack(pady=10, fill='x')
            self.show_page(0)
        except Exception as e:
            self._handle_error("界面渲染失败", e)

    def show_page(self, page_num):
        try:
            PaginationManager.render_page(self, page_num, self.pages, self.config)
        except Exception as e:
            self._handle_error("渲染失败", e)

    # ==== 核心功能 ====
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def _change_page(self, delta):
        new_page = self.current_page + delta
        if 0 <= new_page < len(self.pages):
            self.current_page = new_page
            self.show_page(new_page)

    def _set_display_ratio(self, ratio_value):
        try:
            self.config['ratio_index'] = self.config['display_ratios'].index(ratio_value)
            self.show_page(self.current_page)
        except ValueError:
            logging.error(f"无效比例值: {ratio_value}")

    # ==== 错误处理 ====
    def _handle_error(self, title, error):
        logging.error(f"{title}: {str(error)}")
        messagebox.showerror(title, str(error))
        self.processing_in_progress = False

    def _handle_critical_error(self, title, error):
        logging.critical(f"{title}: {str(error)}")
        messagebox.showerror(title, f"致命错误: {str(error)}\n程序即将退出")
        sys.exit(1)

if __name__ == "__main__":
    try:
        app = ReadingApp()
        app.root.mainloop()
    except Exception as e:
        messagebox.showerror("崩溃", f"未处理异常: {str(e)}")


