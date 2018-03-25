# codding=UTF-8
import jieba  # 分词库
from wordcloud import WordCloud, ImageColorGenerator  # 词云库
import codecs
from PIL import Image
import numpy as np
import os


class RockWordCloud():
    def __init__(self, word_file, font_path, save_file_path):
        self.font_path = font_path
        self.word_file = word_file
        self.save_file_path = save_file_path

    def build_image_from_word(self):
        text = codecs.open(self.word_file, 'r', encoding='utf-8').read()
        # 2、结巴分词，默认精确模式。可以添加自定义词典userdict.txt,然后jieba.load_userdict(file_name) ,file_name为文件类对象或自定义词典的路径
        # 自定义词典格式和默认词库dict.txt一样，一个词占一行：每一行分三部分：词语、词频（可省略）、词性（可省略），用空格隔开，顺序不可颠倒
        # 结巴分词:cut_all参数可选, True为全模式，False为精确模式,默认精确模式
        cut_text = jieba.cut(text, cut_all=False)
        result = "/".join(cut_text)  # 必须给个符号分隔开分词结果来形成字符串,否则不能绘制词云
        # print(result)

        # 3、生成词云图，这里需要注意的是WordCloud默认不支持中文，所以这里需已下载好的中文字库
        # 无自定义背景图：需要指定生成词云图的像素大小，默认背景颜色为黑色,统一文字颜色：mode='RGBA'和colormap='pink'
        wc = WordCloud(font_path=self.font_path,
                       background_color='white', width=800, height=600,
                       max_font_size=50,
                       max_words=1000)  # ,min_font_size=10)#,mode='RGBA',colormap='pink')
        wc.generate(result)
        wc.to_file(self.save_file_path + r"/wordcloud.png")  # 按照设置的像素宽高度保存绘制好的词云图，比下面程序显示更清晰

    def build_backgroud_image(self, back_image_file):
        text = codecs.open(self.word_file, 'r', encoding='utf-8').read()
        cut_text = jieba.cut(text)
        result = "/".join(cut_text)  # 必须给个符号分隔开分词结果来形成字符串,否则不能绘制词云

        # 3、初始化自定义背景图片
        image = Image.open(back_image_file)
        graph = np.array(image)

        wc = WordCloud(font_path=self.font_path,
                       background_color='white', width=800, height=600,
                       max_font_size=50,
                       max_words=1000,
                       mask=graph)  # ,min_font_size=10)#,mode='RGBA',colormap='pink')
        wc.generate(result)
        # 5、绘制文字的颜色以背景图颜色为参考
        image_color = ImageColorGenerator(graph)  # 从背景图片生成颜色值
        wc.recolor(color_func=image_color)
        module_path = os.path.splitext(back_image_file)[0]
        back_image_name = os.path.basename(module_path)
        save_file_path = self.save_file_path + "/wc_" + back_image_name + ".png"
        wc.to_file(save_file_path)
        return save_file_path
