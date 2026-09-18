# wordcount

A small command-line tool inspired by Unix `wc`: it counts lines, words and
characters of files (or standard input). Built with Python and Typer.

## Installation

Create a virtual environment and install the package with its development
dependencies:

```bash
python3 -m venv .venv
.venv/bin/pip install -e ".[dev]"
```

## Usage

Without options it counts lines, words and characters, like `wc`:

```bash
.venv/bin/wordcount loremipsum.txt
```

Count lines only:

```bash
.venv/bin/wordcount -l loremipsum.txt
```

Count words only:

```bash
.venv/bin/wordcount -w loremipsum.txt
```

Count characters only:

```bash
.venv/bin/wordcount -c loremipsum.txt
```

Count several metrics at once (flags can be combined):

```bash
.venv/bin/wordcount -lw loremipsum.txt
.venv/bin/wordcount loremipsum.txt loremipsum.txt
```

Read from standard input with `-` or with no file argument:

```bash
cat loremipsum.txt | .venv/bin/wordcount -
cat loremipsum.txt | .venv/bin/wordcount
```

## Running the tests

```bash
.venv/bin/python -m pytest
```

Coverage is measured with `pytest-cov` and must stay at or above 90%.

## Reflexiones
- ¿Qué información perdió el agente al comenzar una nueva sesión?
Entiendo que pierde el contexto.
- ¿Qué decisiones tomaste junto con el agente?
Creo que pocas, ya que todo estaba explicado en los ficheros md.
- ¿Qué utilidad tuvo el modo de planificación?
Que no caambia nada, sino que evalua el cambio. De hecho, si pides implementarlo, te obliga a cambiar a modo Build.
- ¿Qué aportó el análisis de cobertura?
Estudia la relacion entre el codigo y los test. Por ejemplo, una cobertura 100% significan que los tests evaluan todo el codigo. 