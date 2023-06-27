from dash import dcc

generics_discount_tt = dcc.Markdown(
    """**Generics Discount** is the percentage reduction in productive value of the asset
    due to patent expiry. Factors had may contribute to this reduction include,
    generics introduced into the market, reduced leverage with insurers etc.
    """)

discount_rate_tt = dcc.Markdown(
    """**Discount Rate** is the expected rate of return on the asset. It is usually a measure of the
    risk of the asset's future cashflows.
    """
)

tax_rate_tt = dcc.Markdown(
    """**Tax Rate** is the company's taxation rate.
    """
)

sales_margin_tt = dcc.Markdown(
    """**Sales Margin** is the percentage profit made on sales after all expenses are accounted for.
    """
)

success_probability_tt = dcc.Markdown(
    """Probability of FDA Approval
    """
)
