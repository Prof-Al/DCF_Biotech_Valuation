import dash
import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Portfolio Overview", href="/")),
        dbc.NavItem(dbc.NavLink("Global Parameters", href="/parameters")),
        # dbc.NavItem(dbc.NavLink("Assets", href="/assets")),
        # dbc.NavItem(dbc.NavLink("Add Asset", href="/add_asset")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Assets", href="/assets"),
                dbc.DropdownMenuItem("Add Asset", href="/add_asset"),
            ],
            label="Asset"
        )
        # dbc.DropdownMenu(
        #     children=[
        #         # dbc.DropdownMenuItem("More pages", header=True),
        #         # dbc.DropdownMenuItem(
        #         #     f"{page['name']}, href={page['relative_path']}"
        #         # )
        #         # for page in dash.page_registry.values()
        #         dbc.DropdownMenuItem("Community forums", href="https://community.okama.io"),
        #         # dbc.DropdownMenuItem("Compare Assets", href="/")
        #     ],
        #     nav=True,
        #     in_navbar=True,
        #     label="More",
        # ),
    ],
    brand="DCF Valuation",
    brand_href="/",
    color="primary",
    dark=True,
)