from markdown_pdf import MarkdownPdf

pdf = MarkdownPdf(toc_level=2, optimize=True)

from markdown_pdf import Section

section = Section("# Title\n", toc=False)
pdf.add_section(section)

text = """# Section with links

- [External link](https://github.com/vb64/markdown-pdf)
![Descriptive alt text](img/python.png)
"""

pdf.add_section(Section(text))


pdf.add_section(
  Section("# <a name='head1'></a>Head1\n\n![python](img/python.png)\n\nbody\n"),
  user_css="h1 {text-align:center;}"
)
pdf.save("output.pdf")
