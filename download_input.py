"""
Advent of Code Input Downloader

Downloads puzzle input from adventofcode.com using Firefox session cookies.
Run from within a day directory (e.g., 01/) to automatically download that day's input.

Usage:
    cd 01/
    python ../download_input.py
"""

import sys
from pathlib import Path
from typing import Optional

import requests
from rich import print


# Custom Exceptions

class DayDetectionError(ValueError):
    """Raised when day number cannot be detected from directory name."""
    pass


class CookieError(RuntimeError):
    """Raised when session cookie cannot be extracted."""
    pass


class DownloadError(RuntimeError):
    """Raised when input download fails."""
    pass


# Core Functions

def detect_day_number() -> int:
    """
    Detect the day number from the current working directory name.

    Returns:
        int: Day number (1-25)

    Raises:
        DayDetectionError: If directory format is invalid or day is out of range
    """
    cwd = Path.cwd()
    dir_name = cwd.name

    # Try to parse as integer
    try:
        day = int(dir_name)
    except ValueError as e:
        raise DayDetectionError(
            f"Directory name '{dir_name}' is not a valid day number. "
            f"Expected format: two-digit day (01-25)"
        ) from e

    # Validate range
    if not 1 <= day <= 25:
        raise DayDetectionError(
            f"Day {day} is out of valid range (1-25)"
        )

    return day


def get_session_cookie() -> str:
    """
    Extract Advent of Code session cookie from Firefox.

    Returns:
        str: Session cookie value

    Raises:
        CookieError: If cookie cannot be found or extracted
    """
    try:
        import browser_cookie3
    except ImportError as e:
        raise CookieError(
            "browser-cookie3 library not found. "
            "Install with: pip install browser-cookie3"
        ) from e

    try:
        # Get Firefox cookies for adventofcode.com
        cj = browser_cookie3.firefox(domain_name='adventofcode.com')

        # Extract session cookie
        for cookie in cj:
            if cookie.name == 'session':
                return cookie.value

        # Cookie not found
        raise CookieError(
            "Session cookie not found in Firefox. "
            "Please log in to adventofcode.com in Firefox first."
        )

    except Exception as e:
        if isinstance(e, CookieError):
            raise
        raise CookieError(
            f"Failed to extract cookies from Firefox: {e}"
        ) from e


def download_input(day: int, session: str, year: int = 2025) -> str:
    """
    Download puzzle input from adventofcode.com.

    Args:
        day: Day number (1-25)
        session: Session cookie value
        year: Year (default: 2025)

    Returns:
        str: Puzzle input content

    Raises:
        DownloadError: If download fails for any reason
    """
    url = f"https://adventofcode.com/{year}/day/{day}/input"

    # Prepare request with session cookie
    cookies = {'session': session}
    headers = {
        'User-Agent': 'github.com/tcgarvin/adventOfCode2025 by @tcgarvin'
    }

    try:
        response = requests.get(url, cookies=cookies, headers=headers, timeout=30)

        # Check for various error conditions
        if response.status_code == 404:
            raise DownloadError(
                f"Day {day} input not found. "
                f"The puzzle may not be available yet."
            )
        elif response.status_code == 400:
            raise DownloadError(
                f"Bad request for day {day}. "
                f"Check that the day number is valid."
            )
        elif response.status_code in (401, 403):
            raise DownloadError(
                "Authentication failed. "
                "Your session cookie may be expired. "
                "Please log in to adventofcode.com in Firefox again."
            )
        elif response.status_code == 500:
            raise DownloadError(
                "Advent of Code server error. "
                "Please try again later."
            )
        elif not response.ok:
            raise DownloadError(
                f"Download failed with status {response.status_code}: "
                f"{response.text[:200]}"
            )

        # Validate we got actual input
        content = response.text
        if not content or content.strip() == '':
            raise DownloadError(
                f"Downloaded input for day {day} is empty"
            )

        return content

    except requests.RequestException as e:
        raise DownloadError(
            f"Network error downloading input: {e}"
        ) from e


def save_input(content: str, output_path: Path) -> None:
    """
    Save puzzle input to file.

    Args:
        content: Puzzle input content
        output_path: Path to save file

    Raises:
        OSError: If file cannot be written
    """
    try:
        # Create parent directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write content
        output_path.write_text(content, encoding='utf-8')

    except OSError as e:
        raise OSError(
            f"Failed to write input to {output_path}: {e}"
        ) from e


def main() -> None:
    """
    Main entry point for the script.

    Detects day from current directory, downloads input from adventofcode.com,
    and saves to input.txt in the current directory.
    """
    try:
        # Detect day from directory name
        day = detect_day_number()
        print(f"Detected day: {day}")

        # Get session cookie from Firefox
        print("Extracting session cookie from Firefox...")
        session = get_session_cookie()

        # Download input
        print(f"Downloading input for day {day}, year 2025...")
        content = download_input(day, session, year=2025)

        # Save to current directory
        output_path = Path.cwd() / "input.txt"
        save_input(content, output_path)

        print(f"Successfully saved input to {output_path}")
        print(f"Input size: {len(content)} bytes")

    except (DayDetectionError, CookieError, DownloadError, OSError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled by user", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
