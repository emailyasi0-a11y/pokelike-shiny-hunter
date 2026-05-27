# Pokelike Shiny Hunter

Automated shiny hunter for [pokelike.xyz](https://pokelike.xyz), a browser-based Pokemon roguelike.

The script opens Chrome, lets you log in and set up your run manually, then takes over and resets in a loop until a shiny Pokemon appears — either any shiny or a specific one you choose.

```
__________       __          .__  .__ __
\______   \____ |  | __ ____ |  | |__|  | __ ____
 |     ___/  _ \|  |/ // __ \|  | |  |  |/ // __ \
 |    |  (  <_> )    <\  ___/|  |_|  |    <\  ___/
 |____|   \____/|__|_ \\___  >____/__|__|_ \\___  >
                     \/    \/             \/    \/

  _________.__    .__              .__                  __
 /   _____/|  |__ |__| ____ ___.__.|  |__  __ __  _____/  |_  ___________
 \_____  \ |  |  \|  |/    <   |  ||  |  \|  |  \/    \   __\/ __ \_  __ \
 /        \|   Y  \  |   |  \___  ||   Y  \  |  /   |  \  | \  ___/|  | \/
/_______  /|___|  /__|___|  / ____||___|  /____/|___|  /__|  \___  >__|
        \/      \/        \/\/          \/           \/          \/
```

---

## Requirements

- Python 3.8+
- Google Chrome installed
- The following Python packages:

```
pip install selenium webdriver-manager
```

`webdriver-manager` handles the ChromeDriver automatically. If you prefer to manage ChromeDriver yourself, the script will fall back to whatever `chromedriver` is on your PATH.

---

## Usage

```
python shiny_hunter.py
```

1. The script opens Chrome and navigates to pokelike.xyz
2. Log in, choose your gender and starter, and start the run
3. Navigate to the screen where the pokeball is visible
4. Press **ENTER** in the terminal to start the hunt
5. The script resets in a loop automatically

Press **Ctrl+C** at any time to stop the current hunt and return to the mode menu. Chrome stays open so you can start a new hunt without restarting the script.

---

![Demo](https://github.com/user-attachments/assets/13aa49c3-e52d-41fb-9157-7fd8554ec5d3)

## Modes

### [1] Any Shiny
Stops whenever any shiny Pokemon appears. The terminal shows the Pokemon name and asks whether to keep it or keep hunting.

```
[~] #  42  |  00:31  |  click -> [-] No shiny
[~] #  43  |  00:32  |  click ->
******************************************************
  [!!!]  SHINY FOUND
  Pokemon  : Magnemite
  Attempt  : #43
  Time     : 00:32
******************************************************
  [?] Keep this Magnemite?
  ENTER  -> keep hunting
  Ctrl+C -> return to menu
```

### [2] Custom Shiny
You enter a specific Pokemon name. Any other shiny that appears is silently skipped and the loop continues until the target is found.

```
[>] Pokemon name to hunt: Tauros
[+] Mode set: Custom Shiny -> Tauros

[~] #  12  |  00:09  |  click -> [>] Magnemite -- not Tauros, skipping
[~] #  13  |  00:10  |  click -> [>] Geodude -- not Tauros, skipping
[~] #  97  |  01:14  |  click ->
******************************************************
  [!!!]  TARGET SHINY FOUND
  Pokemon  : Tauros
  Attempt  : #97
  Time     : 01:14
******************************************************
```

---

## Configuration

At the top of `shiny_hunter.py` you can adjust the timing to match your connection and machine speed:

| Variable | Default | Description |
|---|---|---|
| `WAIT_AFTER_R` | `1.8` | Seconds after pressing R before clicking the pokeball |
| `WAIT_AFTER_CLICK` | `3.5` | Seconds after clicking the pokeball before checking for a shiny |
| `SHINY_POLL_PERIOD` | `0.4` | How often (in seconds) to check for the shiny badge |
| `SHINY_TIMEOUT` | `7.0` | Max seconds to wait for a shiny before giving up and resetting |

If the page renders fast on your machine, these can be reduced significantly. A working fast configuration:

```python
WAIT_AFTER_R      = 0.05
WAIT_AFTER_CLICK  = 0.05
SHINY_POLL_PERIOD = 0.1
SHINY_TIMEOUT     = 0.11
```

Lower `WAIT_AFTER_R` until the pokeball stops being found, then add `0.1s` back. Lower `WAIT_AFTER_CLICK` until you start seeing false negatives, then add `0.1s` back.

---

## How it works

The script uses Selenium to control Chrome. On each attempt it:

1. Sends the `R` key to the page to trigger the game's reset
2. Finds the pokeball SVG element (`sprites/catchPokemon.png`) and dispatches a click event via JavaScript
3. Waits for the battle screen to render, then polls for a visible `span.shiny-badge` element
4. If found, reads the Pokemon name from the `div.poke-name` inside the same `poke-card`
5. In Custom mode, skips the Pokemon if the name does not match the target

---

## License

MIT — see [LICENSE](LICENSE)
