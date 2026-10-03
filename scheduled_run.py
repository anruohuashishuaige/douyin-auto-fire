"""Run one daily batch at a random time inside 11:40–12:00 Beijing time."""
import os
import time
from app.send_window import allowed, choose_start, now

def main():
    selected = choose_start(now())
    if selected is None:
        print("SKIPPED: today's 11:40-12:00 Beijing window has ended.")
        return 0
    print(f'Random batch start (Beijing): {selected.isoformat()}', flush=True)
    while now() < selected:
        time.sleep(min(30, max(0, (selected - now()).total_seconds())))
    if not allowed(now()):
        print('SKIPPED: runner resumed outside the sending window.')
        return 0
    os.environ['DOUYIN_WINDOW_ENFORCED'] = 'true'
    from run import main as run_main
    return run_main()

if __name__ == '__main__':
    raise SystemExit(main())
