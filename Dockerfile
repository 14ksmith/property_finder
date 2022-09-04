# Download the base img. Contains Linux as a base OS, contains Python 3.8
# and all the necessary depenencies.
FROM python:3.8-slim-buster

# Setting the root directory name
WORKDIR /app

# Copy everything from the root project directory into the root directory defined above
# Everything is copied from the root project directory because a .dockerfile ignores `assets/` and `README.md`.
COPY . .
RUN pip3 install -r requirements.txt

# Execute the command to run main.py
# Each argument is passed as a value in the array, you can also pass cli flags and arguments.
CMD [ "python3", "main.py"]