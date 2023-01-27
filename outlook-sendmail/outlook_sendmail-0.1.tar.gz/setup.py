import setuptools

def main():
    setuptools.setup(
        name             = "outlook_sendmail",
        version          = "0.1",
        license          = "MIT",
        install_requires = ['pywin32'],
        py_modules       = ["outlook_sendmail"]
    )

if __name__ == "__main__":
    main()