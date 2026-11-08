

import csv
import random
from datetime import date, datetime, timedelta
from pathlib import Path

SEED = 6301
AS_OF = date(2026, 11, 7)                  # last day of data
START = AS_OF - timedelta(days=364)        # 12 months: 2025-11-08 .. 2026-11-07
PRICE_INCREASE_DAY = date(2026, 6, 1)      # coffee went up $0.25 on this day

N_MEMBERS = 50
N_MEMBERS_NEVER_ORDERED = 6
N_ORDERS = 1500

# The two orders whose payments deliberately do NOT match their total.
BROKEN_ORDERS = {
    137: -100,   # customer underpaid by $1.00
    902: +50,    # customer overpaid by $0.50
}

DATA_DIR = Path(__file__).parent / "data"
rng = random.Random(SEED)


def dollars(cents: int) -> str:
    """Format whole cents as a dollar string, e.g. 475 -> '4.75'."""
    return f"{cents / 100:.2f}"


def write_csv(name: str, header: list[str], rows: list[list]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_DIR / f"{name}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print(f"  {name}.csv: {len(rows):,} rows")


# ---------------------------------------------------------------- products
# (name, category, price_cents, cost_cents, available_today, season)
# season: None = all year, otherwise the set of months it was sold.
PRODUCTS = [
    ("Espresso",            "coffee", 300, 60,  True,  None),
    ("Americano",           "coffee", 350, 70,  True,  None),
    ("Latte",               "coffee", 475, 120, True,  None),
    ("Cappuccino",          "coffee", 450, 110, True,  None),
    ("Flat White",          "coffee", 475, 120, True,  None),
    ("Mocha",               "coffee", 525, 150, True,  None),
    ("Cold Brew",           "coffee", 450, 90,  True,  None),
    ("Drip Coffee",         "coffee", 275, 45,  True,  None),
    ("Peppermint Mocha",    "coffee", 575, 170, False, {12, 1}),   # winter only
    ("Chai Latte",          "tea",    450, 110, True,  None),
    ("Matcha Latte",        "tea",    525, 160, True,  None),
    ("Earl Grey",           "tea",    300, 40,  True,  None),
    ("Green Tea",           "tea",    300, 40,  True,  None),
    ("Iced Lemon Tea",      "tea",    375, 70,  False, {6, 7, 8}),  # summer only
    ("Butter Croissant",    "food",   375, 120, True,  None),
    ("Blueberry Muffin",    "food",   350, 100, True,  None),
    ("Bagel & Cream Cheese","food",   425, 140, True,  None),
    ("Avocado Toast",       "food",   850, 320, True,  None),
    ("Turkey Sandwich",     "food",   925, 380, True,  None),
    ("Chocolate Cookie",    "food",   250, 60,  True,  None),
    ("Matcha Cookie",       "food",   275, 70,  True,  set()),      # new, never sold
    ("Bottled Water",       "other",  200, 50,  True,  None),
    ("Orange Juice",        "other",  400, 150, True,  None),
    ("Kombucha",            "other",  475, 200, True,  None),
]

# Relative popularity (higher = sold more often), same order as PRODUCTS.
POPULARITY = [6, 5, 14, 9, 6, 6, 8, 7, 5, 6, 5, 3, 3, 4,
              8, 6, 5, 3, 4, 7, 0, 4, 3, 2]

products_rows = []
for pid, (name, cat, price, cost, avail, _season) in enumerate(PRODUCTS, start=1):
    assert price >= cost, f"{name}: price below cost"
    products_rows.append([pid, name, cat, dollars(price), dollars(cost), avail])


def product_price_on(pid: int, day: date) -> int:
    """Price in cents actually charged on a given day."""
    _, cat, price, *_ = PRODUCTS[pid - 1]
    if cat == "coffee" and day < PRICE_INCREASE_DAY:
        return price - 25
    return price


def sellable(pid: int, day: date) -> bool:
    season = PRODUCTS[pid - 1][5]
    return season is None or day.month in season


# ----------------------------------------------------------------- options
# (name, price_cents, cost_cents)
OPTIONS = [
    ("Extra Shot",      100, 30),
    ("Oat Milk",         75, 25),
    ("Almond Milk",      75, 25),
    ("Vanilla Syrup",    60, 10),
    ("Caramel Syrup",    60, 10),
    ("Hazelnut Syrup",   60, 10),
    ("Whipped Cream",    50, 15),
    ("Extra Hot",         0,  0),   # free option
    ("Lavender Syrup",   80, 20),   # nobody ever chooses this one
]
OPTION_WEIGHTS = [8, 10, 4, 7, 5, 3, 3, 4, 0]
options_rows = [[oid, n, dollars(p), dollars(c)]
                for oid, (n, p, c) in enumerate(OPTIONS, start=1)]

# ----------------------------------------------------------------- members
FIRST_NAMES = ["Ana", "Ben", "Carla", "Diego", "Emma", "Felipe", "Grace",
               "Hugo", "Isabel", "Jack", "Kenji", "Lucia", "Mateo", "Nora",
               "Omar", "Paula", "Quinn", "Rosa", "Sam", "Tara", "Uma",
               "Victor", "Wen", "Ximena", "Yusuf", "Zoe", "Liam", "Mia",
               "Noah", "Olivia", "Priya", "Raj", "Sofia", "Theo", "Valeria",
               "Will", "Aisha", "Bruno", "Chloe", "Daniel", "Elena", "Finn",
               "Gabi", "Hana", "Ivan", "Julia", "Kai", "Leo", "Maya", "Nico"]

members_rows = []
member_join = {}
used_mobiles = set()
for mid in range(1, N_MEMBERS + 1):
    name = FIRST_NAMES[mid - 1]
    while True:
        mobile = f"617-{rng.randint(200, 999)}-{rng.randint(1000, 9999)}"
        if mobile not in used_mobiles:
            used_mobiles.add(mobile)
            break
    email = (f"{name.lower()}{rng.randint(1, 99)}@example.com"
             if rng.random() < 0.7 else "")          # ~30% gave no email
    if mid > N_MEMBERS - N_MEMBERS_NEVER_ORDERED:
        # the last few joined recently and have not ordered yet
        join = AS_OF - timedelta(days=rng.randint(1, 20))
    else:
        # joined any time from two years ago up to two months ago
        join = AS_OF - timedelta(days=rng.randint(60, 730))
    member_join[mid] = join
    members_rows.append([mid, name, mobile, email, join.isoformat(), 0])

ordering_members = list(range(1, N_MEMBERS - N_MEMBERS_NEVER_ORDERED + 1))
# a few regulars order much more often than everyone else
member_weights = [rng.choice([1, 1, 2, 3, 8]) for _ in ordering_members]

# ------------------------------------------------------------------ orders
days = [START + timedelta(days=i) for i in range((AS_OF - START).days + 1)]
# weekdays busy, weekends quiet, summer quiet (fewer students on campus)
day_weights = []
for d in days:
    w = 1.0 if d.weekday() < 5 else 0.35
    if d.month in (6, 7, 8):
        w *= 0.45
    day_weights.append(w)

order_days = sorted(rng.choices(days, weights=day_weights, k=N_ORDERS))

orders_rows, lines_rows, line_opt_rows, payments_rows = [], [], [], []
line_id = 0
payment_id = 0
points_earned = {mid: 0 for mid in member_join}

for order_id, day in enumerate(order_days, start=1):
    hour = rng.choices(range(7, 19), weights=[6, 9, 8, 5, 4, 7, 6, 4, 3, 3, 2, 1])[0]
    ordered_at = datetime(day.year, day.month, day.day,
                          hour, rng.randint(0, 59), rng.randint(0, 59))

    member_id = None
    if rng.random() < 0.6:                 # ~60% of orders are by members
        eligible = [(m, w) for m, w in zip(ordering_members, member_weights)
                    if member_join[m] <= day]
        if eligible:
            ms, ws = zip(*eligible)
            member_id = rng.choices(ms, weights=ws)[0]

    channel = "app" if (member_id and rng.random() < 0.45) else "counter"
    orders_rows.append([order_id, ordered_at.isoformat(sep=" "),
                        member_id if member_id else "", channel])

    # --- lines: 1 to 3 different products
    candidates = [pid for pid in range(1, len(PRODUCTS) + 1)
                  if sellable(pid, day) and POPULARITY[pid - 1] > 0]
    weights = [POPULARITY[pid - 1] for pid in candidates]
    n_lines = rng.choices([1, 2, 3], weights=[60, 30, 10])[0]
    chosen = set()
    while len(chosen) < n_lines:
        chosen.add(rng.choices(candidates, weights=weights)[0])

    order_total = 0
    for pid in sorted(chosen):
        line_id += 1
        qty = rng.choices([1, 2, 3], weights=[85, 12, 3])[0]
        unit = product_price_on(pid, day)
        lines_rows.append([line_id, order_id, pid, qty, dollars(unit)])
        order_total += qty * unit

        # --- options: only on drinks, 0 to 2 different ones
        if PRODUCTS[pid - 1][1] in ("coffee", "tea"):
            n_opts = rng.choices([0, 1, 2], weights=[50, 35, 15])[0]
            opts = set()
            while len(opts) < n_opts:
                opts.add(rng.choices(range(1, len(OPTIONS) + 1),
                                     weights=OPTION_WEIGHTS)[0])
            for oid in sorted(opts):
                oprice = OPTIONS[oid - 1][1]
                line_opt_rows.append([line_id, oid, dollars(oprice)])
                order_total += qty * oprice     # charged once per unit

    # --- payments: must add up to order_total (except the two broken orders)
    to_pay = order_total + BROKEN_ORDERS.get(order_id, 0)
    if channel == "app":
        methods = ["app"]
    else:
        methods = [rng.choices(["card", "cash"], weights=[70, 30])[0]]
    # members sometimes pay part of the order with points
    if member_id and to_pay > 200 and rng.random() < 0.15:
        methods = ["points"] + methods
    if len(methods) == 2:
        first = rng.randint(1, min(300, to_pay - 1))     # points cover up to $3
        amounts = [first, to_pay - first]
    else:
        amounts = [to_pay]
    for method, amt in zip(methods, amounts):
        assert amt > 0
        payment_id += 1
        payments_rows.append([payment_id, order_id, method, dollars(amt)])

    if member_id:
        points_earned[member_id] += order_total // 100   # 1 point per dollar

for row in members_rows:
    row[5] = points_earned[row[0]] % 150   # balance left after redeeming

# ------------------------------------------------------------------- write
print(f"Writing CSVs to {DATA_DIR}")
write_csv("members", ["member_id", "first_name", "mobile", "email",
                      "join_date", "points_balance"], members_rows)
write_csv("products", ["product_id", "name", "category", "price", "cost",
                       "available_today"], products_rows)
write_csv("options", ["option_id", "name", "price", "cost"], options_rows)
write_csv("orders", ["order_id", "ordered_at", "member_id", "channel"],
          orders_rows)
write_csv("order_lines", ["line_id", "order_id", "product_id", "quantity",
                          "unit_price"], lines_rows)
write_csv("line_options", ["line_id", "option_id", "price_charged"],
          line_opt_rows)
write_csv("payments", ["payment_id", "order_id", "method", "amount"],
          payments_rows)
print(f"Deliberately broken orders (payments != total): {sorted(BROKEN_ORDERS)}")