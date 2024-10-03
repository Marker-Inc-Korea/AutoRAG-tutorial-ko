import os

import click
from dotenv import load_dotenv

from autorag.chunker import Chunker

root_dir = os.path.dirname(os.path.realpath(__file__))


@click.command()
@click.option('--raw_path', type=click.Path(exists=True, dir_okay=False, file_okay=True),
			  default=os.path.join(root_dir, "parsed_raw", "0", "5.parquet"))
@click.option('--config', type=click.Path(exists=True, dir_okay=False), default=os.path.join(root_dir, "config", "chunk.yaml"))
@click.option('--project_dir', type=click.Path(dir_okay=True), default=os.path.join(root_dir, "chunked_corpus"))
def main(raw_path, config, project_dir):
	load_dotenv()

	if not os.path.exists(project_dir):
		os.makedirs(project_dir)

	parser = Chunker.from_parquet(raw_path, project_dir=project_dir)
	parser.start_chunking(config)


if __name__ == '__main__':
	main()
