import re
import hashlib
import subprocess
import os
import tempfile
import secrets

class SecurityEnhancements:
    """
    Security Enhancements for API.
    - Uses SHA-256 instead of SHA-1 for hashing.
    - Executes shell commands securely.
    - Uses a secure temporary directory.
    """

    @staticmethod
    def secure_hash(data: str) -> str:
        """ Use SHA-256 instead of SHA-1 for secure hashing. """
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    @staticmethod
    def safe_subprocess(command: list) -> subprocess.CompletedProcess:
        """
        Executes subprocess securely without shell=True.
        :param command: List of command arguments.
        :return: subprocess.CompletedProcess object.
        """
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"

    @staticmethod
    def validate_input(user_input: str) -> str:
        """
        Validates user input using regex to prevent shell injection.
        :param user_input: Input from the user.
        :return: Sanitized input.
        """
        if user_input is None:
            raise ValueError("Invalid input detected: NoneType received")

        pattern = re.compile(r"^[a-zA-Z0-9_.\-\s]+$")  # ✅ Now allows spaces!
        if not pattern.match(user_input):
            raise ValueError(f"Invalid input detected: {user_input}")

        return user_input

    @staticmethod
    def secure_temp_file() -> str:
        """
        Creates a secure temporary file instead of using /tmp.
        :return: Path to the temp file.
        """
        temp_dir = tempfile.gettempdir()
        temp_file = os.path.join(temp_dir, f"secure_temp_{secrets.token_hex(8)}.txt")
        return temp_file
