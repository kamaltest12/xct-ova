#!/bin/bash
jsonArgs=""
if [ -f /opt/jboss/tools/ovasso.json  ] || [ -f /opt/jboss/tools/xctsso.json ]; then
  jsonArgs="-Dkeycloak.import="
  if [ -f /opt/jboss/tools/ovasso.json ]; then
    jsonArgs+="/opt/jboss/tools/ovasso.json,"
  fi

  if [ -f /opt/jboss/tools/xctsso.json ]; then
    jsonArgs+="/opt/jboss/tools/xctsso.json,"
  fi

  if [[ "$jsonArgs" == *, ]]; then
    jsonArgs=${jsonArgs%?}
  fi
fi


/opt/jboss/tools/docker-entrypoint.sh --server-config=standalone.xml -Djboss.socket.binding.port-offset=100 -Dkeycloak.profile.feature.token_exchange=enabled -b 0.0.0.0 -Dkeycloak.profile.feature.upload_scripts=enabled "$jsonArgs" &
export PATH=$PATH:/opt/jboss/keycloak/bin

if [ -n "$jsonArgs" ] && [ ! -f /opt/jboss/keycloak/standalone/provisioned ]; then
  touch /opt/jboss/keycloak/standalone/provisioned
elif [ ! -f /opt/jboss/keycloak/standalone/provisioned ]; then
  # Login to Keycloak
  echo "Trying to log in..."
  until kcadm.sh config credentials --server http://localhost:8180/auth --realm master --user admin --password password; do
    echo "Login failed, will retry..."
    sleep 1;
  done
  echo "Login succeeded"

  echo "$(date) - Starting provisioning..."
  /tmp/keycloakConfig.sh
  echo "$(date) - Done provisioning"
  touch /opt/jboss/keycloak/standalone/provisioned

else
  echo "Already provisioned"
fi

wait