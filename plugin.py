from __future__ import annotations
from LSP.plugin.core.views import position_to_offset
from .utils import get_eol
from LSP.plugin import Session, apply_text_edits
from LSP.plugin.core.protocol import DocumentUri, ExecuteCommandParams, Position, TextEdit
from lsp_utils import NpmClientHandler
from typing import Callable, Tuple, cast
import os
import sublime

ApplyExtractCodeActionArguments = Tuple[DocumentUri, int, TextEdit]


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

    def on_pre_server_command(self, command: ExecuteCommandParams, done_callback: Callable[[], None]) -> bool:
        session = self.weaksession()
        if not session:
            return False
        if command['command'] == '_somesass.applyExtractCodeAction':
            if 'arguments' in command:
                arguments = cast(ApplyExtractCodeActionArguments, command['arguments'])
                self._handle_apply_extract_code_action(arguments, session, done_callback)
            else:
                sublime.status_message('No arguments provided to applyExtractCodeAction command. Ignoring.')
            return True
        return False

    def _handle_apply_extract_code_action(
        self, arguments: ApplyExtractCodeActionArguments, session: Session, done_callback: Callable[[], None]
    ) -> None:
        uri, document_version, text_edit = arguments
        session_buffer = session.get_session_buffer_for_uri_async(uri)
        if not session_buffer:
            done_callback()
            return
        if document_version != session_buffer.version:
            sublime.status_message('The document has changed since the extract edit was made. Please retry.')
            done_callback()
            return
        for session_view in session_buffer.session_views:
            view = session_view.view
            apply_text_edits(view, [text_edit], required_view_version=document_version)
            def trigger_rename() -> None:
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
                view.run_command('lsp_symbol_rename')
                done_callback()
            # Trigger rename after a timeout to ensure didChange is sent to the server beforehand.
            sublime.set_timeout(trigger_rename)
            return
        done_callback()

