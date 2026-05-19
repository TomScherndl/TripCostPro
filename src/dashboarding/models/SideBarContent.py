from dashboarding.models.TabNames import TabNames

OVERVIEW_SIDEBAR_CONTENT = """
## HELP: Overview Dashboard
Welcome to the central commodity dashboard. This page provides current commodity prices.

### Core Market Tracking
We monitor critical energy sources, including:
*   **Electric Energy:** electricity pricing (energy market - not company specific load prices).
*   **Fossil Fuels:** liquid fossilized fuels (e.g., diesel, gasoline).

### Functionality
Utilize the integrated Date Picker to analyze historical data and compare pricing across specific time periods.

### Market Insights
The dashboard highlights key price changes using delta metrics (percentage change) to quickly indicate market direction (up or down). This allows users to monitor immediate volatility and trend shifts within the commodity sector.

*Recommendation: Use this section for initial assessment of current market conditions.*
"""
PRICES_SIDEBAR_CONTENT = """
## HELP: Historical Price Analysis
This section provides an advanced view into commodity pricing dynamics, allowing users to conduct detailed comparative analysis.

### Key Features
*   **Comparative Charting:** View multiple commodities overlaid on a single line chart for direct price comparison and correlation study.
*   **Electricity Data:** Monitor real-time and historical electricity rates and supply trends.
*   **Fuel Commodity Tracking:** Detailed pricing information for various fuel types, including diesel and gasoline.

### Interactive Controls
Use the integrated range sliders to adjust the data visualization parameters (date ranges, price floors/ceilings). This enables dynamic filtering and detailed analysis of specific market segments.

*This module is designed for deep dive financial and energy sector analysis.*
"""
TRIP_PLANNER_SIDEBAR_CONTENT = """
## HELP: Trip Planning Tool
The Trip Planner facilitates comprehensive journey cost estimation by integrating various travel parameters. This tool provides a reliable assessment of travel feasibility based on current commodity pricing.

### Inputs and Parameters
Users can define the following variables for calculation:
*   **Date Selection:** Specifies the desired date of travel for accurate, time-specific cost projections.
*   **Distance Calculation:** Input field to define the total distance (e.g., kilometers) of the planned route.
*   **Budget Allocation:** Allows users to set a financial budget constraint for trip planning.

### Core Calculations
The system calculates the estimated costs based on three primary factors:
1.  Electricity Consumption Cost
2.  Fuel Expenditure Cost
3.  Total Budget Constraint Compliance (Flagged upon successful calculation).

*Output provides an immediate assessment of whether the planned journey is fiscally viable within the specified budget.*
"""

CARS_SIDEBAR_CONTENT = """
## HELP: Vehicle Fleet Management
This command center allows users to manage and dynamically update vehicle data, ensuring accurate fuel consumption calculations for trip planning.

### Core Functionality
*   **Dynamic Data Editor:** Provides an interface for adding, editing, or removing entries in the vehicle fleet database.
*   **Commodity Integration:** Supports tracking various energy sources, including traditional fossil fuels (Diesel) and electric power (kWh).
*   **Consumption Metrics:** Tracks fuel efficiency using standard units such as liters per 100km (l/100km) or kilowatt-hours per 100km (kWh/100km).
*   **Scalability:** Supports managing diverse vehicle types, from internal combustion engine vehicles to electric models.

*Note: All modifications made within this module are instantly reflected and utilized in the Trip Planner calculations.*
"""
