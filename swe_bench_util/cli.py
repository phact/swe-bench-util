"""This module provides the CLI."""

from typing import Optional
import json
import sys

import typer

from swe_bench_util import __app_name__, __version__

from datasets import load_dataset

app = typer.Typer()

def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


def write_file(path, text):
    with open(path, 'w') as f:
        f.write(text)
        print(f"File '{path}' was saved", file=sys.stderr)

def write_json(path, name, data):
    json_str = json.dumps(data, indent=2)
    json_path = f"{path}/{name}.json"
    write_file(json_path, json_str)

def format_markdown_code_block(text):
    text = text.replace('```', '\\`\\`\\`')
    return f"```\n{text}\n```"

def write_markdown(path, name, data):
    template_fields = [
        "instance_id"
        "repo",
        "base_commit",
        "problem_statement"
    ]
    text = f"""# {data['instance_id']}

* repo: {data['repo']}
* base_commit: {data['base_commit']}

## problem_statement
{data['problem_statement']}
"""
    for k, v in data.items():
        if k not in template_fields:
            text += f"""## {k}\n{format_markdown_code_block(v)}\n\n"""
    md_path = f"{path}/{name}.md"
    write_file(md_path, text)

@app.command()
def get(index:int=0, split: str='dev', dataset_name='princeton-nlp/SWE-bench'):
    dataset = load_dataset(dataset_name, split=split)
    row_data = dataset[index]
    id = row_data['instance_id']
    write_json('rows', f"{id}", row_data)
    write_markdown('rows', f"{id}", row_data)
    
    


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return