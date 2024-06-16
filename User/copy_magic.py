import sublime
import sublime_plugin
import re
from pathlib import Path

lib_path = Path("D:\\MSYS2\\mingw64\\include\\c++\\13.2.0\\x86_64-w64-mingw32")

atcoder_include = re.compile('#include\s*["<](atcoder/[a-z_]*(|.hpp))[">]\s*')
include_guard = re.compile('#.*ATCODER_[A-Z_]*_HPP')

def dfs(f: str):
    defined = set()
    result = []
    if f in defined:
        return result
    defined.add(f)

    try:
        s = open(str(lib_path / f)).read()
        for line in s.splitlines():
            if include_guard.match(line):
                continue

            m = atcoder_include.match(line)
            if m:
                result.extend(dfs(m.group(1)))
                continue
            result.append(line)
    except FileNotFoundError:
        print(f"File {f} not found.")

    return result

class CopyMagicCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        selected_text = "\n".join([self.view.substr(region) for region in self.view.sel() if not region.empty()])
        sublime.set_clipboard(selected_text.strip())
        self.expander_operation()

    def is_enabled(self):
        return any(not sel.empty() for sel in self.view.sel())

    def expander_operation(self):
        s = sublime.get_clipboard()
        result = []
        for line in s.splitlines():
            m = atcoder_include.match(line)
            if m:
                result.extend(dfs(m.group(1)))
                continue
            result.append(line)

        output = '\n'.join(result) + '\n'
        sublime.set_clipboard(output)
