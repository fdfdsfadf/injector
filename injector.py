import time
import keyboard
import pyperclip

# Initialize the counter
counter = 0

def sequential_paste():
    global counter
    
    # Ignore if counter exceeds 9999
    if counter > 9999:
        print("Reached 9999. Stopping increment.")
        return

    # Format the number to always be 4 digits (e.g., 0000, 0001)
    formatted_number = f"{counter:04d}"
    
    # Save the current clipboard content so we can restore it later
    try:
        original_clipboard = pyperclip.paste()
    except Exception:
        original_clipboard = ""

    # Copy the formatted number to the clipboard
    pyperclip.copy(formatted_number)

    # Briefly release Ctrl+V to prevent infinite loops, then simulate the paste
    time.sleep(0.05)
    keyboard.send("ctrl+v")
    time.sleep(0.05)

    # Restore original clipboard content
    if original_clipboard:
        pyperclip.copy(original_clipboard)

    print(f"Pasted: {formatted_number}")
    
    # Increment the counter for the next press
    counter += 1

def main():
    print("Script is running...")
    print("Press 'Ctrl + V' to paste sequentially (0000 -> 9999).")
    print("Press 'Ctrl + Shift + Q' to exit the script.")

    # Override Ctrl+V with our custom function
    # trigger_on_release=True prevents the hotkey from firing repeatedly if held down
    keyboard.add_hotkey("ctrl+v", sequential_paste, trigger_on_release=True)

    # Add a safety exit hotkey
    keyboard.wait("ctrl+shift+q")

if __name__ == "__main__":
    main()
