import gzip

if __name__ == '__main__':
    with gzip.open('backup_2023-01-26.gz', 'rb') as f:
        data = f.read()
        print(data)
