import json


class Conf:
    _conf: object
    _source_file: str
    _export_path: str

    def __init__(self,
                 json_config_file: str,
                 export_path: str = "./") -> None:
        """
        Open and parse the JSON config file.
        :param: json_config_file: The JSON config file to parse
        :param: export_path: path where JSON can be exported as cpp files for use with Arduino sketches
        """
        self._export_path = export_path
        fl = None
        try:
            fl = open(json_config_file, 'r')
            self._conf = json.load(fl)
        except Exception as e:
            raise ValueError("Cannot open JSON config file [{}]".format(str(e)))
        finally:
            if fl is not None:
                fl.close()
        return

    @property
    def config(self):
        """
        The object resulting from the parse of the JSON config file.
        :return: Dictionary of values loaded values as dictionary indexed by the JSON item names.
        """
        return self._conf

    @property
    def source_file(self) -> str:
        """
        The name of the JSON file used to bootstrap the configuration
        :return: JSON file name
        """
        return self._source_file
