# Eventforce Dashboard - Updated 2026-05-26

## ✅ What's New

### 1. **Enhanced KPI Cards**
- Now shows 5 key metrics:
  - Total Events
  - Events with ETOP (count + total $)
  - Events with Attendance (count + total attendees)
  - Average Attendance per event
  - Average ETOP per Attendee

### 2. **Attendance Focus**
- **Attendance vs ETOP scatter plot** - visualizes correlation
- **Top events by Attendance** - separate ranking
- **Top events by ETOP** - side-by-side comparison
- **ETOP per Attendee efficiency** - shows which events generate most pipeline per person

### 3. **Data Quality Checks** ⚠️
New section highlights:
- Events missing attendance data (Complete/Assigned status only)
- High-value ETOP events that need attendance data
- Breakdown of events WITH attendance by status

### 4. **Tabbed Event Table**
Three views:
- **All Events** - shows everything, marks blank attendance with "⚠️ BLANK"
- **With Attendance** - only events that have attendance data
- **Missing Attendance** - flags Complete/Assigned events needing data entry

---

## 📊 Current Data Summary

### Events with Attendance (19 total):
1. World Tour Sydney - 10,564 attendees ($212M ETOP)
2. World Tour NYC - 7,676 attendees ($220M ETOP)
3. **World Tour Paris - 7,023 attendees ($235M ETOP)** ✅
4. Tableau Conference - 6,734 attendees ($615.7M ETOP)
5. TDX26 - 6,200 attendees ($399.2M ETOP)
6. CKO FY27 - 4,999 attendees ($0 ETOP)
7. World Tour DC - 4,917 attendees ($43.8M ETOP)
8. World Tour Frankfurt - 4,000 attendees ($207M ETOP)
9. World Tour Toronto - 4,000 attendees ($172M ETOP)
10. World Tour Amsterdam - 3,173 attendees ($81.4M ETOP)
... and 9 more

### High-Value Events Missing Attendance:
- World Tour Brussels - $56.3M ETOP, NO attendance
- World Tour Sao Paulo - $130M ETOP, NO attendance
- Plus 37 other events with blank attendance

---

## 🚀 To Run

```bash
streamlit run /Users/jritchie/.aisuite/notebook/2026-04-28/eventforce_dashboard.py
```

---

## 🎯 Key Features

### Filters (Sidebar)
- Event Type (World Tour, Dreamforce, TDX, etc.)
- Minimum ETOP threshold

### Visualizations
1. **KPI Cards** - 5 key metrics at a glance
2. **Attendance vs ETOP Scatter** - bubble chart with hover details
3. **Top 5 ETOP/Attendee** - efficiency metrics
4. **Top 10 by Attendance** - horizontal bar chart
5. **Top 10 by ETOP** - horizontal bar chart
6. **Events by Status** - bar chart (Complete, Assigned, New, Canceled)
7. **Event Leads by ETOP** - top performers
8. **Data Quality Alerts** - missing attendance warnings
9. **Tabbed Detail Table** - sortable, filterable event data

### Export
- Download filtered data as CSV

---

## ✅ Verified Data Points

**World Tour Paris (1) FY27:**
- ✅ Attendance: 7,023
- ✅ ETOP: $235,000,000
- ✅ Status: Complete
- ✅ Date: May 21, 2026
- ✅ Lead: Philip Drinkwater

All data sourced from: `/Users/jritchie/Downloads/report1779828207111.csv`
