FROM python:3.9-slim
RUN pip install flask requests
WORKDIR /app
COPY vuln_web.py .
CMD ["python", "vuln_web.py"]
