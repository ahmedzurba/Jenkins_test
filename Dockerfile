# stage 1 build
FROM maven:3.9.0-eclipse-temurin-8 AS build
WORKDIR /app
COPY pom.xml .

RUN mvn dependency:go-offline
RUN apt update && apt install mysql-server -y
RUN service mysql start && mysql -e \
"CREATE USER 'detector-user' IDENTIFIED BY 'detector-pass';\
GRANT ALL PRIVILEGES ON *.* TO 'detector-user' WITH GRANT OPTION;\
FLUSH PRIVILEGES;CREATE DATABASE detector;"

ENV MYSQL_HOST=$HOSTNAME

COPY . .
RUN mvn package -DskipTests=true


# stage 2
FROM openjdk:8-jre-alpine
WORKDIR /app
COPY --from=build app/target/suspicious-events-detector-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]