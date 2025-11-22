# -*- coding: utf-8 -*-
from wordcloud import WordCloud
from konlpy.tag import Okt
from collections import Counter
import matplotlib.pyplot as plt
import platform
import numpy as np
from PIL import Image

# ---------------------------------------
# 1) 파일 읽기
# ---------------------------------------
file_path = "./seoul_foreign_company_benefits_url_map.text"  # 같은 폴더에 두었을 경우
with open(file_path, encoding="utf-8") as f:
    text = f.read()

# ---------------------------------------
# 2) 형태소 분석 → 명사/형용사만 추출
# ---------------------------------------
okt = Okt()
sentences_tag = okt.pos(text)
tokens = [word for word, tag in sentences_tag if tag in ["Noun", "Adjective"]]

# 빈도 계산 (상위 50개)
counts = Counter(tokens)
tags = counts.most_common(50)
print(tags)

# ---------------------------------------
# 3) 한글 폰트 설정
# ---------------------------------------
if platform.system() == "Windows":
    font_path = r"c:\windows\Fonts\malgun.ttf"
elif platform.system() == "Darwin":  # Mac
    font_path = r"/System/Library/Fonts/AppleGothic.ttf"
else:
    font_path = r"/usr/share/fonts/truetype/nanum/NanumGothic.ttf"

# ---------------------------------------
# 4) 마스크 이미지 (책 모양)
# ---------------------------------------
mask_arr = np.array(Image.open("./book.png"))

# ---------------------------------------
# 5) 워드클라우드 생성
# ---------------------------------------
wc = WordCloud(
    font_path=font_path,
    width=800,
    height=800,
    background_color="white",
    max_font_size=220,
    repeat=True,
    colormap="inferno",
    mask=mask_arr,
)

cloud = wc.generate_from_frequencies(dict(tags))
cloud.to_file("seoul_foreign_company_wordcloud.png")  # 책 모양으로 저장
print("[완료] seoul_foreign_company_wordcloud.png 저장됨")

plt.figure(figsize=(10, 8))
plt.axis("off")
plt.imshow(cloud, interpolation="bilinear")
plt.show()
