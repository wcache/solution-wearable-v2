import sys
import uos
import ql_fs
import request
import fota as BaseFota
import app_fota as BaseAppFota
from app_fota_download import update_download_stat
from .threading import Event
from .tarfile import TarFile


class Fota(object):

    class WriteError(Exception):
        pass

    class FlushError(Exception):
        pass

    class VerifyError(Exception):
        pass

    def __init__(self, auto_reset=False, progress_callback=None):
        self.fota = BaseFota(reset_disable=int(not auto_reset))
        self.__finished = Event()
        self.__success = False
        self.__progress_callback = progress_callback

    def __download_callback(self, args):
        if args[0] in (0, 1, 2):
            if self.__progress_callback:
                self.__progress_callback(args[1])
            if args[1] == 100:
                self.__success = True
                self.__finished.set()
        else:
            self.__success = False
            self.__finished.set()

    def get_result(self, timeout=None):
        self.__finished.wait(timeout=timeout)
        return self.__success

    def upgrade(self, url):
        self.__finished.clear()
        self.__success = False
        return self.fota.httpDownload(url1=url, callback=self.__download_callback) == 0

    def mini_upgrade(self, url1, url2):
        return self.fota.httpDownload(url1=url1, url2=url2) == 0

    def local_upgrade(self, path):
        with open(path, 'rb') as f:
            size = f.seek(0, 2)
            f.seek(0, 0)
            while True:
                content = f.read(4096)
                if not content:
                    break
                if self.fota.write(content, size) == -1:
                    raise self.WriteError('fota write bytes stream error')
                if self.__progress_callback:
                    self.__progress_callback(int(f.tell() / size * 100))
        if self.fota.flush() == -1:
            raise self.FlushError('fota flush error')
        if self.fota.verify() == -1:
            raise self.VerifyError('fota verify error')


class AppFota(object):

    class DownloadError(Exception):
        pass

    class DeprecatedError(Exception):
        pass

    def __init__(self):
        self.fota = BaseAppFota.new()

    def set_update_flag(self):
        self.fota.set_update_flag()

    def download(self, url, file_name):
        if self.fota.download(url, file_name) != 0:
            raise self.DownloadError('app fota download error')

    def bulk_download(self, info):
        # return self.fota.bulk_download(info)
        raise self.DeprecatedError('method `bulk_download` has been deprecated')

    @staticmethod
    def __download_file_from_server(url, path):
        response = request.get(url)
        if response.status_code not in (200, 206):
            return False
        with open(path, 'wb') as f:
            for c in response.content:
                f.write(c)

    @staticmethod
    def __decode_file_to_updater_dir(path, updater_dir):
        with TarFile.open(path) as f:
            f.extractall(path=updater_dir)
        for file in f.update_file_list:
            update_download_stat('', file['file_path'], file['size'])

    def download_tar(self, url, path="/usr/temp.tar.gz"):
        """通过压缩文件下载升级：`tar -zcvf code.tar.gz usr`"""
        self.__download_file_from_server(url, path)
        updater_dir = self.fota.app_fota_pkg_mount.fota_dir + '/usr/.updater/'
        try:
            self.__decode_file_to_updater_dir(path, updater_dir)
        except Exception as e:
            if ql_fs.path_exists(updater_dir):
                ql_fs.rmdirs(updater_dir)
            raise e
        finally:
            if ql_fs.path_exists(path):
                uos.remove(path)
