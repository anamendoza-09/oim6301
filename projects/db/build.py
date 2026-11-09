import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import polars as pl

    database = mo.notebook_dir() / "database.duckdb"
    data_dir = mo.notebook_dir() / "data"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return ask, data_dir, database, duckdb, mo, pl


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #Babson Bean Café: Building the Database
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #1. The Tables
    """)
    return


@app.cell
def _(data_dir, database, duckdb):
    database.unlink(missing_ok=True)
    database.with_name(database.name + ".wal").unlink(missing_ok=True)

    TABLES = """
    CREATE TABLE members (
        member_id       INTEGER PRIMARY KEY,
        first_name      VARCHAR NOT NULL,
        mobile          VARCHAR NOT NULL UNIQUE,
        email           VARCHAR,                      -- optional
        join_date       DATE    NOT NULL,
        points_balance  INTEGER NOT NULL DEFAULT 0 CHECK (points_balance >= 0)
    );

    CREATE TABLE products (
        product_id      INTEGER PRIMARY KEY,
        name            VARCHAR NOT NULL UNIQUE,
        category        VARCHAR NOT NULL
                        CHECK (category IN ('coffee', 'tea', 'food', 'other')),
        price           DECIMAL(6, 2) NOT NULL,
        cost            DECIMAL(6, 2) NOT NULL CHECK (cost >= 0),
        available_today BOOLEAN NOT NULL DEFAULT TRUE,
        CHECK (price >= cost)                         -- never priced below cost
    );

    CREATE TABLE options (
        option_id       INTEGER PRIMARY KEY,
        name            VARCHAR NOT NULL UNIQUE,
        price           DECIMAL(6, 2) NOT NULL CHECK (price >= 0),   -- can be zero
        cost            DECIMAL(6, 2) NOT NULL CHECK (cost >= 0)
    );

    CREATE TABLE orders (
        order_id        INTEGER PRIMARY KEY,
        ordered_at      TIMESTAMP NOT NULL,
        member_id       INTEGER REFERENCES members (member_id),      -- optional
        channel         VARCHAR NOT NULL CHECK (channel IN ('counter', 'app'))
    );

    CREATE TABLE order_lines (
        line_id         INTEGER PRIMARY KEY,
        order_id        INTEGER NOT NULL REFERENCES orders (order_id),
        product_id      INTEGER NOT NULL REFERENCES products (product_id),
        quantity        INTEGER NOT NULL CHECK (quantity > 0),
        unit_price      DECIMAL(6, 2) NOT NULL CHECK (unit_price >= 0)
    );

    CREATE TABLE line_options (
        line_id         INTEGER NOT NULL REFERENCES order_lines (line_id),
        option_id       INTEGER NOT NULL REFERENCES options (option_id),
        price_charged   DECIMAL(6, 2) NOT NULL CHECK (price_charged >= 0),
        PRIMARY KEY (line_id, option_id)              -- at most once per line
    );

    CREATE TABLE payments (
        payment_id      INTEGER PRIMARY KEY,
        order_id        INTEGER NOT NULL REFERENCES orders (order_id),
        method          VARCHAR NOT NULL
                        CHECK (method IN ('cash', 'card', 'app', 'points')),
        amount          DECIMAL(8, 2) NOT NULL CHECK (amount > 0)
    );
    """

    LOAD_ORDER = ["members", "products", "options", "orders",
                  "order_lines", "line_options", "payments"]

    VIEW = """
    CREATE VIEW weekly_sales AS
    WITH line_totals AS (
        SELECT
            l.line_id,
            l.order_id,
            l.quantity * (l.unit_price + COALESCE(SUM(lo.price_charged), 0)) AS line_revenue
        FROM order_lines AS l
        LEFT JOIN line_options AS lo ON lo.line_id = l.line_id
        GROUP BY l.line_id, l.order_id, l.quantity, l.unit_price
    )
    SELECT
        date_trunc('week', o.ordered_at)::DATE AS week_starting,
        COUNT(DISTINCT o.order_id)             AS orders,
        SUM(lt.line_revenue)                   AS revenue,
        ROUND(SUM(lt.line_revenue) / COUNT(DISTINCT o.order_id), 2) AS avg_order
    FROM orders AS o
    JOIN line_totals AS lt ON lt.order_id = o.order_id
    GROUP BY week_starting
    ORDER BY week_starting
    """

    with duckdb.connect(database) as _con:
        _con.execute(TABLES)
        for _table in LOAD_ORDER:
            _csv = (data_dir / f"{_table}.csv").as_posix()
            _con.execute(
                f"INSERT INTO {_table} SELECT * FROM read_csv('{_csv}', header = true)"
            )
        _con.execute(VIEW)

    built = True
    return (built,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #3. Look at the Data
    """)
    return


@app.cell
def _(data_dir, pl):
    orders_by_hour = (
        pl.read_csv(data_dir / "orders.csv", try_parse_dates=True)
        .with_columns(pl.col("ordered_at").dt.hour().alias("hour"))
        .group_by("hour")
        .agg(pl.len().alias("orders"))
        .sort("hour")
    )
    orders_by_hour.plot.bar(x="hour:O", y="orders").properties(
        title="Orders by hour of the day", width=500
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #4. Row Counts
    """)
    return


@app.cell
def _(ask, built):
    _ = built
    ask("""
        SELECT 'members'      AS table_name, COUNT(*) AS row_count FROM members
        UNION ALL SELECT 'products',     COUNT(*) FROM products
        UNION ALL SELECT 'options',      COUNT(*) FROM options
        UNION ALL SELECT 'orders',       COUNT(*) FROM orders
        UNION ALL SELECT 'order_lines',  COUNT(*) FROM order_lines
        UNION ALL SELECT 'line_options', COUNT(*) FROM line_options
        UNION ALL SELECT 'payments',     COUNT(*) FROM payments
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 5. A Row It Refuses

    A product priced below its cost breaks the rule *a menu price is never below its
    cost*. The insert runs in its own short write connection, inside `try`/`except`,
    so the notebook keeps going after the database says no.
    """)
    return


@app.cell
def _(built, database, duckdb):
    _ = built
    try:
        with duckdb.connect(database) as _con:
            _con.execute("""
                INSERT INTO products VALUES
                    (99, 'Loss Leader Latte', 'coffee', 1.00, 1.20, TRUE)
            """)
        refused = "The row was accepted. The CHECK is missing!"
    except duckdb.Error as error:
        refused = f"Refused: {error}"
    refused
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #6. Answers You Already Knew
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    **6a. What dates do the orders cover?**
    Expected: first order on 2025-11-08, last on 2026-11-07 (the 12 months up to as_of).
    """)
    return


@app.cell
def _(ask, built):
    _ = built
    ask("""
        SELECT MIN(ordered_at)::DATE AS first_order,
               MAX(ordered_at)::DATE AS last_order
        FROM orders
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    **6b. Which product has never sold?**
    Expected: exactly one, Matcha Cookie, which I asked for as a row with nothing
    attached.
    """)
    return


@app.cell
def _(ask, built):
    _ = built
    ask("""
        SELECT p.name
        FROM products AS p
        LEFT JOIN order_lines AS l ON l.product_id = p.product_id
        WHERE l.line_id IS NULL
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    **6c. Which options are free?**
    Expected: exactly one, Extra Hot, at $0.00 (the scenario says an option's price
    can be zero).
    """)
    return


@app.cell
def _(ask, built):
    _ = built
    ask("SELECT name, price FROM options WHERE price = 0")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 7. A View

    **Weekly question: how many orders and how much revenue did we take each week?**
    """)
    return


@app.cell
def _(ask, built):
    _ = built
    ask("SELECT * FROM weekly_sales ORDER BY week_starting DESC LIMIT 8")
    return


if __name__ == "__main__":
    app.run()
