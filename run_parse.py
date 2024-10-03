import os

from autorag.parser import Parser
import click
from dotenv import load_dotenv

root_dir = os.path.dirname(os.path.realpath(__file__))


@click.command()
@click.option('--data_path_glob', type=click.Path(exists=False, dir_okay=True),
			  default=os.path.join(root_dir, "raw_docs", "*.pdf"))
@click.option('--config', type=click.Path(exists=True, dir_okay=False), default=os.path.join(root_dir, "config", "parse.yaml"))
@click.option('--project_dir', type=click.Path(dir_okay=True), default=os.path.join(root_dir, "parsed_raw"))
def main(data_path_glob, config, project_dir):
	load_dotenv()

	if not os.path.exists(project_dir):
		os.makedirs(project_dir)

	parser = Parser(data_path_glob=data_path_glob, project_dir=project_dir)
	parser.start_parsing(config)


if __name__ == '__main__':
	main()
