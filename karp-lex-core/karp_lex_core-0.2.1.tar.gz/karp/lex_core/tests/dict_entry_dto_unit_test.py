from karp.lex_core.dtos import EntryDtoDict


def test_can_create_entry_dto():
    entry_dto = EntryDtoDict(entry={"field": "value"})

    assert entry_dto.last_modified is None
    assert entry_dto.last_modified_by is None


def test_can_create_entry_dto_with_last_modified_by():
    entry_dto = EntryDtoDict(
        entry={"field": "value"}, lastModifiedBy="username@example.com"
    )

    assert entry_dto.last_modified is None
    assert entry_dto.last_modified_by == "username@example.com"
