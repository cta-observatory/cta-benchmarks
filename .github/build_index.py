""" Build index from directory listing

make_index.py </path/to/directory> [--header <header text>]
"""

INDEX_TEMPLATE = r"""
<html>
<body>
<h2>${header}</h2>
<p>
% for name in names:
    <li><a href="${name}">${name}</a></li>
% endfor
</p>
</body>
</html>
"""

EXCLUDED = ['index.html']

import os
import argparse
from mako.template import Template


default_header = '<header class="page-header"> \
<link rel="stylesheet" href="default.css"> \
<h1>CTA Benchmarks</h1> \
Pages produced by the continuous integration and notebooks in \
<a href="https://github.com/cta-observatory/cta-benchmarks"> cta-benchmarks</a> <br> <br> \
<main> \
List of benchmarks: \
</main> \
</header>'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--header")
    args = parser.parse_args()
    fnames = [fname for fname in sorted(os.listdir(args.directory))
              if fname not in EXCLUDED and fname.endswith('.html')]
    header = (args.header if args.header else default_header)
    template = Template(INDEX_TEMPLATE).render(names=fnames, header=header)
    os.makedirs('docs', exist_ok=True)
    with open('docs/index.html', 'w') as file:
        file.write(template)

if __name__ == '__main__':
    main()