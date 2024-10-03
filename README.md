# AutoRAG 한국어 튜토리얼
AutoRAG 한국어 튜토리얼을 위한 레포입니다. 
이 레포에서는 아주 간단한 데이터를 통해서 AutoRAG를 실행해 볼 수 있습니다.

# 유튜브 영상
해당 레포를 이용한 튜토리얼 영상입니다.

[![Video Label](https://i3.ytimg.com/vi/rA5SoBXB8R4/maxresdefault.jpg)](https://youtu.be/rA5SoBXB8R4?si=kbr9hTDUpPQUiiaN)


# 설치

```bash
pip install -r requirements.txt
```

위를 실행하면 자동으로 AutoRAG가 설치됩니다.

먼저, OPENAI_API_KEY 환경 변수를 직접 설정하거나 `.env` 파일을 생성하여 그 안에 기입하세요.

# RAG 평가 데이터셋 제작 튜토리얼

AutoRAG 사용을 위하여 먼저 RAG 평가 데이터셋을 제작해야 합니다. 아래 과정을 통해 직접 데이터셋을 제작하고 사용해보세요.

1. `raw_docs`에서 원본 문서를 확인합니다. 이 튜토리얼에서는 세 개의 pdf 문서를 이용하고자 합니다.
2. `run_parse.py`를 실행합니다. 이 파일을 통해서 `config/parse.yaml`에 기입된 방법들을 통해 파싱을 실행하고, 그 결과를 비교할 수 있습니다. 
```bash
python make_parse.py 
```
3. `parsed_raw` 폴더 내에 생성된 trial 폴더 (숫자 폴더) 내에서 여러 parquet 파일들을 확인할 수 있습니다. 이것들이 파싱된 결과입니다. `pandas`를 통해 load하여 직접 확인해보세요.
4. `run_chunk.py`를 실행하여 여러 방법으로 청킹을 수행합니다. `config/chunk.yaml`에서 청킹 방법들을 확인할 수 있습니다. 이 때 raw 파일을 설정해야 합니다.
```bash
python run_chunk.py --raw_path ./parsed_row/0/5.parquet
```
5. 실행 이후, 여러 가지 청크 방법을 통해 잘려진 여러 청킹 파일들을 `chunked_corpus` 폴더에서 확인해 보세요.
6. 이제 `make_qa.py` 파일을 실행합니다. chunk를 생성할 때 사용한 raw 파일과, 사용할 chunk 파일을 설정해야 합니다.
해당 chunk 파일은 적당한 것을 선택하면 되며, 추후 다른 chunk 파일들을 통해서도 QA 데이터셋을 생성할 수 있습니다.
이 때 다시 질문을 생성하지 않아도 괜찮습니다. 추후 설명한 update_corpus 기능을 참고하세요.
```bash
python make_qa.py --raw_path ./parsed_raw/0/5.parquet --chunk_path ./chunked_corpus/0/3.parquet --qa_size 20
```
7. `data` 폴더에 생성된 `generated_qa.parquet` 파일과 `generated_corpus.parquet` 파일을 확인하세요.

# 프로젝트 구동
## main.py 이용

1. `.env.template` 파일을 복사하여 `.env` 파일을 만들고 저장합니다. 반드시 본인의 OpenAI api key를 이 파일에 적어주세요.
2. 아래처럼 main.py를 실행하여 AutoRAG를 구동하세요.
```bash
python3 main.py --config ./config/tutorial_ko.yaml
```
3. benchmark 폴더가 생성되면 거기서 결과를 확인할 수 있습니다.

## cli 이용

1. `benchmark` 폴더를 만들어 줍니다.
2. `OPENAI_API_KEY`를 환경변수로 설정합니다. `export OPENAI_API_KEY=sk-xxxx` 
3. 아래 cli 명령을 실행하여 AutoRAG 최적화를 시작합니다.
```bash
autorag evaluate --qa_data_path ./data/qa.parquet --corpus_data_path ./data/corpus.parquet \
  --config ./config/tutorial_ko.yaml --project_dir ./benchmark
```
위 데이터셋 튜토리얼에서 제작한 데이터셋으로 실행하려면, 
`corpus.parquet`을 `corpus_new.parquet`, `qa.parquet`을 `qa_new.parquet`으로 바꿔주세요.
4. benchmark 폴더가 생성되면 거기서 결과를 확인할 수 있습니다.

## 대시보드 실행

아래 명령을 실행하여 대시보드를 로드합니다. 대시보드를 통해 결과를 아주 쉽게 검토할 수 있습니다.

```bash
autorag dashboard --trial_dir ./benchmark/0
```

## streamlit 실행
streamlit을 실행하여 직접 최적화된 RAG를 사용해 볼 수 있습니다. 
아래 명령을 실행하세요.

```bash
autorag run_web --trial_path ./benchmark/0
```

## update corpus

이 기능을 통하여 같은 raw file을 쓰고 있는 chunk corpus들을 기준으로 새로운 QA 파일들을 생성할 수 있습니다. 

아래와 같이 해보세요.

```python
from autorag.data.qa.schema import Raw, Corpus, QA

raw = Raw(initial_raw_df)
corpus = Corpus(initial_corpus_df, raw)
qa = QA(initial_qa_df, corpus)

new_qa = qa.update_corpus(Corpus(new_corpus_df, raw))
```

### 이런 질문을 해보세요.
- 야후가 NFL 팬을 위해 도입한 기능은 뭐야?
- 핀테크 혁신 투자로 기업이 성장한 회사들은 어디가 있어?
- 부동산 대출 연체가 늘어나면 어떻게 되나요?
