### Steps
1. git clone <repository_url>
2. cd <repository_directory>
3. docker build -t todos .
4. docker run -d -p 8080:80 --name todos todos
5. docker logs todos

