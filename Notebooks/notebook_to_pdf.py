import nbformat
from traitlets.config import Config
from nbconvert.preprocessors import ExecutePreprocessor
from nbconvert import PDFExporter

notebook_filename = r"C:\Users\dane.parks\PycharmProjects\civilpy\Notebooks\DPG Selector.ipynb"

# Setup config
c = Config()
c.TagRemovePreprocessor.remove_cell_tags = ("remove_cell",)
c.TagRemovePreprocessor.enabled = True

# Configure and run out exporter
c.PDFExporter.preprocessors = ["nbconvert.preprocessors.TagRemovePreprocessor"]

with open(notebook_filename) as f:
    nb = nbformat.read(f, as_version=4)

ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

ep.preprocess(nb, {'metadata': {}})

pdf_exporter = PDFExporter(config=c)

pdf_data, resources = pdf_exporter.from_notebook_node(nb)

with open(r"C:\Users\dane.parks\PycharmProjects\civilpy\Notebooks\DPG Selector.pdf", "wb") as f:
    f.write(pdf_data)
    f.close()


if __name__ == "__main__":
    print(r"Saved file to C:\Users\dane.parks\PycharmProjects\civilpy\Notebooks\DPG Selector.pdf")
