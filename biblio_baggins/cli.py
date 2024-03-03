import click
from .commands import paperadd

@click.command()
@click.option('--paper-add', '-a', is_flag=True, help="Add paper from clipboard")

def main(paper_add):
    if paper_add:
        paperadd()

if __name__ == '__main__':
    main()
