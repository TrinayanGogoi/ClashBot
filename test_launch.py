from modules.emulator import LDPlayer

emulator = LDPlayer()

emulator.start()
emulator.wait_for_device()
emulator.wait_for_boot()

emulator.launch_app(emulator.config["game"]["package"])

print("\nEverything completed successfully.")