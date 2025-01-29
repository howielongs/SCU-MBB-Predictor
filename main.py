from src.data_loader import fetch_athletes, fetch_activities

# Fetch athlete data
try:
    athletes_df = fetch_athletes()
    print("Athletes DataFrame:")
    print(athletes_df.head())
except Exception as e:
    print(f"Error fetching athletes: {e}")

# Fetch activity data
try:
    activities_df = fetch_activities()
    print("Activities DataFrame:")
    print(activities_df.head())
except Exception as e:
    print(f"Error fetching activities: {e}")

# Merge logic (if applicable)
try:
    # Example: If activities include `activity_athletes` linking to `athlete id`
    merged_df = activities_df.explode("activity_athletes")  # Expand list of athletes
    merged_df = merged_df.merge(athletes_df, left_on="activity_athletes", right_on="id", how="left")
    
    print("Merged DataFrame (Activities with Athlete Details):")
    print(merged_df.head())
except Exception as e:
    print(f"Error merging data: {e}")
