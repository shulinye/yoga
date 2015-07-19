# yoga
A program that creates and reads yoga routines out loud to you.

### main.py
    usage: ./main.py [options]

    optional arguments:
      -h, --help            show this help message and exit
      --version             show program's version number and exit
      -t TIME, --time TIME  time (in minutes)
      -a, --aerobics        Insert aerobics moves
      -s, --strength        Insert strength moves
      -d {-1,0,1,2}, --difficulty {-1,0,1,2}
                            Difficulty: larger number=harder
      -w, --skip-warmup     skips warmup period
      -c, --skip-cooldown   skips cooldown
      -i {child,seatedMeditation,lieOnBack}, --initial-move {child,seatedMeditation,lieOnBack}
      -v, --verbose
      --debug               Debug mode: all delays removed.
      -m MEMORY, --memory MEMORY
                            How many previous moves shall I remember? (default: 5)
      --target {plank,boat}
      -o OUTFILE, --outfile OUTFILE
                            File to write log to

     

### tests.py:
Some tests to make sure that the `movesGraph` doesn't have any oddities in it. Invoked with some of the same argments

    usage: tests.py [-h] [-a] [-s] [-d {-1,0,1,2}]

    optional arguments:
      -h, --help            show this help message and exit
      -a, --aerobics        Insert aerobics moves
      -s, --strength        Insert strength moves
      -d {-1,0,1,2}, --difficulty {-1,0,1,2}
                            Difficulty: larger number=harder


## NOTE:
Requires `espeak`; edit the function `speak()` in `utils.py` if you want to use a different speaking utility.

Also: I know this algorithm can generate some pretty difficult routines, in part because it has some pretty difficult moves in it, and in part because there's a certain randomness in it. If you're going to follow this, take care to listen to your body. Heck, I can't do some of the moves I threw in here. I'm looking at you, revolved running man. Listen to your body. Injuries are not worth it. If your body doesn't want to do something today, dial it back, try again tomorrow.

And because I probably have to: If you use this code, you can't sue me for any injuries.

## LICENSE

tl;dr MIT License, as copied off of wikipedia.

`Copyright (c) 2015 Shulin Ye`

`Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:`

`The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.`

`THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.`
