import os
import subprocess
import re
from typing import Dict, List


def bookSearch(booksDirectory: str) -> str:
    if not os.path.exists(booksDirectory) or not os.path.isdir(booksDirectory):
        raise ValueError(f"Directory {booksDirectory} does not exist!")

    try:
        selectedFile = subprocess.check_output(
            ["fzf", "--preview", "echo {}"], cwd=booksDirectory, text=True
        ).strip()

        if selectedFile:
            return os.path.join(booksDirectory, selectedFile)
        else:
            return "No file selected."
    except subprocess.CalledProcessError:
        return "Error running fzf or no file selected."


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
    bookPath: str = "./books/"
    bookPath = bookSearch(bookPath)

    with open(bookPath) as f:
        fileContents: str = f.read()

    bookLength: int = bookLen(fileContents)
    charCount: Dict[str, int] = charList(fileContents.lower())
    validUserOptions: List[int] = [1, 2, 3]

    print("Bookbot!")
    print("Option 1: book length")
    print("Option 2: character count")
    print("Option 3: word search")

    while True:
        try:
            userOption: int = int(input("What option would you like: "))
            if userOption in validUserOptions:
                break
        except ValueError:
            print("Please enter the number")

    if userOption == 1:
        print(bookLength)
    elif userOption == 2:
        for char, count in charCount.items():
            print(f"The '{char}' character was found {count} times")
    elif userOption == 3:
        userSearchWord: str = str(input("What word would you like to search: "))
        wordSearch(fileContents, userSearchWord)


if __name__ == "__main__":
    main()
