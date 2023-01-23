# This is replaced during release process.
__version_suffix__ = '153'

APP_NAME = "zalando-kubectl"

KUBECTL_VERSION = "v1.21.5"
KUBECTL_SHA512 = {
    "linux": "0bd3f5a4141bf3aaf8045a9ec302561bb70f6b9a7d988bc617370620d0dbadef947e1c8855cda0347d1dd1534332ee17a950cac5a8fcb78f2c3e38c62058abde",
    "darwin": "4d14904d69e9f50f6c44256b4942d6623e2233e45601fb17b2b58a7f6601adacd27add292f64dbe8297f81e27052b14f83f24ef4b2ba1c84344f0169d7aa24b8",
}
STERN_VERSION = "1.19.0"
STERN_SHA256 = {
    "linux": "fcd71d777b6e998c6a4e97ba7c9c9bb34a105db1eb51637371782a0a4de3f0cd",
    "darwin": "18a42e08c5f995ffabb6100f3a57fe3c2e2b074ec14356912667eeeca950e849",
}
KUBELOGIN_VERSION = "v1.26.0"
KUBELOGIN_SHA256 = {
    "linux": "d75d0d1006530f14a502038325836097b5cc3c79b637619cf08cd0b4df5b3177",
    "darwin": "1086814f19fb713278044f275c006d3d111d11ca6d92f2348af7f3eff78eecf1",
}

APP_VERSION = KUBECTL_VERSION + "." + __version_suffix__
