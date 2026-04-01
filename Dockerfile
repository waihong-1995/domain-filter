# Use official Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirement file first (for caching)
COPY requirement.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirement.txt

# Copy rest of the project
COPY . .

# Expose port (Gradio default is 7860)
EXPOSE 7860

# Run your app
CMD ["python", "webapp.py"]