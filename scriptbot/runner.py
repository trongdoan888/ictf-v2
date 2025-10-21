import os, requests, time

DB_URL = os.environ.get("DB_URL", "http://database:5000")
SLEEP = int(os.environ.get("SCRIPT_INTERVAL", "20"))
TARGET_TEAMS = os.environ.get("TEAMS", "team1").split(",")

if __name__ == "__main__":
    print("[SCRIPTBOT] starting")
    while True:
        for t in TARGET_TEAMS:
            try:
                r = requests.get(f"{DB_URL}/get_flag/{t}", timeout=5)
                flag = r.json().get("flag")
                if flag and flag != "no_flag":
                    print(f"[SCRIPTBOT] Found flag for {t}: {flag}. Submitting as 'attacker'...")
                    s = requests.post(f"{DB_URL}/submit_flag", json={"team": "attacker", "flag": flag}, timeout=5)
                    print(f"[SCRIPTBOT] Submit result: {s.json()}")
            except Exception as e:
                print("[SCRIPTBOT] Error:", e)
        time.sleep(SLEEP)
