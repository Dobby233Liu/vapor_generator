# vapor_generator
(De)compressor for the basic ASCII-based RLE used by Undertale's obj_vaporized_new.
I know I didn't say it's that in the tool itself, I only realized it after writing the dumb CLI.

## Usage
```
usage: python -m vapor_generator [-h] {compress,decompress} ...

(De)compressor for the basic ASCII-based RLE used by Undertale's obj_vaporized_new

positional arguments:
  {compress,decompress}
                        Commands
    compress            compresses an image to a vapor data file
    decompress          decompresses a vapor data file to an image

options:
  -h, --help            show this help message and exit
```
```
usage: python -m vapor_generator compress [-h] [-O] input output

positional arguments:
  input           the input image file
  output          the output data file

options:
  -h, --help      show this help message and exit
  -O, --optimize  enables some tricks to reduce output size (if disabled, I will try to produce accurate results)
```
```
usage: python -m vapor_generator decompress [-h] input output

positional arguments:
  input       the input data file
  output      the output image file

options:
  -h, --help  show this help message and exit
```

## Accuracy
This compressor might rarely emit data that is slightly different than whatever compressor Toby came up
with, but it usually should be close enough to the original data.
So far I don't see this actually causing errors in decompression, neither with our own decompressor
nor with the original decompressor.

`tests/allofthem.py` is an accuracy test, you can get a glimpse of this compressor's accuracy
by running that.

## License
[MIT License](LICENSE)