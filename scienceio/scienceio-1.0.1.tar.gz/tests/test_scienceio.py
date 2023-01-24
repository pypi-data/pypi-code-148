import pytest
import time
import uuid

from src.scienceio import HTTPError, ScienceIO

QUERY_TEXT = (
    "The COVID-19 pandemic has shown a markedly low proportion of cases among "
    "children 1-4. Age disparities in observed cases could be explained by "
    "children having lower susceptibility to infection, lower propensity to "
    "show clinical symptoms or both."
)


@pytest.fixture(scope="session", autouse=True)
def scio():
    """
    Init ScienceIO client, using .scio/config
    :return: our client
    """
    yield ScienceIO()


def test_input_is_string(scio):
    """
    Test providing something other than a string returns an error
    """
    # Invalid types.
    with pytest.raises(HTTPError, match="none is not an allowed value"):
        scio.annotate(text=None)

    with pytest.raises(HTTPError, match="str type expected"):
        scio.annotate(text={})

    with pytest.raises(HTTPError, match="str type expected"):
        scio.annotate(text={"nested": "dict"})

    # TODO: Uncomment when this is working in NRT.
    # with pytest.raises(HTTPError, match="str type expected"):
    #     scio.annotate(text=123)

    # Empty strings should be rejected.
    with pytest.raises(HTTPError, match="ensure this value has at least 1 characters"):
        scio.annotate(text="")

    scio.structure(text="normal strings should work just fine")


def test_structure(scio, snapshot):
    """
    Test structure request with a small text snippet
    """

    response = scio.structure(text=QUERY_TEXT)

    assert isinstance(response, dict)

    # Ensure floating-point keys exist in spans, but scrub them out since they
    # may vary in value from run to run slightly and are not always comparable.
    for span in response["spans"]:
        del span["score_id"]
        del span["score_type"]

    assert response == snapshot


def test_async_annotation(scio):
    """
    Test async structure request with a small text snippet.
    """
    request_id = scio.send_structure_request(text=QUERY_TEXT)

    # The request id would be a valid UUID string.
    assert isinstance(request_id, str)
    uuid.UUID(request_id)

    time.sleep(10)

    response = scio.get_structure_response(request_id)

    assert isinstance(response, dict)


def test_async_def_annotation(scio, snapshot):
    """
    Test async structure request with a small text snippet.
    """
    import asyncio

    response = asyncio.run(scio.structure_async(text=QUERY_TEXT))

    assert isinstance(response, dict)

    # Ensure floating-point keys exist in spans, but scrub them out since they
    # may vary in value from run to run slightly and are not always comparable.
    for span in response["spans"]:
        del span["score_id"]
        del span["score_type"]

    assert response == snapshot
