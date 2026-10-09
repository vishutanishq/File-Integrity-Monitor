"""File Integrity Monitor - compare files using SHA-256 hashes."""

from __future__ import annotations

import hashlib
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk


CHUNK_SIZE = 1024 * 1024  # Read files in 1 MiB chunks.


def calculate_sha256(file_path: str | Path) -> str:
    """Return the SHA-256 digest for a file without loading it all into memory."""
    digest = hashlib.sha256()
    with Path(file_path).open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compare_files(first_path: str | Path, second_path: str | Path) -> dict[str, object]:
    """Compare two files and return their paths, hashes, and equality status."""
    first_hash = calculate_sha256(first_path)
    second_hash = calculate_sha256(second_path)
    return {
        "first_path": str(first_path),
        "second_path": str(second_path),
        "first_hash": first_hash,
        "second_hash": second_hash,
        "identical": first_hash == second_hash,
    }


class FileIntegrityMonitor:
    """Small Tkinter GUI for comparing two selected files."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("File Integrity Monitor")
        self.root.geometry("760x520")
        self.root.minsize(640, 460)
        self.first_path: str | None = None
        self.second_path: str | None = None

        self._build_ui()

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=22)
        outer.pack(fill="both", expand=True)

        ttk.Label(
            outer, text="File Integrity Monitor", font=("Segoe UI", 20, "bold")
        ).pack(anchor="w")
        ttk.Label(
            outer,
            text="Compare two files using their SHA-256 cryptographic hashes.",
        ).pack(anchor="w", pady=(4, 18))

        self.first_label = self._file_row(outer, "File 1", self.select_first_file)
        self.second_label = self._file_row(outer, "File 2", self.select_second_file)

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=(18, 10))
        ttk.Button(actions, text="Compare files", command=self.compare_selected).pack(
            side="left"
        )
        ttk.Button(actions, text="Clear selection", command=self.clear_selection).pack(
            side="left", padx=(10, 0)
        )

        ttk.Label(outer, text="Result", font=("Segoe UI", 12, "bold")).pack(
            anchor="w", pady=(14, 4)
        )
        self.status_label = ttk.Label(
            outer, text="Select two files to begin.", wraplength=700
        )
        self.status_label.pack(anchor="w", pady=(0, 12))

        ttk.Label(outer, text="SHA-256 hashes", font=("Segoe UI", 12, "bold")).pack(
            anchor="w", pady=(4, 4)
        )
        self.hash1_label = ttk.Label(outer, text="File 1: —", wraplength=700)
        self.hash1_label.pack(anchor="w", pady=3)
        self.hash2_label = ttk.Label(outer, text="File 2: —", wraplength=700)
        self.hash2_label.pack(anchor="w", pady=3)

        ttk.Label(
            outer,
            text=(
                "Note: matching hashes strongly indicate identical file contents. "
                "This tool compares files on demand; it does not continuously monitor changes."
            ),
            wraplength=700,
        ).pack(anchor="w", pady=(20, 0))

    @staticmethod
    def _file_row(parent: ttk.Frame, title: str, command) -> ttk.Label:
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=7)
        ttk.Button(row, text=f"Choose {title}", command=command).pack(side="left")
        label = ttk.Label(row, text="No file selected", wraplength=530)
        label.pack(side="left", padx=(12, 0), fill="x", expand=True)
        return label

    def select_first_file(self) -> None:
        selected = filedialog.askopenfilename(title="Select the first file")
        if selected:
            self.first_path = selected
            self.first_label.config(text=selected)
            self._reset_result()

    def select_second_file(self) -> None:
        selected = filedialog.askopenfilename(title="Select the second file")
        if selected:
            self.second_path = selected
            self.second_label.config(text=selected)
            self._reset_result()

    def _reset_result(self) -> None:
        self.status_label.config(text="Ready to compare the selected files.")
        self.hash1_label.config(text="File 1: —")
        self.hash2_label.config(text="File 2: —")

    def clear_selection(self) -> None:
        self.first_path = None
        self.second_path = None
        self.first_label.config(text="No file selected")
        self.second_label.config(text="No file selected")
        self._reset_result()

    def compare_selected(self) -> None:
        if not self.first_path or not self.second_path:
            messagebox.showwarning(
                "Files required", "Please select both files before comparing."
            )
            return

        try:
            result = compare_files(self.first_path, self.second_path)
        except OSError as error:
            messagebox.showerror("File error", f"Could not read a selected file:\n{error}")
            return

        self.hash1_label.config(text=f"File 1: {result['first_hash']}")
        self.hash2_label.config(text=f"File 2: {result['second_hash']}")

        if result["identical"]:
            self.status_label.config(text="MATCH — file contents are identical.")
            messagebox.showinfo("Comparison complete", "The files have matching SHA-256 hashes.")
        else:
            self.status_label.config(text="MISMATCH — file contents are different.")
            messagebox.showwarning(
                "Integrity difference detected",
                "The files have different SHA-256 hashes.",
            )


def main() -> None:
    root = tk.Tk()
    FileIntegrityMonitor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
