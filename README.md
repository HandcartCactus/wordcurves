# WordCurves

## Setup
Clone the repository.

### Conda Env
Create the `conda` environment from the `.yml` file:
```bash
conda env create -f wordcurves.yml
```

## What Is WordCurves?
WordCurves is an open-source library for research on recursively generated combinatorial words and their associated curves.

### Words
A combinatorial word $w_{\Sigma}$ is an ordered list of characters from the alphabet $\Sigma$. Words in english can count as combinatorial words, but alphabets do not need to be latin characters. For example, a _binary word_ is a word made from the alphabet $\Sigma = \{0,1\}$. The following count as binary words: $\phi$ (the null word with no characters), $0$, $010$, and $00100100101010$. This library largely concerns binary words.

For words that are not null, we can obtain the $i$th character of a word just like you might get the $i$th item in a list. Syntax for the operation will vary but occasionally, the $i$th character of a word $w$ is denoted by $w_i$.

Words can be concatenated and/or repeated. The syntax for concatenation is writing both words consecutively. For example, if $w=010$ and $v=1111$, then $wv=0101111$. The syntax for repeated concatenation of a word $w$ for $k$ times is $w^k$. 

In `python`, we can use strings to represent words, but string concatenation and repitition have different syntax. To concatenate two words `w='010'` and `v='1111'`, the syntax is `w + v`. To repeat a word `k` times (where `k` is an `int`), we can use the syntax `w * k`. For example, `'01' * 2 = '0101'`.

### Fibonacci Words
In combinatorics, it is sometimes of interest to create words recursively. For example, the _Fibonacci Words_ $f$ are created recursively the following familliar way. Let $f_n$ denote the $n$th fibonacci word (not the $n$th character this time). We start with two base case words, $f_0$ and $f_1$.
$$f_0 = 0;\; f_1=01$$

To get the next fibonacci word, concatenate the previous two words.
$$f_2 = f_1 f_0 = 010$$
To get the $n$th fibonacci word, the formula is the same as before:
$$f_n = f_{n-1} f_{n-2}$$

The length of $f_n$ is $F_{n+1}$, the $(n+1)$th fibonacci number, which grows exponentially. However, because of the recursive concatenation, words $f_n$ for large $n$ are rich with structure and very interesting to play with combinatorially. The limit of $f_n$ does indeed exist, and it is often denoted as:
$$f_{\infty} = \lim_{n \to \infty} f_n$$

Excitingly, the fibonacci words are merely just the tip of the iceberg. There are many different types of recursively generated words. The focus of current research in this area is generating and analyzing binary words created through concatenation and repitition. This library can assist with this area of research and much more. 

### Curves
To illustrate the structure of small fibonacci words and their generalizations, one can employ tables or lists. However, this becomes unruly as as the words become exponentially larger. We can visualize large words and their greater structure by drawing curves that change shape depending on combinatorial structure, and scaling them down to see their larger shape. Drawing a word as a curve is largely arbitrary, but one drawing rule that yields effective results employs turtle graphics, or as a mathematician might say, _a non-branching Lindenmeyer System_. In incredibly verbose python, it looks something like this:

```python
myword = "001001010001001001010101" # word to draw
turning_angle = math.pi / 3 # <-- a configurable parameter

# the turtle's trail is the curve
turtle = Turtle(pos=(0,0), initial_angle=math.pi/2)

# iterate over the character and it's index for each character in the word.
for index, char in enumerate(myword):
    if char=='1':
        turtle.step_forward()

    elif char=='0':
        turtle.step_forward()

        #  if index is even
        if index % 2 == 0:
            turtle.turn_right(turning_angle)

        #if index is odd
        else:
            turtle.turn_left(turning_angle)
```
We can see that every character requires a step forward, but $0$'s make the turtle turn after stepping. Interestingly, the turtle does not step _after_ the turn, meaning for any word $w$, the curves of the words $w0$ and $w1$ are identical. However, the turn itself does reveal the parity of the index of all $0$ characters, and it makes word length parity and character index parity into essential determining features of a word curve. The impact of this is that the insertion of a single character in a word flips the direction of all the associated turns that come after the character, which makes the curve of the new word with a single insertion visibly distinguishable from the original curve. Despite this, combinatorially generated words which rely on concatenation will frequently have similar shapes to words from a few iterations ago, give or take some level of detail. E.g. $f_n$ and $f_{n-1}$ may look different, but scaled down copies of $f_n$ and copies of $f_{n-2}$ or $f_{n-6}$ might look almost the same albeit "hairier" due to barely-perceptible detail on the shrunken copy of $f_n$. Likewise, combinatorial word curves from the same family might look very similar, but be rotated or translated due to parity effects. All of this is to say that because of the recursive structure of the words themselves, word curves demonstrate similarities with previously constructed word curves of the same family. Also as words become larger, their associated curves contain more fine detail when scaled down to a constant size. 

**The combination of self-similarity and increasing detail often creates curves which approach fractals when scaled to a constant size. In fact, with the described curve drawing proccess, the limit of the scaled curve for $f_{\infty}$ and similar generalizations _are_ fractals.** This is a very cool fact.

Despite being incredibly cool, the fractal nature of a recursive word curve is _not_ trivial. Patterns of similarity and overall structure must be individually discovered for each new generalization, and then eventually proven rigorously. Finding patterns and proving them is often tedious and heavily computational. 

To add insult to injury, the very localized drawing rule (that depends on characters of the word) impedes the discovery of important numbers often associated with fractals such as the _Hausdorff dimension_ (or other measurements of a fractal from Fractal Geometry) because those measurements require understanding how the fractal exhibits similarities on a "global" scale. To find these numbers, work must be done to decompose words from each new generalization into a set of previously constructed words that have similar curve shapes, so that the general structure of the fractal can be determined.

## Repo Intent
I intend this repo to assist with various tasks in the research workflow.
### Research Workflow
In my experience, the research workflow is something like this:
1. Select or create a generalization of the fibonacci words
2. Create the associated word curves
3. Inspect iterations of word curves for periodic similarities
4. If a period $p$ is found, find a way to write the $n$th word $w_n$ in terms of $w_{n-p},\, w_{n-2p}$, etc.
5. Describe the boundary shape of the curves for $w_n, w_{n-p}$, etc.
6. Use induction to find the final angle of the turtle after drawing the curves for $w_{n}, w_{n-p}$, etc.
7. Create an Iterated Function System (IFS) that describes the global periodic structure of the curves $w_n, w_{n-p}$, etc.
8. Use the IFS to determine the fractal measurements.

### Package Goals:
I would like the package help with all that. So far, it can:

- [x] Create any arbitrary recursively defined combinatorial words:
  
  See the `words.py` module and the `wordgen` method.

- [x] Create associated word curves:
  
  See the `curves.py` module, the `get_curve` and `get_normed_curve` methods.
- [x] Graph many iterations of word curves to assist with finding periodic similarities, even scaling and rotating them so they are uniform size and direction.

    See the `draw_curves.ipynb` notebook for custom plots of arbitrary word curves.

Currently, it does not:
- [ ] Suggest periods $p$ of interest. (Computationally expensive but simple.)
- [ ] Find a consistent way to write the $n$th word $w_n$ in terms of $w_{n-p},\, w_{n-2p}$, etc for arbitrary $p$. (Computationally expensive and complicated.)
- [ ] Describe the boundary shape of the curves for $w_n, w_{n-p}$, etc. (I don't know algorithms for this, but I am using convex hulls ATM)
- [ ] Find the final angle of the turtle after drawing the curves for $w_{n}, w_{n-p}$, etc. (Complete for small $n$, arbitrary $n$ depends on prev tasks.)
- [ ] Create an Iterated Function System (IFS) that describes the global periodic structure of the curves $w_n, w_{n-p}$, etc.
- [ ] Use the IFS to determine the fractal measurements. (doable, but depends on other stuff).

Many of those are coming soon. I would also like to heavily document and test this repo, but that comes a close second to functionality.

## Contributing
Feel free to reach out if you'd like to contribute.

## License
MIT License, but if you're going to use it, I'd love to know! Drop a star, @ me on twitter, or shoot me an email.









