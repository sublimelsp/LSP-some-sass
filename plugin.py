from __future__ import annotations

from .utils import get_eol
from functools import partial
from LSP.plugin import LspPlugin, OnPreStartContext, Promise, apply_text_edits, command_handler
from LSP.plugin.core.views import position_to_offset
from LSP.protocol import DocumentUri, LSPAny, Position, TextEdit
from lsp_utils import NodeManager
from pathlib import Path
from sublime_lib import ResourcePath
from typing import Tuple, cast
from typing_extensions import override
import sublime

ApplyExtractCodeActionArguments = Tuple[DocumentUri, int, TextEdit]


def plugin_loaded():
    LspSassPlugin.register()


def plugin_unloaded():
    LspSassPlugin.unregister()


class LspSassPlugin(LspPlugin):

    @classmethod
    @override
    def on_pre_start_async(cls, context: OnPreStartContext) -> None:
        package_name = cls.plugin_storage_path.name
        NodeManager.on_pre_start_async(
            context,
            cls.plugin_storage_path,
            ResourcePath('Packages', package_name, 'language-server'),
            Path('node_modules', 'some-sass-language-server', 'bin', 'some-sass-language-server'),
            node_version_requirement='>=20',
        )

    @command_handler('_somesass.applyExtractCodeAction')
    def on_apply_extract_code_action_command(self, arguments: list[LSPAny] | None) -> Promise[LSPAny]:
        if arguments and (session := self.weaksession()):
            uri, document_version, text_edit = cast('ApplyExtractCodeActionArguments', arguments)
            if session_buffer := session.get_session_buffer_for_uri_async(uri):
                if document_version != session_buffer.last_synced_version:
                    sublime.status_message('The document has changed since the extract edit was made. Please retry.')
                    return Promise.resolve(None)
                for session_view in session_buffer.session_views:
                    view = session_view.view

                    def trigger_rename(view: sublime.View | None) -> None:
                        if not view:
                            return
                        new_text = text_edit['newText']
                        lines = new_text.split(get_eol(new_text))
                        usage_keywords = ['_variable', '_function', '_mixin']
                        line_of_usage = lines[len(lines) - 1]
                        usage_keyword_positions = [line_of_usage.find(keyword) for keyword in usage_keywords]
                        position: Position = {
                            'line': text_edit['range']['start']['line'] + len(lines) - 1,
                            'character': max(usage_keyword_positions) + 1,
                        }
                        point = position_to_offset(position, view)
                        view.sel().clear()
                        view.sel().add(point)
                        view.run_command('lsp_symbol_rename', {'session_name': self.plugin_storage_path.name})

                    return apply_text_edits(view, [text_edit], required_view_version=document_version) \
                        .then(lambda view: sublime.set_timeout(partial(trigger_rename, view)))
        else:
            sublime.status_message('No arguments provided to applyExtractCodeAction command. Ignoring.')
        return Promise.resolve(None)
