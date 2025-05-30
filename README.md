# MX Actual Time of Delivery (ATD) Streamlit Dashboard Overview

At Uber Eats, delivering food at the right time isn’t just about logistics — **it’s about trust**. Every late delivery risks a poor customer experience, while every minute of inefficiency affects the bottom line. In a marketplace defined by real-time demand, weather variability, and courier availability, **understanding and improving delivery accuracy is a constant challenge — and a major opportunity**.

This Streamlit dashboard is designed as a tool that can inform decision-making and directly support teams responsible for dispatch planning, courier incentives, and ETA reliability — contributing to smarter, data-driven operations at scale.

---
## Project Overview
- [README.md](/README.md) – 📘 Project usage, setup, and documentation
- [.gitignore](/.gitignore) – Files to be excluded from commits
- [streamlit_app.py](/streamlit_app.py) - 🚀 Main entry point for the Streamlit dashboard
- [views/](/views) – 📊 Individual Streamlit views
    - [home.py](/views/home.py) – Home page with context and instructions
    - [atd_view.py](/views/atd_view.py) – Core ATD dashboard page
- [modules/](/modules) – 🧠 Modular backend logic
    - [controllers/](/modules/controllers/)
        - [atd_view_controller.py](/modules/controllers/atd_view_controller.py) – Business logic for dashboard metrics
    - [admin/](/modules/admin/)
        - [dataspitter.py](/modules/admin/dataspitter.py) – Data loading and preprocessing logic
- [assets/](/assets) – 🖼️ Static resources (CSS and images used in the app)
- [config/](/config)
    -  [constants.py](/config/constants.py) – 🔧 Central definitions (columns, toggles, colors)
-  [data/](/data) – 📁 Where Input/output files store.
-  [requirements/](/requirements)
     - [requirements.txt](/requirements/requirements.txt) – 📦 Dependency list
 - [utils/](/utils) - Common used methods for data processing.

---
 
## Key metrics (from orginal [Data Source - BC_A&A_with_ATD.csv](https://drive.google.com/file/d/1JOlK0MKo11p2wI3rDnxIzvVzGg-oVPnw/view?usp=sharing)):

1. **Region (string)**: The broader region the city belongs to. *(e.g. "Mexico")*. 
2. **Territory (string)**: A subdivision within a region that denotes a more specific zone, such as a territorial division or operational area *(e.g., "Central", "North", "West", "South East", "Long Tail - Region")*.
3. **Country Name (string)**: The name of the country where the delivery or service is being performed, represented by its common name *(e.g. "Mexico")*. 
4. **Workflow UUID (string)**: A unique global identifier (UUID) assigned to a specific workflow, used to track an order or process within the system *(e.g. "8c393c94-9282-41a6-a885-7a6e84b470d7")*. 
5. **Driver UUID (string)**: A unique global identifier (UUID) assigned to the driver or courier responsible for completing the delivery or task related to the workflow *(e.g. "d16e401c-795d-4295-96c0-85ca08ad8c42")*.
6. **Delivery Trip UUID (string)**: A unique global identifier (UUID) associated with a specific delivery trip within a workflow *(e.g. "715f96aa-0a31-46f6-b856-6ea6f87affad")*.
7. **Courier Flow (string)**: The type of transport used by the courier to complete the delivery *(e.g. "Motorbike", "UberEats", "Logistics")*.
8. **Restaurant Offered Timestamp UTC (timestamp)**: The date and time in UTC when the restaurant received the order and began processing it *(e.g. 2025-03-23 02:14:55.000)*.
9. **Order Final State Timestamp Local (timestamp)**: The local date and time when the order reached its final state, for example, when the delivery was completed or the order reached its final status *(e.g. 2025-03-22 21:05:52)*.
10. **Eater Request Timestamp Local (timestamp)**: The local date and time when the customer made the delivery request, when the order was created *(e.g. 2025-03-22 20:14:54)*.
11. **Geo Archetype (string)**: The type of geolocation associated with the order, defined as a strategic region for marketing efforts *(e.g. "Play offense", "Drive momentum", "Defend CP", "Build experience")*.
12. **Merchant Surface (string)**: The type of device or interface used by the merchant (restaurant) to interact with the system *(e.g. "Tablet", "POS", "Web/Mobile", "Unspecified", "Other")*.
13. **Pickup Distance (float)**: The distance in kilometers from the driver accept to the pickup point of the order, such as the restaurant *(e.g. 3.448)*.
14. **Dropoff Distance (float)**: The distance in kilometers from the pickup point to the final delivery destination, such as the customer's address *(e.g. 6.451)*.
15. **Actual Time of Delivery - ATD (float)**: The total time, in minutes, it takes from when the order is offered to the restaurant *(Restaurant Offered Timestamp UTC)* until it is delivered to the final destination *(Order Final State Timestamp Local)*. This is a measure of the total delivery time, including both preparation and transit time. *(e.g. 50.96666666666667)*.

### Additional metrics (calculated from orginal [data source](https://drive.google.com/file/d/1JOlK0MKo11p2wI3rDnxIzvVzGg-oVPnw/view?usp=sharing) and added to [.parquet file](modules/admin/dataspitter.py))

1. **Hour (int64)**: The hour of the day (0–23) extracted from the Eater Request Timestamp Local. *(e.g. 14)*

2. **Weekday (string)**: The day of the week when the order was placed, based on Eater Request Timestamp Local. *(e.g. "Monday", "Saturday")*

3. **Day (datetime)**: The calendar date (with time set to 00:00:00) when the order was placed. *(e.g. "2025-03-22 00:00:00")*

4. **Week (datetime)**: The start date (Monday) of the week during which the order was placed. *(e.g. "2025-03-17")*

5. **Month (datetime)**: The first day of the month in which the order was placed. *(e.g. "2025-03-01")*

6. **Time of Day (string)**: A label categorizing the hour of day when the order was placed into one of four buckets:
   - `"Breakfast"`: 5–11
   - `"Lunch"`: 12–16
   - `"Dinner"`: 17–23
   - `"Late Night"`: 0–4  

7. **Is Weekend? (boolean)**: `True` if the order was placed on a Saturday or Sunday, based on the Eater Request Timestamp Local. *(e.g. True)*

8. **Is Holiday? (boolean)**: `True` if the order was placed on a recognized holiday or seasonality date. This includes both fixed-date holidays (e.g. "Dec 25") and custom dates like "Super Bowl" *(e.g. False)*.

9. **Total Distance (float)**: Sum of `Pickup Distance` and `Dropoff Distance` to gather the totality distance (in kilometers) of the trip. (e.g. 4.5769997)


---

## Requirements
- **Python Version**: Python 3.9


## Installation Guide

#### Open a new terminal and go to the folder where you want to clone your repo.

##### Optional: Improve Your Bash Prompt (Bash 5.2+)
If you're using a terminal with Bash 5.2 (e.g., inside a Docker container or minimal Linux shell), you might see a blank or minimal prompt. To make it more useful, you can customize your shell prompt by updating the ~/.bashrc file.
```bash
echo 'export PS1="\u:\w\$ "' >> ~/.bashrc
```
```bash
source ~/.bashrc
```
As a result you should see your prompt with sometring like this:
```bash
yourusername:/your/current/path$
```

#### Git clone (preferably on your root folder):
```bash
git clone https://github.com/mariana-gtz/atd_bc_aa.git
```

#### Create a virtual environment:
```bash
conda create -p $VIRTUAL_ENV_DIR/atd_bc_aa python=3.9 -y
```

#### Activate the env
```bash
conda activate \$VIRTUAL_ENV_DIR/atd_bc_aa/
```

#### To install packages:
- First upgrade pip.
```bash
$VIRTUAL_ENV_DIR/atd_bc_aa/bin/pip install --upgrade pip
```

- Now go to the **atd_bc_aa/requirements** folder and install required libraries.
```bash
cd atd_bc_aa/requirements
```
```bash
$VIRTUAL_ENV_DIR/atd_bc_aa/bin/pip install --force-reinstall --no-cache-dir -r requirements.txt
```

- Check all installations are correct. Output should be **No broken requirements found.**
```bash
$VIRTUAL_ENV_DIR/atd_bc_aa/bin/pip check
```


#### Download needed data:
- Go to [this link](https://drive.google.com/file/d/1JOlK0MKo11p2wI3rDnxIzvVzGg-oVPnw/view?usp=sharing) and download the data.
- Go to your `data` folder and drag and drop the downloaded file. **File must be named: BC_A&A_with_ATD.csv**
- In your terminal, go to the `modules/admin/` folder
```bash
cd atd_bc_aa/modules/admin
```
- With your activated conda environment, run
```bash
python dataspitter.py
```
- Your terminal will start processing the csv and create the necessary files.


#### FINALLY! Run your streamlit_app
If not on your project's root folder, navigate to it.
```bash
cd atd_bc_aa/
```

On your project's root folder, run the app.
```bash
streamlit run streamlit_app.py 
```


## Notes and Observations
- **Known Limitations**: Data availability might not be complete and affect some visualizations.
- **Future Development Plans**: Incorporation of weather metrics could be useful.


## Contact
For questions or issues, contact:
- **Email**: mariana.gutierrez@uber.com
