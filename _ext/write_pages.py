import os
import pathlib
from sphinx.parsers import RSTParser
from docutils.frontend import OptionParser
from sphinx.util.docutils import SphinxDirective
from sphinx.domains import Domain
from docutils.utils import new_document


class WritePages:
    files = [f"file_{i}" for i in range(1, 10)]
    relative_path = pathlib.Path(__file__).parent.absolute() / ".."

    def write_pages(self):
        for file_name in self.files:
            with open(self.relative_path / f"{file_name}.rst", "w") as f:
                f.write(f"Test - {file_name}\n==============")


class ListPagesDirective(SphinxDirective):
    has_content = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = WritePages()

    def run(self) -> list:
        rst = ".. toctree::\n"
        rst += "   :maxdepth: 2\n\n"
        for file_name in self.pages.files:
            rst += f"   {file_name}\n"
        return self.parse_rst(rst)

    def parse_rst(self, text):
        parser = RSTParser()
        parser.set_application(self.env.app)

        settings = OptionParser(
            defaults=self.env.settings,
            components=(RSTParser,),
            read_config_files=True,
        ).get_default_values()
        document = new_document("<rst-doc>", settings=settings)
        parser.parse(text, document)
        return document.children


def main(*_):
    w = WritePages()
    w.write_pages()


def setup(app: object) -> dict:
    app.add_directive("list-pages", ListPagesDirective)
    app.connect("builder-inited", main)
