# vapor_generator
(De)compressor for the basic ASCII-based RLE used by Undertale's obj_vaporized_new. I know I didn't say it's that in the tool itself, I realized it after I had wrote the dumb CLI.

## Usage
```
usage: python -m vapor_generator [-h] {compress,decompress} ...

(De)compressor for the basic ASCII-based RLE used by Undertale's obj_vaporized_new.

positional arguments:
  {compress,decompress}
                        Commands
    compress            Compresses an image to a vapor data file.
    decompress          Decompresses a vapor data file to an image.

options:
  -h, --help            show this help message and exit
```
```
usage: python -m vapor_generator compress [-h] input output

positional arguments:
  input       The input image file
  output      The output data file

options:
  -h, --help  show this help message and exit
```
```
usage: python -m vapor_generator decompress [-h] input output

positional arguments:
  input       The input data file
  output      The output image file

options:
  -h, --help  show this help message and exit
```

## Accuracy
This compressor might emit data that is slightly different than whichever compressor Toby came up with
(error margin wildly varies),
but if you manually replace `~` at the end with `~~~`, it usually should be close enough to be
indistinguishable from the original data.

So far I don't see this actually causing errors in decompression, neither with our own decompressor
nor with the original decompressor.
In fact, we seem to generate smaller - more "efficiently compressed" - data!
(It's not like this format is efficient anyway.) 
`test_data/allofthem.py` is an accuracy test, you can get a glimpse of this compressor's accuracy
by running that.

Feel free to raise an Issue if this gets problematic for you.

## License
[MIT License](LICENSE)