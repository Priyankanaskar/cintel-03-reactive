
# import libraries----------------------------------------------------------------------------------------------------------------------------------
import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
import shinyswatch
import seaborn as sns
from faicons import icon_svg
from htmltools import css

# Theme
shinyswatch. theme.darkly()
# This package provides the Palmer Penguins dataset----------------------------------------------------------------------------------------------

from shiny import reactive, render, req
import seaborn as sns
import pandas as pd
import palmerpenguins
# Use the built-in function to load the Palmer Penguins dataset-----------------------------------------------------------------------------------------------
import seaborn as sns
penguins = sns.load_dataset("penguins")
penguins_df = load_penguins()



# Use the built-in function to load the Palmer Penguins dataset-----------------------------------------------------------------------------------------------------------
penguins_df = palmerpenguins.load_penguins()
penguins_df_r = penguins_df.rename(columns={"bill_depth_mm": "Bill Depth (mm)", "bill_length_mm": "Bill Length (mm)", 
"flipper_length_mm": "Flipper Length (mm)", "body_mass_g": "Body Mass (g)", "species": "Species", "island": "Island", "sex": "Sex", "year": "Year"})

# Name the page ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

ui.page_opts(title="Naskar's Penguin Data", fillable=False)

#Shiny UI sidebar for user interaction------------------------------------------------------------------------------------------------------------------------------------------------

with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    

# Create a dropdown input to choose a column -----------------------------------------------------------------------------------------------------------------------------------------------
    
    ui.input_selectize("selected_attribute", "Body Measurement", choices=["Bill Length (mm)", "Bill Depth (mm)", "Flipper Length (mm)", "Body Mass (g)"]) 
    
# Create a numeric input for the number of Plotly histogram bins----------------------------------------------------------------------------------------------------------------------------------
    
    ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 30)
    
# Create a slider input for the number of Seaborn bins---------------------------------------------------------------------------------------------------------------------------------------------
    
    ui.input_slider("seaborn_bin_count", "Seaborn Bin Count", 1, 100, 20)
    
# Create a checkbox group input to filter the species-------------------------------------------------------------------------------------------------------------------------------------------------
    ui.input_checkbox_group("selected_species_list", "Selected Species of Penguins", 
                            ["Adelie", "Gentoo", "Chinstrap"], selected="Adelie", inline=False)
    
 # Use ui.input_checkbox_group() to create a checkbox group input to filter the islands--------------------------------------------------------------------
    ui.input_checkbox_group(
        "selected_islands",
        "Islands in Graphs",
        ["Torgersen", "Biscoe", "Dream"],
        selected=["Torgersen", "Biscoe", "Dream"],
        inline=False,
    )
# Add a horizontal rule to the sidebar----------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    ui.hr()
    
# Add a hyperlink to the sidebar------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    
    ui.a("GitHub", href="https://github.com/Priyankanaskar/cintel-03-reactive", target="_blank")

        
# create a layout to include 2 cards with a data table and data grid------------------------------------------------------------------------------------------------------------------------------
with ui.accordion(id="acc", open="closed"):
    with ui.accordion_panel("Data Table"):
        @render.data_frame
        def penguin_datatable():
            return render.DataTable( filtered_data())

    with ui.accordion_panel("Data Grid"):
        @render.data_frame
        def penguin_datagrid():
            return render.DataGrid( filtered_data())
# Plot Charts----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ui.input_select("x", "Variable:",
                choices=["bill_length_mm", "bill_depth_mm"])
ui.input_select("dist", "Distribution:", choices=["hist", "kde"])
ui.input_checkbox("rug", "Show rug marks", value = False)


## Column


@render.plot
def displot():
    sns.displot(
        data=penguins, hue="species", multiple="stack",
        x=input.x(), rug=input.rug(), kind=input.dist())


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#Create Scatter plot
with ui.card(full_screen=True):

    ui.card_header("Plotly Scatterplot: Species")

    @render_plotly
    def plotly_scatterplot():
        # Create a Plotly scatterplot using Plotly Express
        return px.scatter(filtered_data(), x="Flipper Length (mm)", y="Bill Length (mm)", color="Species", 
                          facet_row="Species", facet_col="Sex", title="Penguin Scatterplot")

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Pie Chart plot
with ui.card(full_screen=True):

    ui.card_header("Plotly Pie Chart: Body Mass")

    @render_plotly
    def plotly_pie():
        pie_chart = px.pie(filtered_data(), values="Body Mass (g)", names="Island", title="Body mass on Islands")
        return pie_chart

    @render_plotly
    def plotly_pie_s():
        pie_chart = px.pie(filtered_data(), values="Body Mass (g)", names="Species", title="Body mass from Species")
        return pie_chart
        
# Card view for visualization---------------------------------------------------------------------------------------------------------------------------------------------------------

from shiny import App, ui

app_ui = ui.page_fillable(
    ui.layout_column_wrap(  
        ui.card("Card 1"),
        ui.card("Card 2"),
        ui.card("Card 3"),
        ui.card("Card 4"),
       width="2px",
        length="2px"
    ),
)

# The contents of the first 'page' is a navset with two 'panels'.
page1 = ui.navset_card_underline(
    ui.nav_panel("Plot", ui.output_plot("hist")),
    ui.nav_panel("Table", ui.output_data_frame("data")),
    footer=ui.input_select(
        "var", "Select variable", choices=["bill_length_mm", "body_mass_g"]
    ),
    title="Penguins data",
)

app_ui = ui.page_navbar(
    ui.nav_spacer(),  # Push the navbar items to the right
    ui.nav_panel("Page 1", page1),
    ui.nav_panel("Page 2", "This is the second 'page'."),

)


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Add a reactive calculation to filter the data
@reactive.calc
def filtered_data():
    return penguins_df_r[penguins_df_r["Species"].isin(input.selected_species_list())]
