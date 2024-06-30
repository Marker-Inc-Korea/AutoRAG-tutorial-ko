import os

import click
import pandas as pd
from dotenv import load_dotenv

from llama_index.llms.openai import OpenAI
from autorag.data.qacreation import generate_qa_llama_index, make_single_content_qa

root_path = os.path.dirname(os.path.realpath(__file__))
prompt = """다음은 걸그룹 뉴진스에 관한 기사입니다. 
기사를 보고 할 만한 질문을 만드세요.
반드시 뉴진스와 관련한 질문이어야 합니다.
만약 주어진 기사 내용이 뉴진스와 관련되지 않았다면, 
'뉴진스와 관련 없습니다.'라고 질문을 만드세요.

기사:
{{text}}

생성할 질문 개수: {{num_questions}}

예시:
[Q]: 뉴진스는 몇 명인가요?
[A]: 뉴진스는 총 다섯 명입니다.

뉴진스와 관련이 없는 기사일 경우 예시:
[Q]: 뉴진스와 관련 없습니다.
[A]: 뉴진스와 관련 없습니다.

결과:
"""


@click.command()
@click.option('--corpus_path', type=click.Path(exists=True),
              default=os.path.join('data', 'corpus_new.parquet'))
@click.option('--save_path', type=click.Path(exists=False, dir_okay=False, file_okay=True),
              default=os.path.join('data', 'qa_new.parquet'))
@click.option('--qa_size', type=int, default=5)
def main(corpus_path, save_path, qa_size):
    load_dotenv()

    corpus_df = pd.read_parquet(corpus_path, engine='pyarrow')
    llm = OpenAI(model='gpt-4o', temperature=0.5)
    qa_df = make_single_content_qa(corpus_df, content_size=qa_size, qa_creation_func=generate_qa_llama_index,
                                   llm=llm, prompt=prompt, question_num_per_content=1)
    # delete if the output question is '뉴진스와 관련 없습니다'
    qa_df = qa_df.loc[~qa_df['query'].str.contains('뉴진스와 관련 없습니다')]
    qa_df.reset_index(drop=True, inplace=True)
    qa_df.to_parquet(save_path)


if __name__ == '__main__':
    main()
