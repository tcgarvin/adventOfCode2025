"""
Advent of Code Day Setup Script

Sets up a new Advent of Code day with directory, template, and input download.

Usage:
    python setup_day.py <day>

Examples:
    python setup_day.py 5
    python setup_day.py 05
"""

import sys
import shutil
from pathlib import Path
from typing import Union

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


# Utility Functions

def format_day_number(day: Union[int, str]) -> str:
    """
    Format day number with zero-padding.

    Args:
        day: Day number as int (5) or str ("05", "5")

    Returns:
        Zero-padded string ("01" through "25")

    Raises:
        ValueError: If day is not 1-25
    """
    try:
        day_int = int(day)
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid day: {day}. Expected integer 1-25.") from e

    if not 1 <= day_int <= 25:
        raise ValueError(f"Day {day_int} out of range. Advent of Code has days 1-25.")

    return f"{day_int:02d}"


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


def setup_day_directory(day: Union[int, str], year: int = 2025) -> None:
    """
    Set up directory structure for a specific Advent of Code day.

    Creates:
    - {day}/ directory
    - {day}/{day}.py from template
    - {day}/input.txt (if available)

    Args:
        day: Day number (1-25), accepts int or str
        year: Year (default: 2025)

    Raises:
        ValueError: If day out of range
        CookieError: If session cookie unavailable
        OSError: If file operations fail
    """
    # Format and validate day number
    day_str = format_day_number(day)
    day_int = int(day_str)

    # Get script directory (where this script lives)
    script_dir = Path(__file__).parent

    print(f"Setting up day {day_str}...")

    # 1. Create directory
    day_dir = script_dir / day_str
    if day_dir.exists():
        print(f"Directory {day_str}/ already exists")
    else:
        day_dir.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory {day_str}/")

    # 2. Copy template
    template_path = script_dir / "template.py"
    solution_file = day_dir / f"{day_str}.py"

    if solution_file.exists():
        print(f"⚠ Skipping {day_str}.py (already exists)")
    else:
        if not template_path.exists():
            raise OSError(f"Template file not found: {template_path}")
        shutil.copy(template_path, solution_file)
        print(f"✓ Created {day_str}.py from template")

    # 3. Download input (graceful degradation)
    input_file = day_dir / "input.txt"

    if input_file.exists():
        size = input_file.stat().st_size
        print(f"⚠ Skipping input.txt (already exists, {size} bytes)")
    else:
        try:
            # Get session cookie
            print("Extracting session cookie from Firefox...")
            session = get_session_cookie()

            # Download input
            print(f"Downloading input for day {day_int}, year {year}...")
            content = download_input(day_int, session, year)

            # Save to file
            input_file.write_text(content, encoding='utf-8')
            print(f"✓ Downloaded input.txt ({len(content)} bytes)")

        except DownloadError as e:
            # Graceful degradation for missing inputs
            error_msg = str(e).lower()
            if "not found" in error_msg or "not be available" in error_msg:
                print(f"⚠ Input not available yet for day {day_int}")
                print(f"  You can download it later with: cd {day_str} && python ../download_input.py")
            else:
                # Re-raise for auth/network errors
                raise

        except (CookieError, OSError) as e:
            # Critical errors
            print(f"✗ Failed to download input: {e}", file=sys.stderr)
            raise

    # Success message
    print()
    print(f"Setup complete! To get started:")
    print(f"  cd {day_str}")
    print(f"  python {day_str}.py --example  # (create example.txt first)")
    print(f"  python {day_str}.py            # Run with input.txt")


def main() -> None:
    """
    Main entry point for the script.

    Parses command-line arguments and sets up the day directory.
    """
    # Check arguments
    if len(sys.argv) != 2:
        print("Usage: python setup_day.py <day>", file=sys.stderr)
        print("  day: Integer 1-25", file=sys.stderr)
        sys.exit(1)

    try:
        day = sys.argv[1]
        setup_day_directory(day, year=2025)

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Usage: python setup_day.py <day>", file=sys.stderr)
        print("  day: Integer 1-25", file=sys.stderr)
        sys.exit(1)

    except (CookieError, OSError, DownloadError) as e:
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
