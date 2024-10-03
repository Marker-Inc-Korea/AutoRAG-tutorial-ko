import click
import os

import pandas as pd
from autorag.data.qa.filter.dontknow import dontknow_filter_rule_based
from autorag.data.qa.generation_gt.llama_index_gen_gt import (
	make_basic_gen_gt,
	make_concise_gen_gt,
)
from autorag.data.qa.query.llama_gen_query import factoid_query_gen
from autorag.data.qa.sample import random_single_hop
from autorag.data.qa.schema import Raw, Corpus
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI

root_dir = os.path.dirname(os.path.realpath(__file__))


@click.command()
@click.option("--corpus_path", type=click.Path(exists=True), help="Path to the corpus. Must be parquet file.",
			  required=True, default=os.path.join(root_dir, "chunked_corpus", "0", "3.parquet"))
@click.option("--raw_path", type=click.Path(exists=True), help="Path to the raw data. Must be parquet file.",
			  required=True, default=os.path.join(root_dir, "parsed_raw", "0", "5.parquet"))
@click.option("--qa_size", type=int, help="Number of QA pairs to generate.", default=20)
@click.option("--output_path", type=click.Path(), help="Path to save the generated QA pairs. Must be parquet file.",
			  required=True,
			  default=os.path.join(root_dir, "data", "generated_qa.parquet"))
@click.option("--corpus_output_path", type=click.Path(),
			  default=os.path.join(root_dir, "data", "generated_corpus.parquet"))
def main(corpus_path, raw_path, qa_size, output_path, corpus_output_path):
	load_dotenv()

	for path in [corpus_path, raw_path, output_path, corpus_output_path]:
		if not path.endswith(".parquet"):
			raise ValueError(f"Path {path} must be a parquet file.")

	llm = OpenAI(model="gpt-4o-2024-08-06")

	initial_raw = Raw(pd.read_parquet(raw_path, engine="pyarrow"))
	initial_corpus = Corpus(pd.read_parquet(corpus_path, engine="pyarrow"), initial_raw)
	qa = initial_corpus.sample(random_single_hop, n=qa_size).map(
			lambda df: df.reset_index(drop=True),
		).make_retrieval_gt_contents().batch_apply(
			factoid_query_gen,  # query generation
			llm=llm,
			lang="ko",
		).batch_apply(
			make_basic_gen_gt,  # answer generation (basic)
			llm=llm,
			lang="ko",
		).batch_apply(
			make_concise_gen_gt,  # answer generation (concise)
			llm=llm,
			lang="ko",
		).filter(
			dontknow_filter_rule_based,  # filter unanswerable questions
			lang="ko",
		)

	qa.to_parquet(output_path, corpus_output_path)


if __name__ == "__main__":
	main()
