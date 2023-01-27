import setuptools

def main():
    setuptools.setup(
        name             = "pdf_renderer",
        version          = "0.1",
        license          = "MIT",
        install_requires = ['pandas','numpy','jinja2','pdfkit'],
        py_modules       = ["pdf_renderer"]
    )

if __name__ == "__main__":
    main()