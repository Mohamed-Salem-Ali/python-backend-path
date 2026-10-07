"""Part B of the week 1 project. See README.md in this folder."""


def add_contact(book: list, name: str, phone: str, tags=()) -> bool:
    """Add a contact; return False (and change nothing) if the name already exists."""
    # TODO
    ...


def find(book: list, text: str) -> list:
    """Contacts whose name contains `text`, case-insensitive."""
    # TODO
    ...


def by_tag(book: list) -> dict:
    """{tag: [names]} for every tag used in the book."""
    # TODO
    ...


def format_contact(c: dict) -> str:
    """'Name | phone | tag1, tag2'"""
    # TODO
    ...


def main() -> None:
    """Menu loop: add, search, list, quit."""
    # TODO (last step: use while True, input(), break)
    ...


if __name__ == "__main__":
    book: list = []
    assert add_contact(book, "Ali", "0100", ["family"]) is True
    assert add_contact(book, "Sara", "0111", ["friend", "family"]) is True
    assert add_contact(book, "Ali", "0122") is False
    assert len(book) == 2
    assert [c["name"] for c in find(book, "al")] == ["Ali"]
    assert by_tag(book) == {"family": ["Ali", "Sara"], "friend": ["Sara"]}
    assert format_contact(book[1]) == "Sara | 0111 | friend, family"
    print("All checks passed")
    # main()  # uncomment when the menu is written
