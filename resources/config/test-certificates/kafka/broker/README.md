base64 -w 0 kafka.server.truststore.jks
base64 -w 0 kafka.server.keystore.jks

will give Base64 encoded string that has to go into setup/kubernetes/src/helm-charts/test/ci/opf-ci-umbrella/values.yaml

