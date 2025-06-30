In order to run normal provisioning comment out following json's:
      - ../../../../config/keycloak/ovasso.json:/opt/jboss/tools/ovasso.json:ro
      - ../../../../config/keycloak/xctsso.json:/opt/jboss/tools/xctsso.json:ro

and to generate realms run within container:
/opt/jboss/keycloak/bin/standalone.sh -Djboss.socket.binding.port-offset=200 -Dkeycloak.migration.action=export -Dkeycloak.migration.provider=singleFile -Dkeycloak.migration.usersExportStrategy=REALM_FILE -Dkeycloak.migration.file=/tmp/sso.json


in the end copy then specific realms from generated jsons into ovasso.json and xctsso.json