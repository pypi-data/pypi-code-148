import setuptools

def main():
    setuptools.setup(
        name             = "foundry_df_interface",
        version          = "0.1",
        license          = "MIT",
        install_requires = ['pandas', 'palantir-sdk'],
        py_modules       = ["foundry_df_interface"]
    )

if __name__ == "__main__":
    main()