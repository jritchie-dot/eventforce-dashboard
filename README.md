# 🎯 Eventforce Pipeline Dashboard

An interactive Streamlit dashboard for visualizing event pipeline metrics, including ETOP (Events Touched Open Pipe), attendance data, and event performance analysis.

## Features

### 📊 Key Metrics
- **Total Events Overview** - Complete event count with ETOP and attendance tracking
- **Pipeline Analysis** - Total ETOP across all events
- **Attendance Tracking** - Total attendees and average per event
- **Efficiency Metrics** - Average ETOP per attendee

### 📈 Visualizations

1. **Attendance vs ETOP Correlation** - Interactive scatter plot showing relationship between event size and pipeline
2. **Top Events by Attendance** - Ranked bar chart of highest-attended events
3. **Top Events by ETOP** - Pipeline performance leaders
4. **ETOP per Attendee Efficiency** - Which events generate most pipeline per person
5. **Event Status Breakdown** - Distribution across Complete, Assigned, New, Canceled
6. **Event Lead Performance** - Top performers by total ETOP
7. **Data Quality Checks** - Identifies events missing critical data

### 🎛️ Interactive Features

- **Event Type Filters** - World Tour, Dreamforce, TDX, Peak Performers, Summits, etc.
- **Minimum ETOP Threshold** - Focus on high-value events
- **Tabbed Data Views**:
  - All Events
  - Events with Attendance
  - Missing Attendance (data quality flags)
- **CSV Export** - Download filtered data

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/jritchie-dot/eventforce-dashboard.git
cd eventforce-dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Prepare your data file:
   - Export your event data as CSV
   - Update the `csv_path` variable in `eventforce_dashboard.py` (line 20) to point to your CSV file

## Usage

Run the dashboard:
```bash
streamlit run eventforce_dashboard.py
```

The dashboard will open in your default browser at `http://localhost:8501`

## Data Format

Your CSV file should include these columns:

| Column Name | Description | Required |
|------------|-------------|----------|
| `Event: Event Name` | Name of the event | Yes |
| `Events Touched Open Pipe (ETOP)` | Pipeline value in currency | Yes |
| `Total Actual Attendance` | Number of attendees | Recommended |
| `Event Status` | Complete, Assigned, New, Canceled | Recommended |
| `Event Lead` | Person responsible for event | Optional |
| `Event Start Date` | Event date | Optional |
| `Event Category` | External Customer, Internal Employee, etc. | Optional |
| `Total Event Budget` | Total budget amount | Optional |
| `Security Budget` | Security costs | Optional |
| `Total Medical Costs` | Medical costs | Optional |

### Example CSV Structure:
```csv
"Event: Event Name","Events Touched Open Pipe (ETOP)","Total Actual Attendance","Event Status"
"World Tour NYC FY27","220000000","7676","Complete"
"TDX26","399200000","6200","Assigned"
```

## Key Insights

The dashboard helps answer questions like:
- Which events generate the most pipeline?
- What's the relationship between attendance and ETOP?
- Which events are most efficient (ETOP per attendee)?
- What events are missing critical data?
- How do different event types perform?
- Which event leads drive the most pipeline?

## Project Structure

```
eventforce-dashboard/
├── eventforce_dashboard.py    # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── DASHBOARD_UPDATES.md        # Changelog and update notes
├── event_data_summary.md       # Sample data summary
└── .gitignore                  # Git ignore rules
```

## Technologies

- **[Streamlit](https://streamlit.io/)** - Interactive web application framework
- **[Plotly](https://plotly.com/)** - Interactive visualizations
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation and analysis
- **[NumPy](https://numpy.org/)** - Numerical computing

## Screenshots

### Dashboard Overview
The dashboard provides a comprehensive view with 5 key metric cards at the top, followed by interactive charts and filterable tables.

### Attendance Analysis
Scatter plot visualization correlates attendance with ETOP, using bubble size and color to show efficiency metrics.

### Data Quality
Built-in data quality checks identify events missing attendance data, helping ensure complete reporting.

## Contributing

This is a private dashboard tool. For questions or issues, contact the repository owner.

## License

Internal use only.

## Author

Created for Eventforce pipeline tracking and analysis.

---

**Last Updated:** 2026-05-26
