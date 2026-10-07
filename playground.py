import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    # Review of Session 5
     # Q1 Which parts pick the record?
    orders = [
        {"OrderID": 10248, "ShipCountry": "France"},
        {"OrderID": 10249, "ShipCountry": "Germany"},
    ]
    orders[0]["ShipCountry"]
    # Answer: 0
    return (orders,)


@app.cell
def _(orders):
    # Q2: What happens here?
    orders["ShipCountry"]
    # There is an error because orders is a list, which means we can only use an integer to refer to any item in it. 
    return


@app.cell
def _(orders):
    countries = []
    for order in orders:
        # print(type(order))
        print(order['OrderID'], order['ShipCountry'])
        countries.append(order['ShipCountry'])
    len(set(countries))
    return


@app.cell
def _():
    #Q3
    return


app._unparsable_cell(
    r"""
    # A list starts with square bracketsmy_list = [1, 2, 3, 4, 5]
    # We need to put a [0] in fronto fo the list```python
    my_list = [0] + my_list
    ```

    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
