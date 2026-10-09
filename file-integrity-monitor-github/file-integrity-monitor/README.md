# File Integrity Monitor

A beginner-friendly Python desktop application that compares two files using **SHA-256 hashes**. It provides a graphical interface built with Tkinter and displays both hashes and the comparison result.

## Features

- Select two files through a file picker.
- Calculate SHA-256 hashes without loading an entire large file into memory.
- Compare file contents using their hashes.
- Display both hashes and a clear match/mismatch result.
- Handle missing selections and file-reading errors.
- Includes automated unit tests and sample files.

## Requirements

- Python 3.10 or later recommended.
- Tkinter (usually included with standard Python installations; some Linux distributions package it separately).
- No third-party Python packages are required.

## Run the application

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

```bash
python main.py
```

On some Linux systems, install the Tkinter package first (for example, `python3-tk` on Debian/Ubuntu).

## Test the project

Run the automated tests from the project folder:

```bash
python -m unittest discover -s tests -v
```

## Sample files

The `sample_files/` folder contains two example text files with different contents. Open the application and select both to see a mismatch. To test a match, select the same file twice.

## How it works

1. The program reads each file in 1 MiB chunks.
2. `hashlib.sha256()` calculates a 256-bit digest for each file.
3. The program compares the resulting hexadecimal hash strings.
4. Matching hashes strongly indicate matching file contents; different hashes indicate that the files differ.

## Project structure

```text
file-integrity-monitor/
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
├── LICENSE
├── sample_files/
│   ├── original_config.txt
│   └── modified_config.txt
└── tests/
    └── test_integrity.py
```

## Limitations and security notes

- This is a **file comparison tool**, not a continuous background monitor. It only checks files when you click **Compare files**.
- A matching hash indicates matching content with extremely high confidence, but does not prove who created a file or whether it is trustworthy.
- The application does not modify, delete, quarantine, or upload selected files.
- SHA-256 is used for integrity comparison, not password storage.
- It does not currently maintain a trusted baseline, monitor folders, or generate audit logs.

## Possible future improvements

- Monitor a folder and alert when a file changes.
- Save a baseline manifest of file hashes.
- Export comparison results to CSV or JSON.
- Add a progress indicator for very large files.
- Package the application for Windows.

## Resume description

**File Integrity Monitor | Python, Tkinter, hashlib**

Developed a desktop utility that compares files using SHA-256 cryptographic hashes to identify content differences. Implemented chunk-based file reading, GUI file selection, error handling, and unit tests.

## Interview explanation

> I built a Python desktop application that compares two files using SHA-256. It reads files in chunks, calculates each file's hash, and compares the digests. If the hashes match, the file contents are considered identical with very high confidence; if they differ, the application reports an integrity difference. The current version is an on-demand comparison tool rather than a continuous monitoring service.
