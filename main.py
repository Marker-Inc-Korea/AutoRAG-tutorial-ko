import os

import click
from autorag.evaluator import Evaluator
from dotenv import load_dotenv

root_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(root_path, 'data')


@click.command()
@click.option('--config', type=click.Path(exists=True))
@click.option('--qa_data_path', type=click.Path(exists=True), default=os.path.join(data_path, 'qa.parquet'))
@click.option('--corpus_data_path', type=click.Path(exists=True), default=os.path.join(data_path, 'corpus.parquet'))
@click.option('--project_dir', type=click.Path(exists=False), default=os.path.join(root_path, 'benchmark'))
def main(config, qa_data_path, corpus_data_path, project_dir):
    load_dotenv()
    if os.getenv('OPENAI_API_KEY') is None:
        raise ValueError('OPENAI_API_KEY environment variable is not set')
    if not os.path.exists(project_dir):
        os.makedirs(project_dir)
    evaluator = Evaluator(qa_data_path, corpus_data_path, project_dir=project_dir)
    evaluator.start_trial(config)


if __name__ == '__main__':
    main()
