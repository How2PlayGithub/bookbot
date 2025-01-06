from typing import Dict

bookPath: str = "./books/frankenstein.txt"


def bookLen(fileContents: str) -> int:
    return len(fileContents.split())


def charList(fileContents: str) -> Dict[str, int]:
    fileContents.split()
    charCount: Dict[str, int] = {}

    for char in fileContents:
        if char.isalpha():
            char = char.lower()
            if char in charCount:
                charCount[char] += 1
            else:
                charCount[char] = 1

    charCountOrdered: Dict[str, int] = dict(sorted(charCount.items()))

    return charCountOrdered


def main() -> None:
    with open(bookPath) as f:
        fileContents: str = f.read()

    # Outputting book length

    bookLength = bookLen(fileContents)
    print(f"{bookLength} words found in the document")

    # Outputting character count

    charCount = charList(fileContents.lower())

    for char, count in charCount.items():
        print(f"The '{char}' character was found {count} times")


if __name__ == "__main__":
    main()
