from ftplib import FTP
from typing import List
import argparse
import os

target_path = '/pub/databases/opentargets/platform/21.11/output/etl/json/targets/'
disease_path = '/pub/databases/opentargets/platform/21.11/output/etl/json/diseases/'
eva_path = '/pub/databases/opentargets/platform/21.11/output/etl/json/evidence/sourceId=eva/'

file_dict = {'targets': target_path,
             'diseases': disease_path,
             'eva': eva_path,
             'all': None}


class FTPDownloader:
    def __init__(self, server: str = 'ftp.ebi.ac.uk'):
        self.server = server
        self.ftp = FTP(self.server)
        self.ftp.login()

    def list_directory(self, path: str) -> List[str]:
        self.ftp.cwd(path)
        file_list = self.ftp.nlst()
        return file_list

    def download_all(self, path: str, file: str):
        files = self.list_directory(path)
        files = [file for file in files if file.endswith('.json')]
        length = len(files)
        files.sort()
        if not os.path.isdir('download'):
            os.makedirs('download')
        with open('download/' + file, 'wb') as output:
            for x, file in enumerate(files, 1):
                print(x, '/', length, 'Doing file', file)
                self.ftp.retrbinary('RETR ' + file, output.write)


def main():
    parser = argparse.ArgumentParser(description='Download OpenTargets JSON files')
    parser.add_argument('type', choices=file_dict.keys())
    parser.add_argument('--server', default='ftp.ebi.ac.uk')
    args = parser.parse_args()
    client = FTPDownloader(args.server)
    print("Downloading " + args.type)
    if args.type == 'all':
        for name, path in file_dict.items():
            if path is None:
                continue
            print(name, path)
            client.download_all(path, name + '.json')

    else:
        client.download_all(file_dict[args.type], args.type + '.json')


if __name__ == '__main__':
    main()
