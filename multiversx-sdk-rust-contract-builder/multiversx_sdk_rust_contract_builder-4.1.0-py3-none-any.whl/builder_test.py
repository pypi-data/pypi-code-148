from pathlib import Path

from multiversx_sdk_rust_contract_builder import builder
from multiversx_sdk_rust_contract_builder.packaged_source_code import \
    PackagedSourceCode

input_folder = Path("./testdata/input")
expected_folder = Path("./testdata/expected")
output_folder = Path("./testdata/output")


def test_build_project_adder():
    outcome = builder.build_project(
        project_folder=input_folder / "adder",
        parent_output_folder=output_folder,
        specific_contract=None,
        cargo_target_dir=Path("/tmp/cargo-target-dir"),
        no_wasm_opt=False,
        context="test"
    )

    actual_src_package = PackagedSourceCode.from_file(outcome.get_entry("adder").artifacts.src_package.path)
    expected_src_package = PackagedSourceCode.from_file(expected_folder / "adder-1.2.3.source.json")
    actual_wat = outcome.get_entry("adder").artifacts.text.read().decode()

    assert outcome.context == "test"
    assert outcome.get_entry("adder").version == "1.2.3"
    assert outcome.get_entry("adder").codehash == "58c6e78f40bd6ccc30d8a01f952b34a13ebfdad796a2526678be17c5d7820174"
    assert_equal_src_package(actual_src_package, expected_src_package)
    assert actual_wat == (expected_folder / "adder.wat").read_text()


def test_build_project_empty():
    outcome = builder.build_project(
        project_folder=input_folder / "empty",
        parent_output_folder=output_folder,
        specific_contract=None,
        cargo_target_dir=Path("/tmp/cargo-target-dir"),
        no_wasm_opt=False,
        context="test"
    )

    actual_src_package = PackagedSourceCode.from_file(outcome.get_entry("empty").artifacts.src_package.path)
    expected_src_package = PackagedSourceCode.from_file(expected_folder / "empty-4.5.6.source.json")
    actual_wat = outcome.get_entry("empty").artifacts.text.read().decode()

    assert outcome.context == "test"
    assert outcome.get_entry("empty").version == "4.5.6"
    assert outcome.get_entry("empty").codehash == "20df405fa1733a22748c888f6c1571f2c12cc40a8b1de800e0fd105674b426a5"
    assert_equal_src_package(actual_src_package, expected_src_package)
    assert actual_wat == (expected_folder / "empty.wat").read_text()


def assert_equal_src_package(actual: PackagedSourceCode, expected: PackagedSourceCode):
    assert actual.name == expected.name
    assert actual.version == expected.version

    for actual_entry, expected_entry in zip(actual.entries, expected.entries):
        assert actual_entry.path == expected_entry.path, f"actual={actual_entry.path}, expected={expected_entry.path}"
        assert actual_entry.content == expected_entry.content, f"content differs for {actual_entry.path}"
