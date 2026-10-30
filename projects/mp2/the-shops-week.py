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
    How many orders were placed in the last seven days, and how much revenue did they generate, excluding freight? Which countries generated the most revenue, what are our top five best-selling products based on units sold, and which orders have not shipped yet?
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
    from datetime import date, timedelta

    url = "https://oim.zhili.dev/shop/orders"

    today = date.today()
    start_date = today - timedelta(days=days - 1)

    response = requests.get(
        url,
        params={
            "from_date": start_date.isoformat(),
            "to_date": today.isoformat()
        },
        timeout=30
    )

    response.raise_for_status()

    orders_data = response.json()

    print("Status code:", response.status_code)
    print("Data type:", type(orders_data))
    print("API data:", orders_data)

    return orders_data, requests


@app.cell
def _(orders_data):
    orders = orders_data["items"]
    order_count = len(orders)
    order_count
    return order_count, orders


@app.cell
def _(order_count, orders):
    revenue_exc_freight = 0
    for order in orders:
        revenue_exc_freight += order["order_total_dollars"]- order["freight_dollars"]
        revenue_exc_freight
   
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
def _(orders, requests):
    units_by_product = {}

    for _order in orders:
        order_id = _order["order_id"]

        # Get the product details for each order
        detail_response = requests.get(
            f"https://oim.zhili.dev/shop/orders/{order_id}",
            timeout=30
        )
        detail_response.raise_for_status()
        detail = detail_response.json()

        if "lines" in detail:
            lines = detail["lines"]
        elif "order_details" in detail:
            lines = detail["order_details"]
        elif "items" in detail:
            lines = detail["items"]
        else:
            raise KeyError(
                f"Cannot find product lines: {list(detail.keys())}"
            )

        for line in lines:
            product = line.get("product_name", line.get("product_id"))
            quantity = line["quantity"]

            if product in units_by_product:
                units_by_product[product] += quantity
            else:
                units_by_product[product] = quantity

    top_5_products = sorted(
        units_by_product.items(),
        key=lambda item: item[1],
        reverse=True
    )[:5]

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
def _(orders):

    print(f"Total Orders: {len(orders)}")
    print(f"Orders with a Country: {sum(1 for order in orders if order['ship_country'])}")


    return


@app.cell
def _(orders):
    sum(order["order_total_dollars"] for order in orders)
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
    For the revenue by country cell, the input is The orders and their revenue amounts, along with the country associated with each order. While the output is a list of countries and the total revenue generated by each country in order by the largest to least amount of revenue. The Line I asked AI about was why I should use `print()` instead of `return print()`. I learned that `print()` displays the results, and using it inside a loop allows me to display every country without writing separate statements. If I change the true to false, I think the countries with the lowest revenues will appear.
    """)
    return


@app.cell
def _(orders):
    def _():
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
            reverse=False
        )

        print("Revenue by Country (Excluding Freight):")

        for country, revenue in sorted_countries:
            print(f"{country}: ${revenue:,.2f}")


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After completing the change and running it, my prediction was correct, and it displayed it by changing the order in which the list is presented, Venezuela, being the top of the list before, moved to the bottom of the list.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For the unshipped order cell, the input is the list of orders and their shipping dates. While the output is the number of orders that have not shipped, along with their order information. The line I wanted to understand is `if not _order["shipped_date"]`. I learned that `not` checks whether the shipping date is missing. However, I want to test If I remove `not` from the condition, I expect the code to count shipped orders instead of unshipped orders. So the new count should equal the total number of orders minus the original unshipped count.
    """)
    return


@app.cell
def _(orders):
    def _():
        unshipped_orders = []

        for _order in orders:
            if _order["shipped_date"]:
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


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Originally, With not, the code identified 17 unshipped orders. After removing not, it identified 5 shipped orders. This matched my prediction because the condition changed which orders were selected. Together, the 17 unshipped and 5 shipped orders equal the original 22 orders.
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
