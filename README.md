# vapor_generator
A compressor and decompressor for the basic ASCII-based RLE in Undertale's obj_vaporized_new. I know I didn't say it's that in the tool itself, I realized it after I had wrote the dumb CLI.

## Usage
```
usage: python -m vapor_generator [-h] {generate,parse} ...

Tool for dealing with vapor data for Undertale's obj_vaporized_new.

positional arguments:
  {generate,parse}  Commands
    generate        Generate a new vapor data file.
    parse           Create an image from a vapor data file.

options:
  -h, --help        show this help message and exit
```
```
usage: python -m vapor_generator generate [-h] input output

positional arguments:
  input       The input image file
  output      The output data file

options:
  -h, --help  show this help message and exit
```
```
usage: python -m vapor_generator parse [-h] input output

positional arguments:
  input       The input data file
  output      The output image file

options:
  -h, --help  show this help message and exit
```

## License
[MIT License](LICENSE)