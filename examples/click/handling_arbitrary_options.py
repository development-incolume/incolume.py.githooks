"""Exemplo.

Manipulação de opçoes arbitrarias.
"""
import click

@click.command(context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.pass_context
def cli(ctx):
    # Parse extra args into a dictionary
    # Assumes pairs like --key value
    kwargs = {}
    args = ctx.args
    i = 0
    while i < len(args):
        key = args[i]
        if key.startswith('--'):
            key = key[2:] # Remove --
            if i + 1 < len(args) and not args[i+1].startswith('--'):
                kwargs[key] = args[i+1]
                i += 2
            else:
                kwargs[key] = True # Boolean flag
                i += 1
        else:
            i += 1
    
    click.echo(f"Captured kwargs: {kwargs}")

if __name__ == '__main__':
    cli()   
