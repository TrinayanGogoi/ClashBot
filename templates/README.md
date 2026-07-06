# Templates

This project ships with **no game artwork**. Clash of Clans' icons, art, and
UI are Supercell's IP, so you need to capture your own template crops from
your own running game client. This is also just more robust in practice,
since it guarantees the templates match your exact emulator resolution/scale.

## How to capture a template

1. Get the bot's raw screenshot tool to save a full screenshot:
   ```python
   from src.adb_controller import ADBController
   import cv2
   adb = ADBController(serial="127.0.0.1:5555")
   cv2.imwrite("full_screen.png", adb.screenshot())
   ```
2. Open `full_screen.png` in any image editor (GIMP, Photoshop, even MS Paint).
3. Crop tightly around just the icon/button you want to detect (no extra
   background if you can help it -- tighter crops match more reliably).
4. Save the crop as a `.png` into the matching folder below, using the
   expected filename (no extension needed elsewhere in code -- the loader
   strips it automatically).

## Expected folder / naming layout

```
templates/
  buttons/
    attack.png
    find_match.png
    next.png
    end_battle.png
    surrender.png
    return_home.png
    donate.png
    barracks.png
  resources/
    gold_mine_full.png
    elixir_collector_full.png
    dark_elixir_drill_full.png
  troops/
    barbarian.png
    archer.png
    ... one per troop you want the bot to recognize
```

## Tips for reliable matches

- Capture templates at the **same zoom level** you'll actually run the bot at.
- Avoid including animated/particle effects in the crop (they change frame to
  frame and hurt match confidence).
- If a button has multiple visual states (e.g. "Attack" button pulsing), you
  may want two template variants and use `find_any()`.
- Start `vision.match_threshold` around 0.82 in config.yaml and tune from there
  -- too high and legitimate matches get missed after minor art/resolution
  differences; too low and you get false positives.
