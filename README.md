# Hide Watermark

> Task B of 2023 Shenzhen Cup Mathematical Contest in Modeling

This project aims at adding watermark to pictures without being noticed by viewers.

### Direct Answers

**Task B1**

```plain
python DCT_vote.py --img P.jpg --logo 深圳杯数学建模挑战赛 --output SP.png
python DCT_vote_inv.py --img SP.png
```

The output should be:

```plain
Watermark: 深圳杯数学建模挑战赛
```

**Task B2**

```plain
python DCT_vote.py --img P.jpg --text law.txt --output SP.png
python DCT_vote_inv.py --img SP.png
```

Then you can see an identical text file `watermark.txt` in `./output/`.

### Version 1.0.0

> Updated on August 9th, 2023. This version uses DCT to hide watermark in picture. Technical details will be shown in the paper.

**Configurations**

See at **version 0.0.2**.

**Commands**

1. For adding watermark:

```plain
python DCT_vote.py --img A --logo B --text C.txt --output D
```

Check out the meanings of arguments at **version 0.0.2**.

2. For extracting watermark:

```plain
python DCT_vote_inv.py --img D
```

Will extract watermark added by `DCT_vote.py` in picture `./output/D`. If the watermark's length exceeds 100, then check it out at `./output/watermark.txt`.

Images of `JPEG` format is not supported in this version.

Note that the name of argument has changed compared to **version 0.0.2**.

### Version 0.0.2

> Updated on August 4th, 2023. This version includes the simplest way of hiding watermark (a.k.a. steganography), LSB algorithm.

**Configurations**

All input files should be placed under the `input` directory, including the initial picture and text you want to add as watermark (optional).

**Commands**

1. For adding watermark:

```plain
python SimpleLBS.py --img A --logo B --text C.txt --output D
```

Where `A` is the filename of the input picture and `D` is the filename of the output picture (`output/D` will appear after running this command).

If you want to add a long text as watermark, put the whole text in a text file named `C.txt`. Otherwise, you can input your watermark as argument `B`.

All arguments are optional.

2. For extracting watermark:

```plain
python SimpleLBS_inv.py --output D
```

Will extract watermark added by `SimpleLBS.py` in picture `./output/D`.