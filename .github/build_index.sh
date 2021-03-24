pip install mako

cp BUILD/Preparation/*.html docs/
cp BUILD/Benchmarks/*/*.html docs/
cp BUILD/Summaries/*.html docs/
python .github/build_index.py docs