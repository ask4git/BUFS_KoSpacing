# BUFS_KoSpacing(Ver.0.95)
BUFS_Korean_Spacing_Module  

* 어절 사전과 형태소 사전을 이용한 한국어 띄어쓰기 모듈  
Korean spacing module using Eojeol dictionary and morpheme dictionary  

* 말뭉치에서 추출한 어절과 형태소로 각각의 어절 사전과 형태소 사전을 만들어서 띄어쓰기가 전혀 되어 있지 않은 문자열을 입력받아 사전정보를 이용하여 자동으로 띄어쓰기를 해 주는 모듈

* 0.95 

## Dictionary
+ Corpus
  * 신문 말뭉치 90,237,593어절
  * 현대문어 말뭉치 90,237,593어절
  * 국립국어원 말뭉치 2,150,509어절
+ ### dictionary file
  * [download](https://drive.google.com/open?id=19xpts0_7yF6IucWQtrW9280W7YB61wWV) 204 MB
    - 어절점수
    - 형태소사전
    - 조사사전
    
## Method
```python
import BUFS_KoSpacing as bs
from dictionary import Eojeoldict

d = Eojeoldict(path)
sp = bs.SpacingModule(path)
```
* dictionary.py
```python
d.create_dictionary() # corpus에서 어절을 추출하여 어절사전을 생성하고 .dict와 .txt형태로 저장
d.add_eojeol_data(data_path) # 어절사전에 추가할 파일이 있는 디렉터리의 경로를 입력받아 어절사전에 추가
```
* BUFS_KoSpacing.py
```python
sp.spacing(str()) # string을 입력받아 띄어쓰기가 된 결과를 return
```

## Tag
| tag | meaning |
|---|:---:|
| `/-1` | 문장의 |
| `/0` | 다음 음절과 붙여쓰기 |
| `/1` | 다음 음절과 띄어쓰기 |
| `/2` | 띄어쓰기 붙여쓰기 둘다 허용, testcase본문에는 붙여쓰기 |
| `/3` | 띄어쓰기 붙여쓰기 둘다 허용, testcase본문에는 띄어쓰기 |
* example
  - 나는 바닷바람을 맞으며 콧노래를 흥얼거렸다. 
  - 나/0는/1바/0닷/0바/0람/0을/1맞/0으/0며/1콧/0노/0래/0를/1흥/0얼/0거/0렸/0다/0./0 

## How to use it

```
C:\Users\Username\Desktop\BUFS_KoSpacing>python3 main.py -h
usage: main.py [-h] input

positional arguments:
  input       input file name

optional arguments:
  -h, --help  show this help message and exit
```

1. 어절 사전을 내려받아 프로젝트가 있는 경로에 압축을 풉니다.

1. 프로젝트가 있는 폴더에 입력으로 사용할 text파일을 넣어줍니다.

1. python3 main.py testfile.txt

1. 프로젝트가 있는 폴더에 outpuut.txt파일에 결과가 출력됩니다.

## Accuracy
+ Precision=  (#Number of correct tag)/(#Number of predicted tag)
+ Recall=  (#Number of correct tag)/(#Number of tag)
+ F-measure= 2×(Precision×Recall)/(Precision+Recall)
+ Sentence Accuracy=  (#Number of correct sentence)/(#Number of sentence)

## Accuracy
| Corpus | Precision | Recall | F-measure | Sentence Accuracy |
|---|:---:|:---:|:---:|:---:|
| 신문 말뭉치 |	0.9502	| 0.9032	| 0.9261	| 0.027 |
| 소설 말뭉치	| 0.9421	| 0.8901	| 0.9153	| 0.016 |

