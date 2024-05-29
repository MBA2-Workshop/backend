import subprocess
import os

# ========================
# Create the superuser
# ========================

print("Creating superuser...")

# Create superuser if it doesn't exist
create_superuser_command = (
    "from django.contrib.auth import get_user_model; "
    "User = get_user_model(); "
    "User.objects.create_superuser(os.environ['DJANGO_SUPERUSER_USERNAME'], "
    "os.environ['DJANGO_SUPERUSER_EMAIL'], os.environ['DJANGO_SUPERUSER_PASSWORD']) "
    "if not User.objects.filter(username=os.environ['DJANGO_SUPERUSER_USERNAME']).exists() "
    "else None"
)

# Run the command to create the superuser
subprocess.run(
    ["python", "manage.py", "shell", "-c", create_superuser_command],
    check=True,
    env=os.environ,
)
