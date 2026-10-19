# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *For a $400,000 loan, how does the monthy payment, total interest, and schedule compare between a 30-year mortgage at a 7.03% and a 15-year mortgage at 6.42%*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *I will start by calculating how much you would need to pay each month for each loan option. Then, I'll observe how each payment is divided between interest and principal. Eventually, as you make payments, your remaining loan balance gets smaller, meaning that you gradually pay less in interest. Next, I will calculate how much interest you would pay in total for each loan option to see which one costs less overall. My loop carries the remaining interest from one month to the next. In section 6, I will add up all the payments used to repay the loan, excluding interest. Therefore, it should match the original amount borrowed.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    loan_amount = 400000
    annual_rates = {30: 0.0703, 15: 0.0642}
    return annual_rates, loan_amount


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(annual_rates, loan_amount):
    term_years = 30
    r = annual_rates[term_years] / 12
    n = term_years * 12
    payment = loan_amount * r / (1 - (1 + r) ** -n)
    payment
    return


@app.cell
def _(annual_rates, loan_amount):
    payments = {}
    for _term_years in annual_rates:
        _r = annual_rates[_term_years] / 12
        _n = _term_years * 12
        payments[_term_years] = round(loan_amount * _r / (1 - (1 + _r) ** -_n), 2)
    payments
    return (payments,)


@app.cell
def _(annual_rates, loan_amount):
    schedules = {}
    for _term_years in annual_rates:
        _r = annual_rates[_term_years] / 12
        _n = _term_years * 12
        _payment = round(loan_amount * _r / (1 - (1 + _r) ** -_n), 2)

        _balance = loan_amount
        _schedule = []
        for _month in range(1, _n + 1):
            _interest = round(_balance * _r, 2)
            if _month < _n:
                _principal = round(_payment - _interest, 2)
                _payment_due = _payment
            else:
                _principal = _balance
                _payment_due = round(_interest + _principal, 2)
            _balance = round(_balance - _principal, 2)
            _schedule.append({
                "month": _month,
                "payment": _payment,
                "interest": _interest,
                "principal": _principal,
                "balance": _balance,
            })
        schedules[_term_years] = _schedule

    for _term_years in annual_rates:
            print(f"\n{_term_years}-year loan schedule")
            print(f"{'Month':>5} {'Payment':>12} {'Interest':>12} {'Principal':>12} {'Balance':>14}")
            for _row in schedules[_term_years]:
                print(
                    f"{_row['month']:>5} "
                    f"{_row['payment']:>12,.2f} "
                    f"{_row['interest']:>12,.2f} "
                    f"{_row['principal']:>12,.2f} "
                    f"{_row['balance']:>14,.2f}"
                )
    return (schedules,)


@app.cell
def _(annual_rates, loan_amount):
    extra_payment = 200

    schedules_extra = {}
    for _term_years in annual_rates:
        _r = annual_rates[_term_years] / 12
        _n = _term_years * 12
        _payment = round(loan_amount * _r / (1 - (1 + _r) ** -_n), 2)

        _balance = loan_amount
        _schedule = []
        for _month in range(1, _n + 1):
            _interest = round(_balance * _r, 2)
            _principal = round(_payment + extra_payment - _interest, 2)
            if _principal > _balance:
                _principal = _balance
            _balance = round(_balance - _principal, 2)
            _schedule.append({
                "month": _month,
                "payment": _payment + extra_payment,
                "interest": _interest,
                "principal": _principal,
                "balance": _balance,
            })
            if _balance <= 0:
                break
        schedules_extra[_term_years] = _schedule

    schedules_extra
    return (schedules_extra,)


@app.cell
def _(annual_rates, schedules, schedules_extra, total_interest):
    months_saved = {}
    interest_saved = {}
    for _term_years in annual_rates:
        months_saved[_term_years] = len(schedules[_term_years]) - len(schedules_extra[_term_years])
        _total_interest_extra = round(sum(row["interest"] for row in schedules_extra[_term_years]), 2)
        interest_saved[_term_years] = round(total_interest[_term_years] - _total_interest_extra, 2)

    for _term_years in annual_rates:
        print(f"{_term_years}-year loan: pays off {months_saved[_term_years]} months sooner, saving ${interest_saved[_term_years]:,.2f} in interest.")
    return


@app.cell
def _(schedules):
    schedules[30][-1]
    ["balance"]
    return


@app.cell
def _(schedules):
    len(schedules[30])
    return


@app.cell
def _(annual_rates, schedules):
    def _():
        total_interest = {}
        for term_years in annual_rates:
            total_interest[term_years] = round(sum(row["interest"] for row in schedules[term_years]),2)
        return total_interest


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(annual_rates, schedules):
    total_interest = {}
    for _term_years in annual_rates:
        total_interest[_term_years] = round(sum(row["interest"] for row in schedules[_term_years]), 2)
    total_interest
    return (total_interest,)


@app.cell
def _(annual_rates, payments, total_interest):
    def _():
        for term_years in annual_rates:
            print(f"{term_years}-year loan: payment = ${payments[term_years]:,.2f}, total interest = ${total_interest[term_years]:,.2f}")
            print(f"For a $400,000 loan, the 30-year mortgage at 7.03% has a lower monthly payment  (${payments[30]:,.2f})"
                  f"than the 15-year at 6.42% (${payments[15]:,.2f}), but the 15-year loan saves"
                  f"${total_interest[30] - total_interest[15]:,.2f} in total interest over the life of the loan")


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(annual_rates, loan_amount, schedules):
    def _():
        for term_years in annual_rates:
            total_principal_paid = round(sum(row["principal"] for row in schedules[term_years]), 2)
            final_balance = schedules[term_years][-1]["balance"]
            print(f"{term_years}-year: total principal paid =    ${total_principal_paid:,.2f}, loan amount = ${loan_amount:,.2f}, final balance = {final_balance}")


    _()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *I summed the principal-paid column across each schedule and compared it to the original loan amount, which summed to $ 400,000, matching the loan amount exactly. With a final balance of $0.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *When I was completing section 5, the AI agent suggested adding "return" before printing statements; however, I did not take it because it would have returned "none" instead of the sentence itself. I was getting errors, and the code wasn't running properly, in addition to other errors that contributed.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Working with AI, I aimed to complete the what if you pay an extra $200 every month. How many months, and how much interest, does that save on each loan? Speaking with my agent, I told it I was thinking to just add "Schedule extra" to the exisitng table we had. The AI agent liked the idea, and by itself computed the code in the tables. However, there were areas I did not understand at first glance. For example, the AI used a function called `amortization_schedule` that took an additional parameter, `extra_payment`, and recalculated the balance after each month by subtracting both the regular payment and the extra $200 from the principal. I had to trace through the logic manually to understand how the extra payment was reducing the loan term and the total interest paid, since the function reused the same loop structure as the original schedule but added a conditional check to stop once the balance reached zero.*
    """)
    return


if __name__ == "__main__":
    app.run()
