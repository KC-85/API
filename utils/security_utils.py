import hashlib
import subprocess
import os
import tempfile
import secrets
import re
import logging

# Set up logging for security events
logging.basicConfig(
    filename="security.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class SecurityEnhancements:
    """
    Security Enhancements for API.
    - Uses SHA-256 instead of SHA-1 for hashing.
    - Executes shell commands securely.
    - Uses a secure temporary directory.
    - Implements enhanced input validation.
    """

    @staticmethod
    def secure_hash(data: str) -> str:
        """Use SHA-256 instead of SHA-1 for secure hashing."""
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    @staticmethod
    def safe_subprocess(command: list) -> subprocess.CompletedProcess:
        """
        Executes subprocess securely without shell=True.
        Prevents risky commands from executing.
        :param command: List of command arguments.
        :return: subprocess.CompletedProcess object.
        """
        blocked_commands = ["rm", "dd", "mkfs", "shutdown", "reboot"]
        if any(cmd in command for cmd in blocked_commands):
            logging.warning(f"Blocked attempt to execute: {command}")
            raise ValueError("Command execution is not allowed!")

        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result
        except subprocess.CalledProcessError as e:
            logging.error(f"Subprocess execution failed: {e}")
            return f"Error: {e}"

    @staticmethod
    def validate_input(user_input: str) -> str:
        """
        Validates user input using regex to prevent shell injection.
        :param user_input: Input from the user.
        :return: Sanitized input.
        """
        pattern = re.compile(r"^[a-zA-Z0-9_.-]+$")  # Allow only safe characters
        if not pattern.match(user_input):
            logging.warning(f"Invalid input detected: {user_input}")
            raise ValueError("Invalid input detected!")
        return user_input

    @staticmethod
    def secure_temp_file() -> str:
        """
        Creates a secure temporary file instead of using /tmp.
        Uses NamedTemporaryFile for better security.
        :return: Path to the temp file.
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        return temp_file.name


# Example Usage
if __name__ == "__main__":
    security = SecurityEnhancements()

    # Secure Hashing
    secure_hash_value = security.secure_hash("my_secure_data")
    print(f"Secure Hash: {secure_hash_value}")

    # Secure Subprocess Execution
    try:
        command_output = security.safe_subprocess(["ls", "-l"])
        print(f"Subprocess Output: {command_output.stdout}")
    except ValueError as err:
        print(err)

    # Secure Temporary File
    temp_file_path = security.secure_temp_file()
    print(f"Secure Temp File: {temp_file_path}")

    # Input Validation Example
    try:
        validated_input = security.validate_input("safe_input")
        print(f"Validated Input: {validated_input}")
    except ValueError as e:
        print(e)
