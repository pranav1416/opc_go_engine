import os
import sys
import multiprocessing

import six

if sys.version_info[0] == 3:
    from urllib.request import urlopen, urlretrieve
else:
    from urllib import urlopen, urlretrieve


def worker(url_and_target):
    try:
        (url, target_path) = url_and_target
        print('>>> Downloading ' + target_path)
        urlretrieve(url, target_path)
    except (KeyboardInterrupt, SystemExit):
        print('>>> Exiting child process')


class KGSIndex:
    """Using previously played games from at least 6 dan to improve predictions. Store data locally."""

    def __init__(self, url='http://u-go.net/gamerecords', index_page='kgs_index.html', directory='data'):
        self.url = url
        self.index_page = index_page
        self.data_directory = directory
        self.file_info = []
        self.urls = []
        self.load_index()

    def download_files(self):
        """Retrieves files from KGS server."""
        if not os.path.isdir(self.data_directory):
            os.makedirs(self.data_directory)
        urls_to_download = []
        for file_info in self.file_info:
            url = file_info['url']
            file_name = file_info['filename']
            if not os.path.isfile(self.data_directory + '/' + file_name):
                urls_to_download.append((url, self.data_directory + '/' + file_name))
        for url in urls_to_download:
            worker(url)

        """
        multiprocessing causing errors

        cores = multiprocessing.cpu_count()
        pool = multiprocessing.Pool(processes=cores)
        try:
            it = pool.imap(worker, urls_to_download)
            for _ in it:
                pass
            pool.close()
            pool.join()
        except KeyboardInterrupt:
            print(">>> Caught KeyboardInterrupt, terminating workers")
            pool.terminate()
            pool.join()
            sys.exit(-1)
        """

    def load_index(self):
        """Create the actual index representation from the previously downloaded or cached html."""
        index_contents = self.create_index_page()
        split_page = [item for item in index_contents.split('<a href="') if item.startswith("https://")]
        for item in split_page:
            download_url = item.split('">Download')[0]
            if download_url.endswith('.tar.gz'):
                self.urls.append(download_url)
        for url in self.urls:
            filename = os.path.basename(url)
            split_file_name = filename.split('-')
            num_games = int(split_file_name[len(split_file_name) - 2])
            print(filename + ' ' + str(num_games))
            self.file_info.append({'url': url, 'filename': filename, 'num_games': num_games})

    def create_index_page(self):
        if os.path.isfile(self.index_page):
            print('>>> Reading cached index page')
            index_file = open(self.index_page, 'r')
            index_contents = index_file.read()
            index_file.close()
        else:
            print('>>> Downloading index page')
            fp = urlopen(self.url)
            data = six.text_type(fp.read())
            fp.close()
            index_contents = data
            index_file = open(self.index_page, 'w')
            index_file.write(index_contents)
            index_file.close()
        return index_contents


"""Call to download and store files locally."""
index = KGSIndex()
index.download_files()
