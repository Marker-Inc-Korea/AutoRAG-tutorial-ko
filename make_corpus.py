import os

import click
from autorag.utils import cast_corpus_dataset
from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import TokenTextSplitter
from autorag.data.corpus import llama_text_node_to_parquet

root_dir = os.path.dirname(os.path.realpath(__file__))


@click.command()
@click.option('--dir_path', type=click.Path(exists=True, dir_okay=True, file_okay=False),
              default=os.path.join(root_dir, 'raw_docs'))
@click.option('--save_path', type=click.Path(exists=False, dir_okay=False, file_okay=True),
              default=os.path.join(root_dir, 'data', 'corpus_new.parquet'))
def main(dir_path: str, save_path: str):
    if not save_path.endswith('.parquet'):
        raise ValueError('The input save_path did not end with .parquet.')
    documents = SimpleDirectoryReader(dir_path, recursive=True).load_data()
    nodes = TokenTextSplitter().get_nodes_from_documents(documents=documents, chunk_size=256, chunk_overlap=64)
    corpus_df = llama_text_node_to_parquet(nodes)
    corpus_df = cast_corpus_dataset(corpus_df)
    corpus_df.to_parquet(save_path)


if __name__ == '__main__':
    main()
