# Bundled ADB

This folder contains a Windows `adb.exe` and its two required DLLs
(`AdbWinApi.dll`, `AdbWinUsbApi.dll`) so you don't need to install Android
Platform Tools separately.

All three files must stay together in the same folder — `adb.exe` loads the
DLLs at runtime and won't work without them next to it.

## Using it

In `config/config.yaml`, set:

```yaml
device:
  adb_path: "tools/adb/adb.exe"
```

Then confirm it works from your project folder in Command Prompt:

```
tools\adb\adb.exe version
tools\adb\adb.exe devices
```

If `adb devices` shows your emulator (as `device`, not `unauthorized` or
`offline`), you're set — `main.py` will use this same binary automatically.

## If you'd rather add it to PATH instead

You can still do it the "normal" way if you prefer — add this folder to your
Windows PATH environment variable, and leave `adb_path: "adb"` in the config.
Either approach works; using the bundled path above just avoids editing
system PATH at all.
