# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 to the outside world
EXPOSE 80

# Run FastAPI on startup (you can also run Streamlit separately if needed)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
