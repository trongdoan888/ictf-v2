import requests, time, random, string, os

DB_URL = os.environ.get("DB_URL", "http://database:5000")
TICK_INTERVAL = int(os.environ.get("TICK_INTERVAL", "30"))
TEAMS = os.environ.get("TEAMS", "team1").split(",")

def random_flag():
    return "FLAG{" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=12)) + "}"

def set_flags():
    for t in TEAMS:
        flag = random_flag()
        try:
            r = requests.post(f"{DB_URL}/set_flag", json={"team": t, "flag": flag}, timeout=5)
            print(f"[GAMEBOT] set {t} -> {flag} ({r.status_code})")
        except Exception as e:
            print(f"[GAMEBOT] Error setting flag for {t}: {e}")

if __name__ == "__main__":
    print("[GAMEBOT] starting")
    while True:
        set_flags()
        time.sleep(TICK_INTERVAL)
