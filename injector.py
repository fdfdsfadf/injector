import time
import keyboard

# Global counter initialization
counter = 0

def sequential_type():
    global counter
    
    if counter > 9999:
        print("Reached 9999. Process stopped.")
        return

    # 1. Format the current sequence number to exactly 4 digits
    formatted_number = f"{counter:04d}"
    
    # 2. Release Ctrl and V keys virtually so they don't corrupt the string
    keyboard.release("ctrl")
    keyboard.release("v")
    time.sleep(0.01)  # Minimal delay to allow OS to process the release

    # 3. Simulate direct physical hardware typing string instead of pasting
    keyboard.write(formatted_number)
    
    print(f"Successfully typed: {formatted_number}")
    
    # 4. Increment the sequence counter for the next trigger
    counter += 1

def main():
    print("====================================================")
    print("  SUCCESS: Sequential Typing Script Is Live!")
    print("====================================================")
    print(" -> Click inside any text box or application.")
    print(" -> Press 'Ctrl + V' to automatically type numbers.")
    print(" -> Press 'Ctrl + Shift + Q' to safely turn off script.")
    print("====================================================")

    # Use add_hotkey with immediate suppression to catch the system event
    keyboard.add_hotkey("ctrl+v", sequential_type, suppress=True, trigger_on_release=True)

    # Standard exit wait loop
    keyboard.wait("ctrl+shift+q")
    print("\nScript terminated safely.")

if __name__ == "__main__":
    main()
