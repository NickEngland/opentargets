from download_from_ftp import FTPDownloader, target_path


def test_connect():
    downloader = FTPDownloader()
    files = downloader.list_directory(target_path)
    print(len(files))
    assert len(files) == 201
