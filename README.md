```
I sure could make an image input handler in the future, but currently, here's how you use the tentai show puzzle generator:
██ = white square
░░ = black square
Pretend this is the pattern you'd like to generate —
██████░░██
░░██████░░
░░██░░░░██
Run tentai_show_maker.py (and make sure PIL is available if you're generating an image).
The pattern is five squares wide and three tall, so input "5x3" when prompted.
Now convert each white square to a 1 and each black square to a 0 —
11101
01110
01001
Remove all newlines ("111010111001001"), and feed it in as prompted.
After that, the program's output might say something like:
.D.cC
b...c
.Cr.C
Lowercase implies a black dot, uppercase a white dot.
c = dot in the center of the square
r = dot on the right edge of the square
b = dot on the bottom edge
d = dot on the bottom right corner
(This notation was stolen from https://github.com/nespera/tentaishow)
To generate an image from the notation, give an affirmative when prompted. If you accidentally say no, rip out the genimage() function from the file and DIY.

This code is stochastic and it sucks; please keep this in mind as you run into errors every other time you use it :3
```
