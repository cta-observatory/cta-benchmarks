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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("directory")
    parser.add_argument("--header")
    args = parser.parse_args()
    fnames = [fname for fname in sorted(os.listdir(args.directory))
              if fname not in EXCLUDED and fname.endswith('.html')]
    header = (args.header if args.header else os.path.basename(args.directory))
    template = Template(INDEX_TEMPLATE).render(names=fnames, header=header)
    os.makedirs('docs', exist_ok=True)
    with open('docs/index.html', 'w') as file:
        file.write(template)
    print(template)


if __name__ == '__main__':
    main()