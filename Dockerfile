# Step 1: Use an official Python runtime as a parent image
FROM python:3.9-slim

# Step 2: Set the working directory inside the container
WORKDIR /app

# Step 3: Copy the requirements file to the working directory
COPY requirements.txt /app/

# Step 4: Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the current directory contents into the container at /app
COPY . /app/

# Step 6: Expose the port Django runs on
EXPOSE 8000

# Step 7: Run Django's migrations and start the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
