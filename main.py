import subprocess
import re
from typing import Dict, List

bookPath: str = "./books/frankenstein.txt"


def bookLen(fileContents: str) -> int:
    return len(fileContents.split())


def charList(fileContents: str) -> Dict[str, int]:
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


def getParagraph(lines: List[str], selectedLineNumber: int) -> str:
    paragraphs: List[tuple[int, str]] = []
    currentParagraph: List[str] = []
    currentLineNumber: int = 0

    for line in lines:
        currentLineNumber += 1
        if line.strip():
            currentParagraph.append(line.strip())
        else:
            if currentParagraph:
                paragraphs.append(
                    (
                        currentLineNumber - len(currentParagraph),
                        "\n".join(currentParagraph),
                    )
                )
            currentParagraph = []

    if currentParagraph:
        paragraphs.append(
            (currentLineNumber - len(currentParagraph), "\n".join(currentParagraph))
        )

    for startLine, paragraph in paragraphs:
        linesInParagraph = paragraph.splitlines()
        endLine = startLine + len(linesInParagraph) - 1
        if startLine <= selectedLineNumber <= endLine:
            return paragraph

    return ""


def wordSearch(fileContents: str, searchWord: str) -> None:
    searchPattern: str = re.escape(searchWord.lower()) + r"\b"

    lines: List[str] = fileContents.splitlines()
    results: list[str] = []

    for lineNumber, line in enumerate(lines, start=1):
        if re.search(searchPattern, line.lower()):
            results.append(f"Line {lineNumber}: {line.strip()}")

    if results:
        resultsStr: str = "\n".join(results)

        selected: str = subprocess.run(
            ["fzf"], input=resultsStr, text=True, capture_output=True
        ).stdout.strip()

        if selected:
            selectedLineNumber = int(selected.split(":")[0].split()[1])
            paragraph = getParagraph(lines, selectedLineNumber)

            print(f"Selected line: {selected}")
            print("\n Full paragraph: \n")
            print(paragraph)
        else:
            print("No selection made")
    else:
        print(f"No occurrences of the word '{searchWord}' found.")


def main() -> None:
    with open(bookPath) as f:
        fileContents: str = f.read()

    bookLength = bookLen(fileContents)
    print(f"{bookLength} words found in the document")

    charCount = charList(fileContents.lower())

    for char, count in charCount.items():
        print(f"The '{char}' character was found {count} times")

    userSearchWord: str = str(input("What word would you like to search: "))
    wordSearch(fileContents, userSearchWord)


if __name__ == "__main__":
    main()
