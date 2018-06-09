# ID3 algorithm implementation in Python

### Installing

Require [pptree](https://github.com/clemtoy/pptree)

```
pip install pptree
```

## Usage

```
python3 id3.py FILENAME.csv
```

## Example

```
python3 id3.py baseball.csv
```

Output:

```
        ┌(Overcast)┐
        │          └Yes
 Outlook┤
        ├(Sunny)┐
        │       │        ┌(High)┐
        │       │        │      └No
        │       └Humidity┤
        │                └(Normal)┐
        │                         └Yes
        └(Rain)┐
               │    ┌(Weak)┐
               │    │      └Yes
               └Wind┤
                    └(Strong)┐
                             └No
spent: 0.006014347076416016s
```
