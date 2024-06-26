I sure could make an image input handler in the future, but currently, here's how you use the tentai show puzzle generator:
```
██ = white square
░░ = black square
Pretend this is the pattern you'd like to generate —
██████░░██
░░██████░░
░░██░░░░██
```
Run tentai_show_maker.py (and make sure PIL is available if you're generating an image).
The pattern is five squares wide and three tall, so input "5x3" when prompted.
Now convert each white square to a 1 and each black square to a 0 —
```
11101
01110
01001
```
Remove all newlines ("111010111001001"), and feed it in as prompted.
After that, the program's output might say something like:
```
.D.cC
b...c
.Cr.C
```
Lowercase implies a black dot, uppercase a white dot.
```
c = dot in the center of the square
r = dot on the right edge of the square
b = dot on the bottom edge
d = dot on the bottom right corner
(This notation was stolen from https://github.com/nespera/tentaishow)
```
To generate an image from the notation, give an affirmative when prompted. If you accidentally say no, rip out the genimage() function from the file and DIY :3

As of May 15, 2024, this code is irrevocably broken and doesn't seem to generate valid games most of the time. Hopefully this will change.
As of the morning of May 16, 2024, the generator seems to make valid puzzles all the time, but sometimes they aren't very good ones. Hopefully this will change.
As of the evening of May 16, 2024, it'll make a great puzzle if it generates a valid puzzle on its first pass, but the correcting mechanism makes it utterly freak out. Hopefully this will change.
As of May 17, 2024, I realized that it doesn't actually generate puzzles with multiple solutions much at all, so I've edited out the solver step. I'm relatively happy with this version.
