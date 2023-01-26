from pathlib import Path

HARDCODED_BUILD_FOLDER = Path("/tmp/elrond-contract-rust")
HARDCODED_UNWRAP_FOLDER = Path("/tmp/unwrapped")
ONE_KB_IN_BYTES: int = 1024
MAX_PACKAGED_SOURCE_CODE_SIZE: int = 2 * ONE_KB_IN_BYTES * 1024
# The output archive contains not only the *.wasm, but also *.wat, *.abi.json files etc.
MAX_OUTPUT_ARTIFACTS_ARCHIVE_SIZE: int = 2 * ONE_KB_IN_BYTES * 1024

CONTRACT_CONFIG_FILENAME = "multiversx.json"
OLD_CONTRACT_CONFIG_FILENAME = "elrond.json"
