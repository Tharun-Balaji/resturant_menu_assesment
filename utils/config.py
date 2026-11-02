import os


def load_system_prompt() -> str:
    """Load the system prompt from prompt.txt file."""
    prompt_path : str = ''
    try:

        # config.py -> utils -> project root
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # Go to the parent directory of the parent directory
        prompt_path = os.path.join(
            current_dir,
            "..",
            "prompt.txt"
        )

        with open(prompt_path, "r", encoding="utf-8") as file:
            return file.read().strip()

    except FileNotFoundError:
        raise FileNotFoundError(
            f"prompt.txt not found at expected location: {prompt_path}"
        )

    except Exception as e:
        raise RuntimeError(
            f"Error loading system prompt: {e}"
        )


def get_system_prompt() -> str:
    """Get the system prompt."""

    return load_system_prompt()


# Export the system prompt
SYSTEM_PROMPT = get_system_prompt()
