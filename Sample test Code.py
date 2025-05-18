import psutil

print("CPU usage:", psutil.cpu_percent(interval=1), "%")
print("Memory usage:", psutil.virtual_memory().percent, "%")
print("Disk usage:", psutil.disk_usage('/').percent, "%")
