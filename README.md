# hide-watermark

> Task B of 2023 Shenzhen Cup Mathematical Contest in Modeling

This project aims at adding watermark to pictures without being noticed by viewers.

### Version 0.0.2

> Updated on August 4th, 2023. This version includes the simplest way of hiding watermark (a.k.a. steganography), LSB algorithm.

**Configurations**

All input files should be placed under the `input` directory, including the initial picture and text you want to add as watermark (optional).

**Quick Start**

1. For adding watermark:

```plain
python SimpleLBS.py --img A --logo B --text C.txt --output D
```

Where `A` is the filename of the input picture and `D` is the filename of the output picture (`output/D` will appear after running this command).
If you want to add a long text as watermark, put the whole text in a text file named `C.txt`. Otherwise, you can input your watermark as argument `B`.

2. For extracting watermark:

```plain
python SimpleLBS_inv.py --output D
```

Will extract watermark added by `SimpleLBS.py` in picture `output/D`.