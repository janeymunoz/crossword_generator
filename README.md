# Crossword Generator
_A tool to create valid crossword puzzle grids!_

## Description
This code, written in Python, will output an image of a valid (psuedo-)randomly generated crossword grid. Although there may be no stringent definition of what makes a crossword puzzle layout 'valid,' in this particular instance it means that the grid adheres to [construction guidelines](https://www.nytimes.com/crosswords/submissions) as outlined by the New York Times. In summary, the criteria are:
* grid size
  - 15 x 15 (i.e., small)
  - 21 x 21 (i.e., large)
* minimum word length: 3 letters
* symmetry about the origin, or center, of the puzzle.

The repository includes an example of an output for each puzzle size, [small](xword_example_small.png) and [large](xword_example_large.png).

## How to use it
This crossword generator requires Python 3.6 and Pillow 5.1.0 (PIL Fork). 
After cloning or downloading the repository, the function `xword_image_gen` is all that needs to be run in order to produce your crossword grid!
If you have the required dependencies and have the repository on your computer, the following script run from the directory in which the repository is saved will save a .png image file into the repository directory. 
```
$ python -c 'import xword_generator; xword_generator.xword_image_gen()'
```
### Syntax
If no arguments are given to the `xword_image_gen` function, as shown above, default arguments will be used. Following is the syntax for **xword_image_gen()**:
```
xword_generator.xword_image_gen(size=None, max_word_len=None, max_black_len=None, save_name=None)
```
#### Parameters
* size
  - "S" or "L". "S" = small, 15 x 15. "L" = large, 21 x 21
  - default size="S"
* max\_word\_len
  - the maximum length of a word that is generated in the first row of the puzzle, influencing how the rest of the puzzle will unfold
  - default max\_word\_len=5
* max\_black\_len
  - the maximum number of black squares that can be generated in the first row of the puzzle, influencing how the rest of the puzzle will unfold
  - default max\_black\_len=4
* save\_name
  - a string indicating the name of the output file where the image will be saved in the directory. **Will overwrite existing file of the same name.** Name must be string type, and end in ".png"
  - default save\_name="xword\_out.png"

## Future work
As both a crossword enthusiast and amatuer programmer, I embarked on writing this code to exercise my coding ability, and also get myself one step closer to eventually submitting my own crossword to be considered for publishing in the NYT! *stares off whistfully...* To both ends, I plan to continue to work on this repository. Some of my current ideas on future work include:
* specifiying maximum number of words in the puzzle. The NYT consturciton guidelines give maximum word counts for puzzles based on size. Cursory investigation seems to indicate that this criterion is typically met, but further constraints should be outlined to ensure.
  - 15 x 15 (themed): 78 words
  - 15 x 15 (themeless): 72 words
  - 21 x 21 (always themed): 140 words
* specifying themed versus themeless for small puzzles (similar to previous bullet)
* adding more options for a tailored output. For example, being able to specify that the four longest clues are 15 squares in length.
* debugging. There appears to be a bug where the "compare\_look" function returns a NoneType object, halting the crossword output altogether
* generating words to fill puzzle. Given zero or more words to be included in the puzzle, use a dictionary to fill the rest of the puzzle with valid word combinations.
* generating an answer key from words included in the puzzle.
* generating clues for words based on existing crosswords available on the internet.
