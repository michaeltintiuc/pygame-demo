# pygame-demo
:video_game: A demo platformer in python


#### Requirements
* python 2.7.*
* pygame 1.9.*
* pyinstaller 3.6

```python
pip2 installer -r requireents.txt
```

Generating a binary requires pyinstaller@3.6 which has a bug: https://github.com/pyinstaller/pyinstaller/issues/5540
and requires a change in `depend/utils.py` around line 400 `if m is None: continue`

#### Run
```
cd /path/to/game
python2 .
```
