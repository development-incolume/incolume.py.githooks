# how to pass options by context in click Python

To pass options by context in **Python Click**, use the **`@click.pass_context`** decorator to inject the context object into your command function, allowing you to store and retrieve values via **`ctx.obj`** or **`ctx.params`**.

**Method 1: Using `ctx.obj` for Shared State**
Store shared configuration in the context object at the group level and retrieve it in subcommands.

```python
import click

@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    # Store shared options in the context object
    ctx.ensure_object(dict)
    ctx.obj['DEBUG'] = debug

@cli.command()
@click.pass_context
def sync(ctx):
    # Access the stored option
    if ctx.obj['DEBUG']:
        click.echo("Debug mode is on")
    click.echo("Syncing data...")

if __name__ == '__main__':
    cli()
```

**Method 2: Using `ctx.params` for Direct Access**
Access command-line arguments directly from the context’s `params` dictionary.

```python
import click

@click.command()
@click.option('--name', default='World')
@click.pass_context
def hello(ctx):
    # Access option value via context
    name = ctx.params['name']
    click.echo(f"Hello, {name}!")

if __name__ == '__main__':
    hello()
```

**Key Points:**
*   **`@click.pass_context`** is required to make the context available as the first argument (`ctx`) in your function.
*   **`ctx.obj`** is ideal for passing complex objects or shared configuration between commands.
*   **`ctx.params`** provides a dictionary of all options and arguments for the current command.
*   Use **`ctx.ensure_object(dict)`** to safely initialize `ctx.obj` if it hasn't been set yet.
