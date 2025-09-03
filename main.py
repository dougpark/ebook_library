from LibraryScanner import LibraryScanner

if __name__ == "__main__":
    folder_to_scan = "test_books"

    scanner = LibraryScanner()
    ebooks = scanner.scan_folder(folder_to_scan)

    # Example: Print results (could be turned into HTML later)
    for ebook in ebooks:
        meta = ebook["metadata"]
        print(f"File: {ebook['file_path']}")
        print(f"  Title : {meta['title']}")
        print(f"  Author: {meta['author']}")
        print(f"  Date  : {meta['date_published']}")
        print()