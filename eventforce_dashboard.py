import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Eventforce Pipeline Dashboard",
    page_icon="🎯",
    layout="wide",
)

st.title("🎯 Eventforce Pipeline Dashboard")
st.caption(f"Last updated: {date.today().strftime('%B %d, %Y')}")
st.divider()

# ── Load CSV data ─────────────────────────────────────────────────────────────
csv_path = "/Users/jritchie/Downloads/report1779828207111.csv"

try:
    df = pd.read_csv(csv_path)

    # Clean up column names
    df.columns = df.columns.str.strip()

    # Convert numeric columns, handling empty strings and blanks
    numeric_cols = [
        'Events Touched Open Pipe (ETOP)',
        'Total Event Budget',
        'Total Medical Costs',
        'Security Budget',
        'Total Actual Attendance'
    ]

    for col in numeric_cols:
        if col in df.columns:
            # Replace empty strings with NaN, then convert to numeric
            df[col] = df[col].replace('', np.nan)
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

    # Use ETOP as the main pipeline metric
    df['ETOPP Total'] = df['Events Touched Open Pipe (ETOP)']

    # Count events with data
    events_with_etop = len(df[df['ETOPP Total'] > 0])
    events_with_attendance = len(df[df['Total Actual Attendance'] > 0])

    st.success(f"✅ Loaded {len(df)} events | {events_with_etop} with ETOP | {events_with_attendance} with attendance data")

except FileNotFoundError:
    st.error(f"❌ CSV file not found at: {csv_path}")
    st.stop()
except Exception as e:
    st.error(f"❌ Error loading CSV: {str(e)}")
    st.stop()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.header("Filters")

# Event type filter - use Event Category if available, otherwise derive from name
if 'Event Category' in df.columns:
    df['Event Type'] = df['Event Category'].fillna('Unknown')
else:
    df['Event Type'] = df['Event: Event Name'].apply(lambda x:
        'World Tour' if 'World Tour' in str(x) else
        'Peak Performers' if 'Peak Performers' in str(x) else
        'Dreamforce' if 'Dreamforce' in str(x) else
        'TDX' if 'TDX' in str(x) or 'TrailblazerDX' in str(x) else
        'Summit/Conference' if any(kw in str(x) for kw in ['Summit', 'Conference', 'Connect']) else
        'Other'
    )

# Use the correct event name column
event_name_col = 'Event: Event Name' if 'Event: Event Name' in df.columns else 'Event Name'
df['Event Name'] = df[event_name_col]

event_types = st.sidebar.multiselect(
    "Event Type",
    options=sorted(df['Event Type'].unique()),
    default=sorted(df['Event Type'].unique()),
)

min_pipeline = st.sidebar.number_input(
    "Minimum ETOPP Total ($)",
    min_value=0,
    value=0,
    step=1000000,
    format="%d",
)

# Apply filters
df_filtered = df[
    (df['Event Type'].isin(event_types)) &
    (df['ETOPP Total'] >= min_pipeline)
].copy()

# ── KPI cards ─────────────────────────────────────────────────────────────────
total_events = len(df_filtered)
total_etop = df_filtered['ETOPP Total'].sum()
total_budget = df_filtered['Total Event Budget'].sum() if 'Total Event Budget' in df_filtered.columns else 0
total_attendance = int(df_filtered['Total Actual Attendance'].sum()) if 'Total Actual Attendance' in df_filtered.columns else 0
avg_etop = total_etop / total_events if total_events > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🎪 Total Events", f"{total_events:,}")
with col2:
    events_with_etop_filtered = len(df_filtered[df_filtered['ETOPP Total'] > 0])
    st.metric("💰 Events w/ ETOP", f"{events_with_etop_filtered:,}", delta=f"${total_etop:,.0f}")
with col3:
    events_with_attendance_filtered = len(df_filtered[df_filtered['Total Actual Attendance'] > 0])
    st.metric("👥 Events w/ Attendance", f"{events_with_attendance_filtered:,}", delta=f"{total_attendance:,} total")
with col4:
    avg_attendance = int(total_attendance / events_with_attendance_filtered) if events_with_attendance_filtered > 0 else 0
    st.metric("📊 Avg Attendance", f"{avg_attendance:,}")
with col5:
    avg_etop_per_attendee = int(total_etop / total_attendance) if total_attendance > 0 else 0
    st.metric("💵 Avg ETOP/Attendee", f"${avg_etop_per_attendee:,}")

st.divider()

# ── Attendance vs ETOP Analysis ──────────────────────────────────────────────
st.subheader("📊 Attendance & ETOP Analysis")

# Calculate ETOP per attendee
df_filtered['ETOP per Attendee'] = df_filtered.apply(
    lambda row: row['ETOPP Total'] / row['Total Actual Attendance'] if row['Total Actual Attendance'] > 0 else 0,
    axis=1
)

col_scatter, col_efficiency = st.columns([2, 1])

with col_scatter:
    st.write("**Attendance vs ETOP Correlation**")
    # Filter to events with both attendance and ETOP
    scatter_data = df_filtered[(df_filtered['Total Actual Attendance'] > 0) & (df_filtered['ETOPP Total'] > 0)].copy()

    if not scatter_data.empty:
        fig_scatter = px.scatter(
            scatter_data,
            x='Total Actual Attendance',
            y='ETOPP Total',
            hover_data=['Event Name'],
            labels={'Total Actual Attendance': 'Attendance', 'ETOPP Total': 'ETOP ($)'},
            color='ETOP per Attendee',
            color_continuous_scale='Viridis',
            size='ETOPP Total',
            size_max=30,
        )
        fig_scatter.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=350,
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.info("No events with both attendance and ETOP data.")

with col_efficiency:
    st.write("**Top 5 by ETOP/Attendee**")
    efficiency_data = df_filtered[df_filtered['ETOP per Attendee'] > 0].nlargest(5, 'ETOP per Attendee')[['Event Name', 'ETOP per Attendee']].copy()

    if not efficiency_data.empty:
        for idx, row in efficiency_data.iterrows():
            st.metric(
                label=row['Event Name'][:25] + "..." if len(row['Event Name']) > 25 else row['Event Name'],
                value=f"${row['ETOP per Attendee']:,.0f}",
                delta="per person"
            )
    else:
        st.info("No efficiency data available.")

st.divider()

# ── Top Events by Attendance and ETOP ─────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Top 10 Events by Attendance")
    top_attendance = df_filtered[df_filtered['Total Actual Attendance'] > 0].nlargest(10, 'Total Actual Attendance')[['Event Name', 'Total Actual Attendance', 'ETOPP Total']].copy()

    if not top_attendance.empty:
        fig_attendance = px.bar(
            top_attendance,
            y='Event Name',
            x='Total Actual Attendance',
            orientation='h',
            labels={'Total Actual Attendance': 'Attendees', 'Event Name': ''},
            color='Total Actual Attendance',
            color_continuous_scale='Greens',
            hover_data={'ETOPP Total': ':$,.0f'}
        )
        fig_attendance.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=400,
            showlegend=False,
        )
        fig_attendance.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_attendance, use_container_width=True)
    else:
        st.info("No events with attendance data.")

with col_right:
    st.subheader("Top 10 Events by ETOP")
    top_events = df_filtered[df_filtered['ETOPP Total'] > 0].nlargest(10, 'ETOPP Total')[['Event Name', 'ETOPP Total', 'Total Actual Attendance']].copy()

    if not top_events.empty:
        fig_top = px.bar(
            top_events,
            y='Event Name',
            x='ETOPP Total',
            orientation='h',
            labels={'ETOPP Total': 'ETOP ($)', 'Event Name': ''},
            color='ETOPP Total',
            color_continuous_scale='Blues',
            hover_data={'Total Actual Attendance': ':,'}
        )
        fig_top.update_layout(
            margin=dict(t=10, b=10, l=10, r=10),
            height=400,
            showlegend=False,
        )
        fig_top.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_top, use_container_width=True)
    else:
        st.info("No events with ETOP data.")

# ── Data Quality: Missing Attendance ──────────────────────────────────────────
st.divider()
st.subheader("⚠️ Data Quality Check")

col_dq1, col_dq2 = st.columns(2)

with col_dq1:
    st.write("**Events Missing Attendance Data**")
    missing_attendance = df_filtered[
        (df_filtered['Total Actual Attendance'] == 0) &
        (df_filtered['Event Status'].isin(['Complete', 'Assigned']))
    ][['Event Name', 'ETOPP Total', 'Event Status', 'Event Start Date']].copy()

    if not missing_attendance.empty:
        st.warning(f"⚠️ {len(missing_attendance)} events are Complete/Assigned but have no attendance data")

        # Show top events by ETOP that are missing attendance
        missing_with_etop = missing_attendance[missing_attendance['ETOPP Total'] > 0].nlargest(10, 'ETOPP Total')
        if not missing_with_etop.empty:
            st.write("**High-value events missing attendance:**")
            for idx, row in missing_with_etop.iterrows():
                st.write(f"- {row['Event Name']} (${row['ETOPP Total']:,.0f} ETOP) - {row['Event Status']}")
    else:
        st.success("✅ All Complete/Assigned events have attendance data!")

with col_dq2:
    st.write("**Events with Attendance > 0**")
    events_with_att = df_filtered[df_filtered['Total Actual Attendance'] > 0].copy()

    if not events_with_att.empty:
        st.success(f"✅ {len(events_with_att)} events have attendance data")

        # Show breakdown by status
        if 'Event Status' in events_with_att.columns:
            att_by_status = events_with_att.groupby('Event Status').agg({
                'Event Name': 'count',
                'Total Actual Attendance': 'sum'
            }).reset_index()
            att_by_status.columns = ['Status', 'Event Count', 'Total Attendance']
            st.dataframe(att_by_status, use_container_width=True, hide_index=True)

st.divider()

# ── Event Status & Lead Breakdown ────────────────────────────────────────────
st.subheader("Event Overview")

col_a, col_b = st.columns(2)

with col_a:
    if 'Event Status' in df_filtered.columns:
        st.write("**Events by Status**")
        status_counts = df_filtered['Event Status'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']

        fig_status = px.bar(
            status_counts,
            x='Status',
            y='Count',
            color='Status',
            labels={'Count': 'Number of Events', 'Status': ''},
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
        fig_status.update_layout(
            margin=dict(t=10, b=10),
            height=300,
            showlegend=False,
        )
        st.plotly_chart(fig_status, use_container_width=True)

with col_b:
    if 'Event Lead' in df_filtered.columns:
        st.write("**Top Event Leads by ETOP**")
        lead_summary = df_filtered.groupby('Event Lead')['ETOPP Total'].sum().reset_index()
        lead_summary = lead_summary.sort_values('ETOPP Total', ascending=False).head(8)

        fig_leads = px.bar(
            lead_summary,
            y='Event Lead',
            x='ETOPP Total',
            orientation='h',
            labels={'ETOPP Total': 'Total ETOP ($)', 'Event Lead': ''},
            color='ETOPP Total',
            color_continuous_scale='Teal',
        )
        fig_leads.update_layout(
            margin=dict(t=10, b=10),
            height=300,
            showlegend=False,
        )
        fig_leads.update_yaxes(autorange="reversed")
        st.plotly_chart(fig_leads, use_container_width=True)

# ── Detailed Event Table ──────────────────────────────────────────────────────
st.divider()
st.subheader("📋 Detailed Event Data")

# Add tabs for different views
tab1, tab2, tab3 = st.tabs(["All Events", "With Attendance", "Missing Attendance"])

with tab1:
    # Prepare display dataframe with available columns
    display_cols = ['Event Name', 'Total Actual Attendance', 'ETOPP Total']
    if 'Event Status' in df_filtered.columns:
        display_cols.append('Event Status')
    if 'Event Lead' in df_filtered.columns:
        display_cols.append('Event Lead')
    if 'Event Start Date' in df_filtered.columns:
        display_cols.append('Event Start Date')
    if 'Total Event Budget' in df_filtered.columns:
        display_cols.append('Total Event Budget')

    display_df = df_filtered[display_cols].copy()
    display_df = display_df.sort_values('ETOPP Total', ascending=False)

    # Format as currency
    for col in ['ETOPP Total', 'Total Event Budget']:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}" if x > 0 else "-")

    # Format attendance
    if 'Total Actual Attendance' in display_df.columns:
        display_df['Total Actual Attendance'] = display_df['Total Actual Attendance'].apply(lambda x: f"{int(x):,}" if x > 0 else "⚠️ BLANK")

    st.dataframe(
        display_df,
        use_container_width=True,
        height=400,
        hide_index=True,
    )

with tab2:
    st.write("**Events with attendance data**")
    att_df = df_filtered[df_filtered['Total Actual Attendance'] > 0][display_cols].copy()
    att_df = att_df.sort_values('Total Actual Attendance', ascending=False)

    # Format columns
    for col in ['ETOPP Total', 'Total Event Budget']:
        if col in att_df.columns:
            att_df[col] = att_df[col].apply(lambda x: f"${x:,.0f}" if x > 0 else "-")
    if 'Total Actual Attendance' in att_df.columns:
        att_df['Total Actual Attendance'] = att_df['Total Actual Attendance'].apply(lambda x: f"{int(x):,}")

    st.dataframe(att_df, use_container_width=True, height=400, hide_index=True)

with tab3:
    st.write("**Events missing attendance data (Complete or Assigned status)**")
    missing_df = df_filtered[
        (df_filtered['Total Actual Attendance'] == 0) &
        (df_filtered['Event Status'].isin(['Complete', 'Assigned']))
    ][display_cols].copy()
    missing_df = missing_df.sort_values('ETOPP Total', ascending=False)

    # Format columns
    for col in ['ETOPP Total', 'Total Event Budget']:
        if col in missing_df.columns:
            missing_df[col] = missing_df[col].apply(lambda x: f"${x:,.0f}" if x > 0 else "-")
    if 'Total Actual Attendance' in missing_df.columns:
        missing_df['Total Actual Attendance'] = "⚠️ MISSING"

    if not missing_df.empty:
        st.warning(f"⚠️ {len(missing_df)} events need attendance data")
        st.dataframe(missing_df, use_container_width=True, height=400, hide_index=True)
    else:
        st.success("✅ No missing attendance data!")

# ── Export option ─────────────────────────────────────────────────────────────
st.divider()
col_export1, col_export2 = st.columns([3, 1])
with col_export2:
    csv_export = df_filtered.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data",
        data=csv_export,
        file_name=f"eventforce_filtered_{date.today().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )
