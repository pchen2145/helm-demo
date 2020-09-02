FROM gradle:5.4-jdk11 AS builder
WORKDIR /person-service
COPY . /person-service/
RUN gradle build

FROM openjdk:11.0-jdk
WORKDIR /person-service
COPY --from=builder /person-service/build/libs/person-service-0.0.1-SNAPSHOT.jar .
ENTRYPOINT ["java","-jar","/person-service/person-service-0.0.1-SNAPSHOT.jar"] 
EXPOSE 8080
