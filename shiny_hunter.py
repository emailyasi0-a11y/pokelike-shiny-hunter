"""
POKELIKE.XYZ - SHINY HUNTER
----------------------------
1. pip install selenium webdriver-manager
2. python shiny_hunter.py
3. The script opens Chrome on pokelike.xyz
4. Log in and start the run manually
5. Once you are on the screen with the pokeball, press ENTER
6. The script resets in a loop until it finds the shiny you want
"""

import time
import sys

try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
except ImportError:
    print("[!] Missing selenium. Run: pip install selenium webdriver-manager")
    sys.exit(1)

try:
    from webdriver_manager.chrome import ChromeDriverManager
    USE_WDM = True
except ImportError:
    USE_WDM = False

WAIT_AFTER_R      = 0.05
WAIT_AFTER_CLICK  = 0.05
SHINY_POLL_PERIOD = 0.1
SHINY_TIMEOUT     = 0.11


def open_chrome():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if USE_WDM:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    else:
        driver = webdriver.Chrome(options=options)
    return driver


def press_r(driver):
    try:
        body = driver.find_element(By.TAG_NAME, "body")
        body.send_keys("r")
        return True
    except Exception:
        pass
    try:
        ActionChains(driver).send_keys("r").perform()
        return True
    except Exception as e:
        print(f"[-] Could not press R: {e}")
        return False


def click_pokeball(driver):
    try:
        result = driver.execute_script("""
            const selectors = [
                'image[href="sprites/catchPokemon.png"]',
                'image[xlink\\:href="sprites/catchPokemon.png"]',
            ];
            for (const sel of selectors) {
                const el = document.querySelector(sel);
                if (el) {
                    el.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true}));
                    return 'ok';
                }
            }
            for (const img of document.querySelectorAll('image')) {
                const href = img.getAttribute('href') || img.getAttribute('xlink:href') || '';
                if (href.includes('catchPokemon')) {
                    img.dispatchEvent(new MouseEvent('click', {bubbles:true, cancelable:true}));
                    return 'ok_fallback';
                }
            }
            return null;
        """)
        if result:
            return True
    except Exception:
        pass

    for selector in [
        'image[href="sprites/catchPokemon.png"]',
        'image[*|href="sprites/catchPokemon.png"]',
    ]:
        try:
            el = driver.find_element(By.CSS_SELECTOR, selector)
            ActionChains(driver).move_to_element(el).click().perform()
            return True
        except Exception:
            pass

    return False


def check_shiny(driver):
    try:
        for badge in driver.find_elements(By.CSS_SELECTOR, "span.shiny-badge"):
            if not badge.is_displayed():
                continue
            name = None
            try:
                card = badge.find_element(By.XPATH, "./ancestor::*[contains(@class,'poke-card')]")
                name = card.find_element(By.CSS_SELECTOR, ".poke-name").text.strip()
            except Exception:
                pass
            return True, name or "???"
    except Exception:
        pass
    return False, None


def divider(char="-", width=54):
    print(char * width)


def fmt_time(seconds):
    m = int(seconds // 60)
    s = int(seconds % 60)
    return f"{m:02d}:{s:02d}"


def choose_mode():
    print()
    divider()
    print("  SHINY HUNTER - MODE SELECTION")
    divider()
    print("  [1]  Any Shiny")
    print("       Stops on any shiny that appears.")
    print("       Press ENTER to keep hunting or Ctrl+C to keep it.")
    print()
    print("  [2]  Custom Shiny")
    print("       Enter a Pokemon name to hunt.")
    print("       All other shinies will be skipped automatically.")
    divider()
    print()

    while True:
        choice = input("  Select mode [1/2]: ").strip()
        if choice == "1":
            print("[+] Mode set: Any Shiny")
            return "any", None
        elif choice == "2":
            target = input("[>] Pokemon name to hunt: ").strip()
            if target:
                print(f"[+] Mode set: Custom Shiny -> {target}")
                return "custom", target
            else:
                print("[-] Please enter a name.")
        else:
            print("[-] Type 1 or 2.")


def main():
    for line in r"""__________       __          .__  .__ __           
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
        \/      \/        \/\/          \/           \/          \/       """.splitlines():
        print(line)
    print()
    divider("=")

    print()
    print("[*] Opening Chrome...")
    driver = open_chrome()
    driver.get("https://pokelike.xyz/")

    while True:
        mode, target = choose_mode()
        target_lower = target.lower() if target else None

        print()
        divider()
        print("  Chrome is open on pokelike.xyz")
        print()
        print("  1. Log in")
        print("  2. Choose gender + starter and start the run")
        print("  3. Navigate to the screen with the pokeball")
        print()
        print("  When you are ready, press ENTER here")
        divider()
        input()

        print()
        if mode == "any":
            print("[*] Starting hunt -- Any Shiny mode -- Ctrl+C to return to menu")
        else:
            print(f"[*] Starting hunt -- Custom Shiny mode -- Target: {target} -- Ctrl+C to return to menu")
        divider()
        print()

        attempts = 0
        t_start  = time.time()

        try:
            while True:
                attempts += 1
                elapsed = time.time() - t_start
                print(f"[~] #{attempts:>4}  |  {fmt_time(elapsed)}  |  ", end="", flush=True)

                press_r(driver)
                time.sleep(WAIT_AFTER_R)

                found = click_pokeball(driver)
                if not found:
                    print("[-] Pokeball not found -- is it visible on screen?")
                    time.sleep(1)
                    continue

                print("click -> ", end="", flush=True)
                time.sleep(WAIT_AFTER_CLICK)

                shiny, name = False, None
                t_check = time.time()
                while time.time() - t_check < SHINY_TIMEOUT:
                    detected, name = check_shiny(driver)
                    if detected:
                        shiny = True
                        break
                    time.sleep(SHINY_POLL_PERIOD)

                if shiny:
                    if mode == "custom" and name and name.lower() != target_lower:
                        print(f"[>] {name} -- not {target}, skipping")
                        continue

                    elapsed = time.time() - t_start
                    print()
                    print()
                    divider("*")
                    if mode == "custom":
                        print("  [!!!]  TARGET SHINY FOUND")
                    else:
                        print("  [!!!]  SHINY FOUND")
                    print(f"  Pokemon  : {name}")
                    print(f"  Attempt  : #{attempts:,}")
                    print(f"  Time     : {fmt_time(elapsed)}")
                    divider("*")
                    for _ in range(6):
                        sys.stdout.write("\a")
                        sys.stdout.flush()
                        time.sleep(0.4)
                    print()
                    divider()
                    if mode == "any":
                        print(f"  [?] Keep this {name}?")
                        print("  ENTER  -> keep hunting")
                        print("  Ctrl+C -> return to menu")
                    else:
                        print(f"  [?] Keep this {name}?")
                        print(f"  ENTER  -> keep hunting for {target}")
                        print("  Ctrl+C -> return to menu")
                    divider()
                    input()
                    print()
                    print("[*] Resuming hunt...")
                    print()
                else:
                    print("[-] No shiny")

        except KeyboardInterrupt:
            elapsed = time.time() - t_start
            print()
            print()
            divider()
            print("[+] Hunt stopped.")
            print(f"    Total attempts : {attempts:,}")
            print(f"    Total time     : {fmt_time(elapsed)}")
            divider()
            print()
            print("[*] Returning to menu... (Ctrl+C again to exit)")
            print()


if __name__ == "__main__":
    main()
