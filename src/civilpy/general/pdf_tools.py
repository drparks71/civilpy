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

import fitz
from pathlib import Path
from civilpy.general import PrintColors

path_to_pdf = r"C:\Users\dane.parks\PycharmProjects\civilpy\Notebooks\res\temp\Enola_Structure_QC.pdf"
path_to_original_pdf = (
    r"C:\Users\dane.parks\PycharmProjects\civilpy\Notebooks\res\temp\Locked Manual.pdf"
)

doc = fitz.open(path_to_pdf)  # open a document


def check_bookmarks(toc):
    all_bookmarks = [*range(len(doc))[1:], len(doc)]
    bookmark_parent_sections = []
    print(f"Checking {len(doc)} Bookmarks...")

    # Check that there is only 1 bookmark to each sheet
    for index, bookmark in enumerate(toc):
        if bookmark[2] == -1:
            bookmark_parent_sections.append(bookmark[1])
        elif not all_bookmarks:
            print(
                f"{PrintColors.WARNING}Duplicate bookmark: {bookmark}{PrintColors.ENDC}"
            )
        else:
            try:
                all_bookmarks.remove(bookmark[2])
            except Exception as e:
                print(
                    f"\n{PrintColors.FAIL}Multiple Bookmarks are pointing to the same page: \n{bookmark[1], index, e}{PrintColors.ENDC}"
                )
                return all_bookmarks

    print(f"\nFound {len(bookmark_parent_sections)} sections of the document: ")
    print([f"{x}" for x in bookmark_parent_sections])

    # Return the Parent Sections of the PDF document
    return all_bookmarks, bookmark_parent_sections


def check_metadata_for_title(doc):
    if doc.metadata["title"] == "":
        print(
            f"\n{PrintColors.WARNING}Document has no Title in metadata{PrintColors.ENDC}"
        )
    else:
        pass


def get_and_verify_annotations(page=None):
    annotations = []

    for annot in page.annots():  # Loop through the annotations on the page
        annotations.append(annot)

    return annotations


def ns_plan_set_analysis(path):
    file = Path(path)
    doc = fitz.open(file)
    doc.bookmarks = doc.get_toc(False)
    print(f"Analyzing {doc.page_count} pages of the planset {file.name}")

    check_metadata_for_title(doc)
    x = check_bookmarks(doc.bookmarks)
    page = doc[0]
    get_and_verify_annotations(page)

    return x


if __name__ == "__main__":
    ns_plan_set_analysis(path_to_pdf)
