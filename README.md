# pybuster
A dir buster clone that doesn't derp out when a connection fails.

## Usage
``` bash
python3 pybuster.py -u url [-w wordlist -o outfile]
```

### Bad Interpreter: No such file or directory
If you see the following:
` -bash: ./pybuster.py: /usr/bin/python3^M: bad interpreter: No such file or directory `
... fix EOL characters with dos2unix
` dos2unix pybuster.py `
