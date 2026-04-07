"""
VMAXRAY TUNNEL CLIENT for MiniOS (GAS v2.0)
Run on MiniOS alongside vmaxcode server (port 8081)

Routes browser requests from GAS → MiniOS vmaxcode (port 8081)
"""

import sys
import json
import time
import base64
import threading
import socket

PY3 = sys.version_info[0] >= 3
if PY3:
    from urllib.request import urlopen, Request
    from urllib.error   import URLError, HTTPError
else:
    from urllib2 import urlopen, Request, URLError, HTTPError

GAS_URL    = "https://script.google.com/macros/s/AKfycbwTvs_1_4ZjDi7HSrpScpgHOGWeMsba0_Ia17skX6vUKCfeU-UlEz2h2wpNf7p2Prm5Fw/exec"
LOCAL_URL  = "http://127.0.0.1:8081"
SECRET     = "VMAXRAY2025"
POLL_INTERVAL = 2
KEEPALIVE_S   = 30
RETRY_DELAY   = 5
MAX_ERRORS    = 5
USER_AGENT   = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

def log(msg):
    ts = time.strftime("%H:%M:%S")
    print("[%s] %s" % (ts, msg))
    sys.stdout.flush()

def relay_url(action):
    return "%s?action=%s&secret=%s" % (GAS_URL, action, SECRET)

def post_json(url, data, timeout=30):
    try:
        payload = json.dumps(data).encode('utf-8')
        req = Request(url, data=payload)
        req.add_header('Content-Type', 'application/json')
        req.add_header('User-Agent', USER_AGENT)
        resp = urlopen(req, timeout=timeout)
        raw = resp.read()
        if not raw:
            return {'error': 'Empty response'}
        try:
            return json.loads(raw.decode('utf-8'))
        except ValueError:
            return {'error': 'BAD_JSON', 'raw': raw[:300].decode('utf-8','replace')}
    except HTTPError as e:
        raw = e.read()
        try:
            return json.loads(raw.decode('utf-8'))
        except:
            return {'error': 'HTTP %d' % e.code}
    except URLError as e:
        return {'error': 'URLError: %s' % str(e.reason)}
    except socket.timeout:
        return {'error': 'Socket timeout'}
    except Exception as e:
        return {'error': str(e)}

def get_local(url, method='GET', headers=None, body_bytes=b'', timeout=25):
    try:
        if method in ('POST','PUT','PATCH') and body_bytes:
            req = Request(url, data=body_bytes)
        else:
            req = Request(url)
        req.get_method = lambda: method
        req.add_header('User-Agent', USER_AGENT)
        skip = {'host','content-length','transfer-encoding','connection','x-secret'}
        for k, v in (headers or {}).items():
            if k.lower() not in skip:
                try:
                    req.add_header(k, v)
                except:
                    pass
        resp = urlopen(req, timeout=timeout)
        status = resp.getcode()
        rbody = resp.read()
        info = resp.info()
        rheads = dict(info.items()) if hasattr(info, 'items') else {}
        return {'status': status, 'headers': rheads, 'body': base64.b64encode(rbody).decode('utf-8')}
    except HTTPError as e:
        rbody = e.read()
        return {'status': e.code, 'headers': {'Content-Type':'application/json'}, 'body': base64.b64encode(rbody).decode('utf-8')}
    except Exception as e:
        err = json.dumps({'error': 'Local error: %s' % str(e)}).encode('utf-8')
        return {'status': 502, 'headers': {'Content-Type':'application/json'}, 'body': base64.b64encode(err).decode('utf-8')}

def run_diagnostics():
    log("=" * 50)
    log(" VMAXRAY TUNNEL MINIOS (GAS v2.0)")
    log("=" * 50)
    all_ok = True

    log("[1/2] Checking vmaxcode server...")
    try:
        req = Request(LOCAL_URL + '/health')
        resp = urlopen(req, timeout=5)
        body = resp.read().decode('utf-8')
        log("      [OK] Server OK: %s" % body.strip()[:60])
    except Exception as e:
        log("      [FAIL] Server unreachable: %s" % str(e))
        all_ok = False

    log("[2/2] Testing GAS registration...")
    r = post_json(relay_url('register_minios'), {}, timeout=10)
    if r.get('ok'):
        log("      [OK] Register OK")
    else:
        log("      [FAIL] Register: %s" % r.get('error', str(r)[:60]))
        all_ok = False

    log("=" * 50)
    if all_ok:
        log(" [OK] Ready — Starting tunnel...")
    else:
        log(" [WARN] Starting anyway...")
    log("=" * 50)
    return all_ok

def poll_loop():
    log("Polling GAS for requests...")
    errors = 0
    last_keepalive = 0

    while True:
        try:
            now = time.time()
            if now - last_keepalive >= KEEPALIVE_S:
                r = post_json(relay_url('register_minios'), {}, timeout=8)
                if r.get('ok'):
                    log("Keepalive [OK]")
                else:
                    log("Keepalive [FAIL] %s" % r.get('error', '?'))
                last_keepalive = now

            result = post_json(relay_url('poll_minios'), {}, timeout=POLL_INTERVAL + 5)

            if 'error' in result:
                errors += 1
                log("Poll error [%d/%d]: %s" % (errors, MAX_ERRORS, result['error']))
                if errors >= MAX_ERRORS:
                    time.sleep(RETRY_DELAY * 5)
                    errors = 0
                else:
                    time.sleep(RETRY_DELAY)
                continue

            errors = 0
            req_id = result.get('id')
            if not req_id:
                continue

            method = result.get('method', 'GET')
            uri = result.get('uri', '/')
            headers = result.get('headers', {})
            body_b64 = result.get('body', '')
            log("-> %s %s [%s]" % (method, uri, req_id[-8:]))

            body_bytes = b''
            if body_b64:
                try:
                    body_bytes = base64.b64decode(body_b64)
                except:
                    pass

            local_url = LOCAL_URL + uri
            resp = get_local(local_url, method, headers, body_bytes)
            log("<- HTTP %d [%s]" % (resp['status'], req_id[-8:]))

            resp['id'] = req_id
            send_r = post_json(relay_url('respond_minios'), resp, timeout=15)
            if 'error' in send_r:
                log("  [WARN] Respond error: %s" % send_r['error'])

        except KeyboardInterrupt:
            log("Stopped.")
            sys.exit(0)
        except Exception as e:
            errors += 1
            log("Loop error: %s" % str(e))
            time.sleep(RETRY_DELAY)

if __name__ == '__main__':
    run_diagnostics()
    poll_loop()
