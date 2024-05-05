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

## License
[MIT License](LICENSE)