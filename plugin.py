from lsp_utils import NpmClientHandler
import os


def plugin_loaded():
    LspSassPlugin.setup()


def plugin_unloaded():
    LspSassPlugin.cleanup()


class LspSassPlugin(NpmClientHandler):
    package_name = __package__
    server_directory = 'language-server'
    server_binary_path = os.path.join(server_directory, 'node_modules', 'some-sass-language-server', 'bin', 'some-sass-language-server')

    @classmethod
    def required_node_version(cls) -> str:
        return '>=20'
