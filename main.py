import time
import pandas as pd
import sys
from kbhit import KBHit
from utils import get_config_value, read_random_text_part, linear_regression_get_beta, write_event, load_events
from datetime import datetime, timezone, timedelta
from definitions import *
from typing_errors import typing_errors

time_zone = datetime.utcnow().astimezone().tzinfo.utcoffset(datetime.now()).seconds


def text_event(kb):
    print(end="How many hours the event has passed: (0.0 for now)", flush=True)
    hours_ago=kb.get_string()
    if not hours_ago:
        hours_ago=0.0
    else:
        hours_ago=float(hours_ago)
    print(f"{int(hours_ago*60)} min ago")

    print(end="Event text: ", flush=True)
    start_time = int(time.time())-int(hours_ago*60)
    text=kb.get_string()
    if text:
        return {"start_time": start_time,
                "time_zone": time_zone,
                "type": "text",
                "text": text}
    else:
        return {}

def testing_typing(kb):
    time_passed = []
    example_text = read_random_text_part(character_count=get_config_value("character_count"),
                                         convert_letters=bool(get_config_value("convert_letters")),
                                         language=get_config_value("language"))

    print("Typing test, please write the text below, and finish with ESC")
    print(example_text)
    print("-" * 30)
    start_time = int(time.time())
    last_hit = time.time()

    while True:
        if kb.kbhit():
            k_in = kb.getch()
            if k_in == ESC:
                print("aborted")
                break
            time_passed.append((time.time() - last_hit, k_in))
            if k_in == BACK:
                print('\b ', end="", flush=True)
                sys.stdout.write('\010')
            else:
                print(end=k_in, flush=True)
            last_hit = time.time()
        time.sleep(0.0001)

    print(end="Analyzing typing errors...", flush=True)
    time_passed_e = typing_errors(time_passed, example_text)
    print()
    return {"start_time": start_time,
            "time_zone": time_zone,
            "language": get_config_value("language"),
            "type": "typing_test",
            "time_passed": time_passed_e,
            "example_text": example_text}


def analyze_typing_test(typing_test_data):
    d = {"time": [t for t, l, e in typing_test_data["time_passed"]],
         "letter": [l for t, l, e in typing_test_data["time_passed"]],
         "correct": [e for t, l, e in typing_test_data["time_passed"]]}
    df = pd.DataFrame(d)

    df["left"] = df["letter"].isin([e for e in get_config_value("left_hand")])
    df["right"] = df["letter"].isin([e for e in get_config_value("right_hand")])
    df['left_left'] = df.left & df.left.shift(1)
    df['right_right'] = df.right & df.right.shift(1)
    metrics = {"general      ": df,
               "left hand    ": df[df["left"]],
               "right hand   ": df[df["right"]],
               "2x left hand ": df[df["left_left"]],
               "2x right hand": df[df["right_right"]],
               }
    print(f"typing speed:  ({len(df)} characters)")
    for k, v in metrics.items():
        verror = v[v["correct"] == False]["time"]
        speed_up = linear_regression_get_beta(v["time"])
        vt = v["time"]
        print(
            f"            {k} : median: {vt.median():.2f}s " +
            f"trend: {int(speed_up * 100 * len(vt))}%  " +
            f"error: {int(10000 * len(verror) / len(v)) / 100}% ({len(verror)})")


def print_event(event):
    tz = timezone(timedelta(seconds=event['time_zone']))
    stime = datetime.fromtimestamp(event['start_time'], tz=tz)
    print(end=f"\nEvent from {stime}   ")
    if event["type"] == "typing_test":
        analyze_typing_test(event)
    if event["type"] == "text":
        print(event["text"])


if __name__ == '__main__':
    kb = KBHit()

    while True:
        print(
            """select an option:
               1) register an event
               2) measure typing speed 
               3) show history    
             ESC) quit                 
            """, flush=True)
        while not kb.kbhit():
            time.sleep(0.001)

        k_in = kb.getch()
        if k_in in [ESC,'q']:
            print("quiting")
            break
        if k_in == '1':
            event = text_event(kb)
            if event:
                print_event(event)
                write_event(event)
        if k_in == '2':
            event = testing_typing(kb)
            write_event(event)
            print_event(event)
        if k_in == '3':
            events = load_events()
            for event in events:
                print_event(event)
        time.sleep(0.001)

    kb.set_normal_term()
