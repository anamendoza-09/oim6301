import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #My Mini Project: The-Shops-Week
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 1: The Question
    Every Monday, Northwind’s operations manager reviews the past week’s shop activity to decide what needs attention before it becomes a problem: which orders haven’t shipped and need chasing, which countries are driving revenue and might warrant more regional stock or outreach, and which products are selling fastest and should be reordered soon. This report answers: how many orders were placed in the last seven days, and how much revenue did they generate, excluding freight? Which countries generated the most revenue? What are the top five best-selling products by units sold? And which orders have not shipped yet?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Part 2: My Plan before AI
    To answer these questions, I will use lists and dictionaries to store the orders and organize information such as revenue, countries, and products.For loops will be used to go through each order and collect the information needed. I will use If statements to identify orders placed within the last seven days and orders that have not shipped yet. Sum will calculate total revenue and the number of units sold, and max will identify the best-selling products and rank the top five based on units sold.
    To check whether my results make sense, I will compare the total revenue with the sum of revenue across all countries. These numbers should agree because they represent the same sales.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Part 3: Input
    """)
    return


@app.cell
def _():
    days = 7
    return (days,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Part 4: The Work
    """)
    return


@app.cell
def _(days):
    import requests
    import json
    from pathlib import Path
    from datetime import date, timedelta

    DATA_DIR = Path(__file__).parent / "data"

    def fetch_orders(from_date, to_date, per_page=50):
        """Fetch every order placed between from_date and to_date, following pagination until all pages are retrieved."""
        all_orders = []
        page = 1

        while True:
            response = requests.get(
                "https://oim.zhili.dev/shop/orders",
                params={
                    "from_date": str(from_date),
                    "to_date": str(to_date),
                    "page": page,
                    "per_page": per_page,
                },
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()
            all_orders.extend(payload["items"])

            if not payload["pagination"]["has_next"]:
                break
            page += 1

        return all_orders


    today = date.today()
    start_date = today - timedelta(days=days - 1)

    orders = fetch_orders(start_date, today)
    order_count = len(orders)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    (DATA_DIR / f"orders_{start_date}_{today}.json").write_text(json.dumps(orders, indent=2))

    print(f"Fetched {order_count} orders from {start_date} to {today}.")
    return DATA_DIR, json, order_count, orders, requests, start_date, today


@app.cell
def _(order_count, orders):
    revenue_exc_freight = sum(order["order_total_dollars"] for order in orders)

    print(f"{order_count} orders were placed in the last 7 days, totalling ${revenue_exc_freight:,.2f} in revenue excluding freight.")
    return (revenue_exc_freight,)


@app.cell
def _(orders):

    print(orders[0].keys())
    return


@app.cell
def _(orders):
    revenue_by_country = {}

    for _order in orders:
        country = _order["ship_country"]
        revenue = _order["order_total_dollars"]

        if country in revenue_by_country:
            revenue_by_country[country] += revenue
        else:
            revenue_by_country[country] = revenue

    sorted_countries = sorted(
        revenue_by_country.items(),
        key=lambda item: item[1],
        reverse=True
    )

    print("Revenue by Country (Excluding Freight):")

    for country, revenue in sorted_countries:
        print(f"{country}: ${revenue:,.2f}")
    return (sorted_countries,)


@app.cell
def _(DATA_DIR, json, orders, requests, start_date, today):
    def fetch_order_lines(order_id):
        """Fetch the line items for a single order."""
        response = requests.get(f"https://oim.zhili.dev/shop/orders/{order_id}", timeout=30)
        response.raise_for_status()
        detail = response.json()

        if "lines" in detail:
            return detail["lines"]
        elif "order_details" in detail:
            return detail["order_details"]
        elif "items" in detail:
            return detail["items"]
        else:
            raise KeyError(f"Cannot find product lines: {list(detail.keys())}")


    units_by_product = {}
    lines_by_order = {}

    for _order in orders:
        lines = fetch_order_lines(_order["order_id"])
        lines_by_order[_order["order_id"]] = lines

        for line in lines:
            product = line.get("product_name", line.get("product_id"))
            quantity = line["quantity"]
            units_by_product[product] = units_by_product.get(product, 0) + quantity

    (DATA_DIR / f"order_lines_{start_date}_{today}.json").write_text(json.dumps(lines_by_order, indent=2))

    top_5_products = sorted(units_by_product.items(), key=lambda item: item[1], reverse=True)[:5]

    print("Top 5 Best-Selling Products by Units Sold:")
    for product, units in top_5_products:
        print(f"{product}: {units} units sold")
    return (top_5_products,)


@app.cell
def _(orders):
    unshipped_orders = []

    for _order in orders:
        if not _order["shipped_date"]:
            unshipped_orders.append(_order)

    unshipped_count = len(unshipped_orders)

    print(f"Total unshipped orders: {unshipped_count}")

    print("\nOrders that have not shipped yet:")

    for _order in unshipped_orders:
        print(
            f"Order ID: {_order['order_id']} | "
            f"Customer: {_order['customer_name']} | "
            f"Order Date: {_order['order_date']}"
        )
    return unshipped_count, unshipped_orders


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Part 5: The Answer
    """)
    return


@app.cell
def _(
    days,
    order_count,
    revenue_exc_freight,
    sorted_countries,
    top_5_products,
    unshipped_count,
    unshipped_orders,
):
    def _():
        print("Northwind Shop - Weekly Report")
        print(f"Total Orders: {order_count}")
        print(f"Revenue (excluding freight): ${revenue_exc_freight:,.2f}")
        print(f"Unshipped Orders: {unshipped_count}")

        print()
        print("Revenue by Country")
        print(f"{'Country':<25}{'Revenue':>12}")
        for country, revenue in sorted_countries:
            print(f"{country:<25}${revenue:>11,.2f}")

        print()
        print("Top 5 Products")
        print(f"{'Product':<40}{'Units':>8}")
        for product, units in top_5_products:
            print(f"{product:<40}{units:>8}")

        print()
        print("Unshipped Order IDs")
        for order in unshipped_orders:
            print(order["order_id"])

        print()
        print("Manager Summary")
        return print(
            f"In the last {days} days, Northwind Shop received {order_count} orders, "
            f"generated ${revenue_exc_freight:,.2f} in revenue excluding freight, "
            f"and had {unshipped_count} orders that have not shipped."
        )


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Part 6: How I know these numbers are right
    """)
    return


@app.cell
def _(orders, revenue_exc_freight):
    def _():
        order_count = len(orders)
        orders_with_country = sum(1 for order in orders if order["ship_country"])

        print(f"Total Orders: {order_count}")
        print(f"Orders with a Country: {orders_with_country}")
        assert order_count == orders_with_country, "Order count and orders-with-country disagree!"

        total_order_value = sum(order["order_total_dollars"] for order in orders)
        print(f"Sum of order totals: ${total_order_value:,.2f}")
        print(f"Revenue reported above: ${revenue_exc_freight:,.2f}")
        assert abs(total_order_value - revenue_exc_freight) < 0.01, "These should match — same orders, same field."
        return print("Both checks agree.")


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 7: Working with the Agent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    AI suggested using `print()` instead of `return print()` because `print()` displays the results directly, while `return` is meant to send a value back from a function. I applied this in my **Revenue by Country** section, where I used a loop to display each country's revenue. I kept this approach because the same code can display results for any country in the data without having to write a separate print statement for each one. After doing this, I realized that using a `for` loop with `print()` was more efficient and readable than writing multiple individual print statements for each country.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Part 8: Reading it Back
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the revenue by country function, the input is the list of orders, each with a country and an order total, plus a descending argument that controls the sort order. The output is each country printed with its total revenue, ranked from highest to lowest when descending=True, or lowest to highest when descending=False; the function also returns this ranked list so it can be reused elsewhere, not just printed. The line I asked AI about was why the loop uses print() for each country instead of just returning the list once. I learned that print() inside the loop displays every country as the loop works through the list, while return only happens once the loop finishes, sending the finished list back to whatever called the function. If I call revenue_by_country_report(orders, descending=False) instead of leaving it at the default True, I think the countries with the lowest revenue will appear first instead of last.
    """)
    return


@app.cell
def _(orders):
    def revenue_by_country_report(orders, descending=True):
        totals = {}
        for _order in orders:
            country = _order["ship_country"]
            totals[country] = totals.get(country, 0) + _order["order_total_dollars"]

        ranked = sorted(totals.items(), key=lambda item: item[1], reverse=descending)

        print("Revenue by Country (Excluding Freight):")
        for country, revenue in ranked:
            print(f"{country}: ${revenue:,.2f}")
        return ranked

    revenue_by_country_report(orders, descending=False)  
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After completing the change and running it, my prediction was correct, calling the function with descending=False reversed the order of the list, and Venezuela, which had been at the top, moved to the bottom.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the unshipped orders function, the input is the list of orders and each one’s shipped_date, plus a want_shipped argument that decides which group to look for. The output is a count and a listing of whichever group matched: unshipped orders by default, or shipped orders if want_shipped=True. The line I wanted to understand is bool(o["shipped_date"]) == want_shipped. I learned that bool(o["shipped_date"]) turns the shipped date into True when it has a value and False when it’s empty, so the comparison only keeps orders whose shipped status matches what I asked for. I want to test what happens if I call the function with want_shipped=True instead of the default False; I expect it to return the shipped orders instead of the unshipped ones, and the new count should equal the total number of orders minus the original unshipped count.
    """)
    return


@app.cell
def _(orders):
    def unshipped_orders_report(orders, want_shipped=False):
        matches = [o for o in orders if bool(o["shipped_date"]) == want_shipped]
        label = "shipped" if want_shipped else "unshipped"

        print(f"Total {label} orders: {len(matches)}")
        for o in matches:
            print(f"Order ID: {o['order_id']} | Customer: {o['customer_name']} | Order Date: {o['order_date']}")
        return matches

    unshipped_orders_report(orders, want_shipped=True)  
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Originally, with want_shipped=False (the default), the function identified 20 unshipped orders. Calling it again with want_shipped=True identified 13 shipped orders. This matched my prediction because changing the argument changed which group of orders the comparison selected. Together, the 20 unshipped and 13 shipped orders equal the 33 total orders fetched for this run.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 9: Going Further
    """)
    return


@app.cell
def _(orders):
    revenue_by_day = {}

    for _order in orders:
        _day = _order["order_date"][:10]
        _revenue = _order["order_total_dollars"]

        if _day in revenue_by_day:
            revenue_by_day[_day] += _revenue
        else:
            revenue_by_day[_day] = _revenue

    revenue_by_day
    return (revenue_by_day,)


@app.cell
def _(revenue_by_day):
    import polars as pl

    revenue_by_day_df = pl.DataFrame({
        "day": list(revenue_by_day.keys()),
        "revenue": list(revenue_by_day.values()),
    }).sort("day")

    revenue_by_day_df
    return (revenue_by_day_df,)


@app.cell
def _(revenue_by_day_df):
    import altair as alt

    revenue_by_day_chart = alt.Chart(revenue_by_day_df).mark_bar().encode(
        x=alt.X("day:N", title="Day"),
        y=alt.Y("revenue:Q", title="Revenue ($)"),
        tooltip=["day", "revenue"]
    ).properties(
        title="Revenue by Day",
        width=500,
        height=300
    )

    revenue_by_day_chart
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Part 10: Time Spent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    4hrs
    """)
    return


if __name__ == "__main__":
    app.run()
