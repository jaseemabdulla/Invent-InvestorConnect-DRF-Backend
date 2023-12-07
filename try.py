from datetime import datetime

# Assuming 'current_period_start' and 'current_period_end' are the provided timestamps
current_period_start_timestamp = 1701790269
current_period_end_timestamp = 1704468669

# Convert timestamps to datetime objects
current_period_start_datetime = datetime.utcfromtimestamp(current_period_start_timestamp)
current_period_end_datetime = datetime.utcfromtimestamp(current_period_end_timestamp)

print("Current Period Start:", current_period_start_datetime)
print("Current Period End:", current_period_end_datetime)

# Print the formatted dates
print("Current Period Start:", current_period_start_datetime.strftime('%Y-%m-%d %H:%M:%S UTC'))
print("Current Period End:", current_period_end_datetime.strftime('%Y-%m-%d %H:%M:%S UTC'))