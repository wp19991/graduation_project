import paramiko


class ssh_diver:
    """
    - 具有ssh的功能
    - 上传文件
    - 执行命令
    """

    def __init__(self, host, port, user, password):
        """
        :param host:  str host
        :param port:  int port
        :param user:  str user
        :param password:  str password
        """
        self.host = str(host)
        self.port = int(port)
        self.user = str(user)
        self.password = str(password)

    def upload_file(self, file_path, remote_dir_path):
        """
        :param file_path:  str 文件路径，包括文件名称
        :param remote_dir_path:  int 远程的文件夹路径
        """
        try:
            s = paramiko.SSHClient()
            s.load_system_host_keys()
            s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            t = paramiko.Transport((self.host, self.port))
            t.connect(username=self.user, password=self.password)

            sftp = paramiko.SFTPClient.from_transport(t)

            sftp.put(r'{}'.format(file_path), '{}'.format(remote_dir_path))
            s.close()

            return True
        except:
            return False
