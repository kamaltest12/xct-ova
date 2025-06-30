# Script used to generate the truststore and keystore for the broker and client.
# see https://docs.confluent.io/current/tutorials/security_tutorial.html#creating-ssl-keys-and-certificates
#!/bin/bash
PASSWORD=password
VALIDITY=999999
BROKER_NAME=kafka
CLIENT_NAME=kafkaclient
ALGO=RSA

PATH_BASE=../../setup/docker/jks/kafka/
rm -fr $PATH_BASE/broker
rm -fr $PATH_BASE/client
mkdir $PATH_BASE/broker
mkdir $PATH_BASE/client

# Create the Certificate Authority (CA)
openssl req -new -x509 -keyout ca-key -out ca-cert -days $VALIDITY -passout pass:$PASSWORD -subj "/CN=$BROKER_NAME"
keytool -keystore $PATH_BASE/broker/kafka.server.truststore.jks -storepass $PASSWORD -alias CARoot -import -file ca-cert -noprompt
keytool -keystore $PATH_BASE/client/kafka.client.truststore.jks -storepass $PASSWORD -alias CARoot -import -file ca-cert -noprompt

# Generate the keys and certificates - BROKER
keytool -keystore $PATH_BASE/broker/kafka.server.keystore.jks -storepass $PASSWORD -alias localhost -validity $VALIDITY -genkey  -keyalg $ALGO -keypass $PASSWORD -dname "CN=$BROKER_NAME" -ext SAN=DNS:$BROKER_NAME

# Sign the certificate - BROKER
keytool -keystore $PATH_BASE/broker/kafka.server.keystore.jks -storepass $PASSWORD -alias localhost -certreq -file cert-file
openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file -out cert-signed -days $VALIDITY -CAcreateserial -passin pass:$PASSWORD
rm cert-file ca-cert.srl
keytool -keystore $PATH_BASE/broker/kafka.server.keystore.jks -storepass $PASSWORD -alias CARoot -import -file ca-cert -noprompt
keytool -keystore $PATH_BASE/broker/kafka.server.keystore.jks -storepass $PASSWORD -alias localhost -import -file cert-signed -noprompt
rm cert-signed

# Generate the keys and certificates - CLIENT
keytool -keystore $PATH_BASE/client/kafka.client.keystore.jks -storepass $PASSWORD -alias localhost -validity $VALIDITY -genkey -keyalg $ALGO -keypass $PASSWORD -dname "CN=$CLIENT_NAME" -ext SAN=DNS:$CLIENT_NAME

# Sign the certificate - CLIENT
keytool -keystore $PATH_BASE/client/kafka.client.keystore.jks -storepass $PASSWORD -alias localhost -certreq -file cert-file
openssl x509 -req -CA ca-cert -CAkey ca-key -in cert-file -out cert-signed -days $VALIDITY -CAcreateserial -passin pass:$PASSWORD
rm cert-file ca-cert.srl
keytool -keystore $PATH_BASE/client/kafka.client.keystore.jks -storepass $PASSWORD -alias CARoot -import -file ca-cert  -noprompt
keytool -keystore $PATH_BASE/client/kafka.client.keystore.jks -storepass $PASSWORD -alias localhost -import -file cert-signed -noprompt
rm cert-signed
rm ca-cert ca-key
