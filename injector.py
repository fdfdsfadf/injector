import time
from pynput import keyboard

# Initialize the counter
counter = 0

# Track the state of the Ctrl key
ctrl_pressed = False

# Create a controller to simulate typing
keyboard_controller = keyboard.Controller()

def on_press(key):
    global counter, ctrl_pressed
    
    # Check if Ctrl is being held down
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = True
        return

    # Check if 'v' is pressed while Ctrl is held down
    if ctrl_pressed and hasattr(key, 'char') and key.char == 'v':
        if counter <= 9999:
            # Format to 4 digits (e.g., 0000, 0001)
            formatted_number = f"{counter:04d}"
            
            # Backspace to remove the 'v' that Windows might register
            # and type the sequential number instead
            keyboard_controller.tap(keyboard.Key.backspace)
            keyboard_controller.type(formatted_number)
            
            print(f"Typed: {formatted_number}")
            counter += 1
            
            # Stop pynput from passing the original 'Ctrl+V' to Windows
            return False 

def on_release(key):
    global ctrl_pressed
    # Reset Ctrl state when released
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False
        
    # Safety exit shortcut: Press Escape to close the script
    if key == keyboard.Key.esc:
        print("Exiting script...")
        return False

def main():
    print("Script is running smoothly...")
    print("Press 'Ctrl + V' to paste sequentially (0000 -> 9999).")
    print("Press 'Escape' to completely exit the script.")

    # Start listening to global keyboard events
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    main()
