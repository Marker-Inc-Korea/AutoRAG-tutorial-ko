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
4. benchmark 폴더가 생성되면 거기서 결과를 확인할 수 있습니다.

# 대시보드 실행

아래 명령을 실행하여 대시보드를 로드합니다. 대시보드를 통해 결과를 아주 쉽게 검토할 수 있습니다.

```bash
autorag dashboard --trial_dir ./benchmark/0
```

# streamlit 실행
streamlit을 실행하여 직접 최적화된 RAG를 사용해 볼 수 있습니다. 
아래 명령을 실행하세요.

```bash
autorag run_web --trial_path ./benchmark/0
```

### 이런 질문을 해보세요.
- 야후가 NFL 팬을 위해 도입한 기능은 뭐야?
- 핀테크 혁신 투자로 기업이 성장한 회사들은 어디가 있어?
- 부동산 대출 연체가 늘어나면 어떻게 되나요?
