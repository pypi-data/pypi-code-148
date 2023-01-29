from copyright_cli import internal
import pathlib
import shutil


def add_copyright(config_path, output_path, skip_if_exists):
    config = internal.Configuration.load(config_path, "copyright.toml")

    if output_path is None:
        output_path = str(config.root_path)

    for folder in config.search_folders:
        files = internal.FileSearch.run(config.root_path, [folder], config.file_extensions, False)
        for file_path in files:
            input_file_path = str(pathlib.Path(config.root_path).joinpath(file_path))

            has_copyright = False
            if skip_if_exists:
                has_copyright = internal.FileProcessor.has_copyright(input_file_path, config.copyright_info)

            output_file_path = pathlib.Path(output_path).joinpath(file_path)
            if has_copyright:
                if not output_file_path.exists():
                    shutil.copyfile(input_file_path, str(output_file_path))
            else:
                internal.FileProcessor.add_copyright_to_file(input_file_path, str(output_file_path), config.copyright_info)
