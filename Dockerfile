# Base Python image
FROM python:3.11

# Working directory set karein
WORKDIR /app

# Requirements copy aur install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baaki project files copy karein
COPY . .

# Chainlit port 7860 pe run hota hai
EXPOSE 7860

# Chainlit command run karein
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "7860"]