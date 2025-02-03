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
        Validates user input to prevent shell injection.
        :param user_input: Input from the user.
        :return: Sanitized input.
        """
        if ";" in user_input or "&" in user_input or "|" in user_input:
            raise ValueError("Invalid input detected!")
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

# Example Usage
if __name__ == "__main__":
    security = SecurityEnhancements()

    # Secure Hashing
    secure_hash_value = security.secure_hash("my_secure_data")
    print(f"Secure Hash: {secure_hash_value}")

    # Secure Subprocess Execution
    command_output = security.safe_subprocess(["ls", "-l"])
    print(f"Subprocess Output: {command_output.stdout}")

    # Secure Temporary File
    temp_file_path = security.secure_temp_file()
    print(f"Secure Temp File: {temp_file_path}")

    # Input Validation Example
    try:
        validated_input = security.validate_input("safe_input")
        print(f"Validated Input: {validated_input}")
    except ValueError as e:
        print(e)
