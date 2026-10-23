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


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
