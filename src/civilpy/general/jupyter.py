"""
CivilPy
Copyright (C) 2019 - Dane Parks

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import asyncio
import nbformat
from nbconvert import WebPDFExporter, PDFExporter, LatexExporter
from nbconvert.preprocessors import TagRemovePreprocessor


def notebook_converter(notebook_path, format='webpdf'):
    # Set the appropriate event loop policy for Windows
    if asyncio.get_event_loop().is_running():
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # Read the notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = nbformat.read(f, as_version=4)

    # Configure the tag removal preprocessor
    tag_remove_preprocessor = TagRemovePreprocessor()
    tag_remove_preprocessor.remove_cell_tags = ("remove_cell",)
    tag_remove_preprocessor.remove_single_output_tags = ("remove_output",)
    tag_remove_preprocessor.remove_input_tags = ("remove_input",)

    # Select the appropriate exporter based on the format
    if format == 'webpdf':
        exporter = WebPDFExporter()
        file_extension = ".pdf"
        write_mode = "wb"
    elif format == 'pdf':
        exporter = PDFExporter()
        file_extension = ".pdf"
        write_mode = "wb"
    elif format == 'latex':
        exporter = LatexExporter()
        file_extension = ".tex"
        write_mode = "w"
    else:
        raise ValueError("Unsupported format. Use 'webpdf', 'pdf', or 'latex'.")

    exporter.register_preprocessor(tag_remove_preprocessor, enabled=True)

    # Convert the notebook to the desired format
    data, resources = exporter.from_notebook_node(notebook)

    # Save the result to a file with the appropriate extension
    output_filename = notebook_path.replace(".ipynb", file_extension)
    with open(output_filename, write_mode, encoding="utf-8" if write_mode == "w" else None) as f:
        f.write(data)

    print(f"File created: {output_filename}")
