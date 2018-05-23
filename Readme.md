# ethermine_exporter

This is a prometheus exporter for Ethermine.org

## Usage

### Build

```
docker build -t jcrowthe/ethermine_exporter .
```

### Run

```
docker run -e ADDRESS='<ethereum-address>' -p 9118:9118 jcrowthe/ethermine_exporter
```

## License

MIT

[Inspiration](https://www.robustperception.io/writing-a-jenkins-exporter-in-python/) for this codebase
