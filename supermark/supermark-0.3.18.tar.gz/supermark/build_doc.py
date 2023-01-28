from pathlib import Path
from shutil import copy
from typing import List, Sequence

import supermark.doc

from .base import Extension
from .chunks import Builder, Chunk
from .examples_yaml import YAMLExamples
from .report import Report
from .utils import write_file
from .write_md import nav_link_back


class DocBuilder(Builder):
    def __init__(
        self,
        input_path: Path,
        output_path: Path,
        base_path: Path,
        template_file: Path,
        report: Report,
        verbose: bool = False,
    ) -> None:
        super().__init__(
            input_path,
            output_path,
            base_path,
            template_file,
            report,
            verbose,
        )
        self.target_folder = input_path / "_doc"

    def build(
        self,
    ) -> None:
        self.target_folder.mkdir(exist_ok=True)
        self.copy_docs()

        # import supermark
        # print(str(supermark.__file__))

        folders: set[Path] = set()
        for extension in self.core.get_all_extensions():
            folders.add(extension.folder)

        # Overview page
        md: List[str] = []
        md.append("# Supermark Documentation")
        md.append("<ul>")
        for folder in sorted(folders):
            x = str(folder.name)
            md.append(f'<li><a href="{x}.html">{x}</a></li>')
        md.append("<ul>")
        write_file("\n".join(md), self.target_folder / "extensions.md", self.report)

        # Page for each extension
        for folder in folders:
            md: List[str] = []
            nav_link_back("All extensions", "extensions.html", md)
            is_first_extension_of_folder = True
            for e in self.core.get_all_extensions():
                if e.folder == folder and is_first_extension_of_folder:
                    self._build_extension(e, md, is_first_extension_of_folder)
                    is_first_extension_of_folder = False
            write_file(
                "\n".join(md),
                self.target_folder / f"{folder.name}.md",
                self.report,
            )

    def copy_docs(self):
        for file in Path(supermark.doc.__file__).parent.glob("*.md"):
            copy(file, self.target_folder)

    def _build_extension(
        self, extension: Extension, md: List[str], is_first_extension_of_folder: bool
    ):
        md.append("\n\n# Documentation\n")
        doc = extension.get_doc()
        if doc is not None and doc.exists() and is_first_extension_of_folder:
            with open(doc, encoding="utf-8") as file:
                lines = file.readlines()
                md.append("".join(lines))

        example_chunks = self._load_example_chunks(extension)

        ye = YAMLExamples(example_chunks)
        ye.write_doc(md)

        # table = extension.get_doc_table(example_chunks)
        # if table is not None:
        #    table.flush_row_group()
        #    md.append("\n\n\n")
        #    md.append(table.get_html())
        #    md.append("\n\n\n")

        for example in extension.get_examples():
            if example.exists():
                self._build_example(extension, example, md)

    def _load_example_chunks(
        self,
        extension: Extension,
    ) -> Sequence[Chunk]:
        example_chunks: List[Chunk] = []
        for example in extension.get_examples():
            chunks = self.core.parse_file(example)
            if chunks is not None:
                for c in chunks:
                    example_chunks.append(c)
        return example_chunks

    def _build_example(self, extension: Extension, example: Path, md: List[str]):
        md.append("\n\n# Example\n")
        code: str = ""
        # include example directly, to show the result
        with open(example, encoding="utf-8") as file:
            code = "".join(file.readlines())
        md.append(code)
        md.append("\n\n\n")
        md.append("\n\n## Source Code\n")
        # include code of the example
        md.append(f"```{self._guess_code_language(code)}")
        md.append(code)
        md.append("```")
        md.append("\n\n\n")

    def _guess_code_language(self, code: str) -> str:
        if code.startswith("---"):
            return "yaml"
        return ""
