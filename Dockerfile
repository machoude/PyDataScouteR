FROM rocker/r-ver:4.3.0

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    && rm -rf /var/lib/apt/lists/*

# Install R packages (remotes + DataScouteR dependencies)
RUN R -e "install.packages(c('remotes', 'dplyr', 'magrittr', 'tibble'))"

# Copy entire DataScouteR repo
COPY DataScouteR /tmp/DataScouteR

# Install DataScouteR package
RUN R CMD INSTALL /tmp/DataScouteR

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY api/requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy API code
COPY api/main.py .

# Expose port
EXPOSE 8000

# Run the API
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
