claimScript=\
'var claimVal = {\"version\": \"1.0\"};\n'\
'var grpVal = user.getAttribute(\"bank-groud-id\")[0];\n'\
'if(grpVal){\n'\
'   claimVal[\"bank-group-id\"] = grpVal;\n'\
'}\n'\
'claimVal[\"bank-users\"] = [];\n'\
'for(var i=1; i<10; i++){\n'\
'   var bankUser = {};\n'\
'   var value1 = user.getAttribute(\"user-name-\"+i)[0];\n'\
'   var userIdVal = undefined;\n'\
'   if(value1){\n'\
'      userIdVal = value1;\n'\
'      bankUser[\"user-name\"] = value1;\n'\
'   }\n'\
'   value1 = user.getAttribute(\"bank-name-\"+i)[0];\n'\
'   if(value1){\n'\
'      userIdVal = userIdVal+\"@\"+value1;\n'\
'      bankUser[\"bank-name\"] = value1;\n'\
'   }\n'\
'   value1 = user.getAttribute(\"banking-entity-name-\"+i)[0];\n'\
'   if(value1){\n'\
'      userIdVal = userIdVal+\"#\"+value1;\n'\
'      bankUser[\"banking-entity-name\"] = value1;\n'\
'   }\n'\
'   if(userIdVal){\n'\
'      bankUser[\"user-id\"] = userIdVal;\n'\
'   }\n'\
'   \n'\
'   if (Object.keys(bankUser).length > 0) {\n'\
'       claimVal[\"bank-users\"].push(bankUser);\n'\
'       bankUser.roles = [];\n'\
'       for(var j=1; j<10; j++){\n'\
'          var value2 = user.getAttribute(\"roles-\"+i+\"-role-name-\"+j)[0];\n'\
'          if(value2){\n'\
'             var role = {\"role-name\": value2};\n'\
'             bankUser.roles.push(role);\n'\
'             \n'\
'             value2 = user.getAttribute(\"roles-\"+i+\"-bank-name-\"+j)[0];\n'\
'             if(value2){\n'\
'                role[\"bank-name\"] = value2;\n'\
'             }\n'\
'             \n'\
'             value2 = user.getAttribute(\"roles-\"+i+\"-bank-entity-name-\"+j)[0];\n'\
'             if(value2){\n'\
'                role[\"bank-entity-name\"] = value2;\n'\
'             }\n'\
'          }\n'\
'       }\n'\
'   }\n'\
'}\n'\
'token.getOtherClaims().put(\"opf-identity\", JSON.stringify(claimVal));'

echo "creating opfsso realm"
kcadm.sh create realms -s realm=xctsso -s enabled=true -o
echo ""

echo "creating opfrest client"
kcadm.sh create clients -r xctsso -s clientId=opfrest -s enabled=true -s id=1908a444-1f81-4e45-8036-7779abd71162 -s clientAuthenticatorType=client-secret -s secret=07720bc0-d1b0-44aa-93da-9ac9cb85a6b4
kcadm.sh update clients/1908a444-1f81-4e45-8036-7779abd71162 -r xctsso -s redirectUris='["*"]' -s rootUrl=https://dockerhost:9443/opfrest -s webOrigins='["https://dockerhost:9443", "https://dockerhost:30443"]'
# adding custom claim 'opf-identity'
kcadm.sh create clients/1908a444-1f81-4e45-8036-7779abd71162/protocol-mappers/models -r xctsso -s name=opf-identity -s protocol=openid-connect -s protocolMapper=oidc-script-based-protocol-mapper -s consentRequired=false -s config='{"jsonType.label":"String","claim.name":"opf-identity","access.token.claim":"true","userinfo.token.claim":"false","id.token.claim":"false","script":"'"$claimScript"'"}'

echo "disabling full scope allowed on opfrest client"
kcadm.sh update clients/1908a444-1f81-4e45-8036-7779abd71162 -r xctsso -s fullScopeAllowed=false
echo "enabling service account on opfrest client"
kcadm.sh update clients/1908a444-1f81-4e45-8036-7779abd71162 -r xctsso -s serviceAccountsEnabled=true
kcadm.sh update clients/1908a444-1f81-4e45-8036-7779abd71162 -r xctsso -s directAccessGrantsEnabled=true

# adding custom claim 'groupIds' opfrest client --> required for permission mappings in CBIS
kcadm.sh create clients/1908a444-1f81-4e45-8036-7779abd71162/protocol-mappers/models -r xctsso -s name=groupIds -s protocol=openid-connect -s protocolMapper=oidc-usermodel-client-role-mapper -s consentRequired=false -s config='{"jsonType.label":"String","claim.name":"groupIds","multivalued":"true","usermodel.clientRoleMapping.clientId":"cbisrest","access.token.claim":"true","userinfo.token.claim":"false","id.token.claim":"true"}'


echo "creating OVA client"
kcadm.sh create clients -r xctsso -s clientId=ova -s enabled=true -s id=1908a444-1f81-4e45-8036-7779abd71163 -s clientAuthenticatorType=client-secret -s secret=b1048aae-f242-4ed8-bec2-2c6b12053c75
kcadm.sh update clients/1908a444-1f81-4e45-8036-7779abd71163 -r xctsso -s redirectUris='["*"]' -s rootUrl=https://dockerhost:9445/ova -s webOrigins='["https://dockerhost:9445", "https://dockerhost:30445"]'
# adding custom claim 'opf-identity'
kcadm.sh create clients/1908a444-1f81-4e45-8036-7779abd71163/protocol-mappers/models -r xctsso -s name=opf-identity -s protocol=openid-connect -s protocolMapper=oidc-script-based-protocol-mapper -s consentRequired=false -s config='{"jsonType.label":"String","claim.name":"opf-identity","access.token.claim":"true","userinfo.token.claim":"false","id.token.claim":"false","script":"'"$claimScript"'"}'
# adding audience 'opfrest' on ova client (required for propagate token scenario)
kcadm.sh create clients/1908a444-1f81-4e45-8036-7779abd71163/protocol-mappers/models -r xctsso -s name=opfrest-audience -s protocol=openid-connect -s protocolMapper=oidc-audience-mapper -s consentRequired=false -s config='{"included.client.audience": "opfrest","id.token.claim": "false","access.token.claim": "true"}'
# disabling full scope allowed on ova client
kcadm.sh update clients/1908a444-1f81-4e45-8036-7779abd71163 -r xctsso -s fullScopeAllowed=false

echo "granting OVA client the right to exchange its token for a token tailored for opfrest (required for exchange token scenario)"
# Update opfrest client --> enable permissions
kcadm.sh update clients/1908a444-1f81-4e45-8036-7779abd71162/management/permissions -r xctsso -s enabled=true
# retrieve real-management client id
rmid=`kcadm.sh get clients -r xctsso --fields id,clientId | grep -B 1 "realm-management"|head -1|sed 's/.*"\(.*\)".*/\1/'| tr -d '\n'`
# create a new policy
kcadm.sh create clients/${rmid}/authz/resource-server/policy/client -r xctsso -s name=opfrest-client-exchange -s 'clients=["1908a444-1f81-4e45-8036-7779abd71163"]'
# retrieve the token exchange permission for opfrest client
permissionId=`kcadm.sh get clients/${rmid}/authz/resource-server/permission -r xctsso --fields id,name | grep -B 1 "token-exchange.permission.client.1908a444-1f81-4e45-8036-7779abd71162"|head -1|sed 's/.*"\(.*\)".*/\1/'| tr -d '\n'`
# Update the permission to add the previously created policy
echo "Adding policy 'opfrest-client-exchange' to permssion with $permissionId"
sleep 5
kcadm.sh update clients/${rmid}/authz/resource-server/permission/${permissionId} -r xctsso -s 'policies=["opfrest-client-exchange"]'
sleep 5


echo "creating cbisrest client"
kcadm.sh create clients -r xctsso -s clientId=cbisrest -s enabled=true -s id=1908a444-1f81-4e45-8036-7779abd71164 -s clientAuthenticatorType=client-secret -s secret=664290b7-28f8-4fed-98e3-bcb72e7b5328
kcadm.sh update clients/1908a444-1f81-4e45-8036-7779abd71164 -r xctsso -s redirectUris='["https://dockerhost:5443/oidcclient/redirect/cbisrest/*"]' -s rootUrl=https://dockerhost:5443/cbis -s webOrigins='["https://dockerhost:9443", "https://dockerhost:30443"]'
echo "disabling full scope allowed on cbisrest client"
kcadm.sh update clients/1908a444-1f81-4e45-8036-7779abd71164 -r xctsso -s fullScopeAllowed=false
echo "creating cbis roles on cbisrest client"
kcadm.sh create clients/1908a444-1f81-4e45-8036-7779abd71164/roles -r xctsso -s name=CBISAccountsUser
kcadm.sh create clients/1908a444-1f81-4e45-8036-7779abd71164/roles -r xctsso -s name=CBISPostingUser
kcadm.sh create clients/1908a444-1f81-4e45-8036-7779abd71164/roles -r xctsso -s name=CBISCalendarUser
kcadm.sh create clients/1908a444-1f81-4e45-8036-7779abd71164/roles -r xctsso -s name=CBISSearchUser
kcadm.sh create clients/1908a444-1f81-4e45-8036-7779abd71164/roles -r xctsso -s name=CBISOperationsUser

echo "adding cbis service account roles on opfRest"
# service-account-opfrest is the default name for the service-account opfrest.
kcadm.sh add-roles -r xctsso --uusername service-account-opfrest --cclientid cbisrest --rolename CBISAccountsUser
kcadm.sh add-roles -r xctsso --uusername service-account-opfrest --cclientid cbisrest --rolename CBISPostingUser
kcadm.sh add-roles -r xctsso --uusername service-account-opfrest --cclientid cbisrest --rolename CBISCalendarUser
kcadm.sh add-roles -r xctsso --uusername service-account-opfrest --cclientid cbisrest --rolename CBISSearchUser
kcadm.sh add-roles -r xctsso --uusername service-account-opfrest --cclientid cbisrest --rolename CBISOperationsUser
echo "configuring scope mappings on opfrest client"
kcadm.sh create -r xctsso -x "clients/1908a444-1f81-4e45-8036-7779abd71162/scope-mappings/clients/1908a444-1f81-4e45-8036-7779abd71164" --body "[{\"name\": \"CBISAccountsUser\"}]"
kcadm.sh create -r xctsso -x "clients/1908a444-1f81-4e45-8036-7779abd71162/scope-mappings/clients/1908a444-1f81-4e45-8036-7779abd71164" --body "[{\"name\": \"CBISPostingUser\"}]"
kcadm.sh create -r xctsso -x "clients/1908a444-1f81-4e45-8036-7779abd71162/scope-mappings/clients/1908a444-1f81-4e45-8036-7779abd71164" --body "[{\"name\": \"CBISCalendarUser\"}]"
kcadm.sh create -r xctsso -x "clients/1908a444-1f81-4e45-8036-7779abd71162/scope-mappings/clients/1908a444-1f81-4e45-8036-7779abd71164" --body "[{\"name\": \"CBISSearchUser\"}]"
kcadm.sh create -r xctsso -x "clients/1908a444-1f81-4e45-8036-7779abd71162/scope-mappings/clients/1908a444-1f81-4e45-8036-7779abd71164" --body "[{\"name\": \"CBISOperationsUser\"}]"

# Update cbisrest client --> enable permissions
kcadm.sh update clients/1908a444-1f81-4e45-8036-7779abd71164/management/permissions -r xctsso -s enabled=true
# create a new policy
kcadm.sh create clients/${rmid}/authz/resource-server/policy/client -r xctsso -s name=cbisrest-client-exchange -s 'clients=["1908a444-1f81-4e45-8036-7779abd71163"]'

# retrieve the token exchange permission for opfcbisrest client
permissionId=`kcadm.sh get clients/${rmid}/authz/resource-server/permission -r xctsso --fields id,name | grep -B 1 "token-exchange.permission.client.1908a444-1f81-4e45-8036-7779abd71164"|head -1|sed 's/.*"\(.*\)".*/\1/'| tr -d '\n'`
# Update the permission to add the previously created policy
echo "Adding policy 'opfrest-client-exchange' to permssion with $permissionId"
sleep 5
kcadm.sh update clients/${rmid}/authz/resource-server/permission/${permissionId} -r xctsso -s 'policies=["cbisrest-client-exchange"]'
sleep 5
#####################End Creating for CBIS integration########################

echo "creating test-client client"
###### test client #######
kcadm.sh create clients -r xctsso -s clientId=test-client -s enabled=true -s id=1908a444-1f81-4e45-8036-7779abd71165 -s clientAuthenticatorType=client-secret -s secret=8a5300d5-a39a-4cd2-80ab-4ac1be73cb05
kcadm.sh update clients/1908a444-1f81-4e45-8036-7779abd71165 -r xctsso -s directAccessGrantsEnabled=true
kcadm.sh update clients/1908a444-1f81-4e45-8036-7779abd71165 -r xctsso -s standardFlowEnabled=false
# adding custom claim 'opf-identity'
kcadm.sh create clients/1908a444-1f81-4e45-8036-7779abd71165/protocol-mappers/models -r xctsso -s name=opf-identity -s protocol=openid-connect -s protocolMapper=oidc-script-based-protocol-mapper -s consentRequired=false -s config='{"jsonType.label":"String","claim.name":"opf-identity","access.token.claim":"true","userinfo.token.claim":"false","id.token.claim":"false","script":"'"$claimScript"'"}'
# adding audience 'opfrest' on test client
kcadm.sh create clients/1908a444-1f81-4e45-8036-7779abd71165/protocol-mappers/models -r xctsso -s name=opfrest-audience -s protocol=openid-connect -s protocolMapper=oidc-audience-mapper -s consentRequired=false -s config='{"included.client.audience": "opfrest","id.token.claim": "false","access.token.claim": "true"}'
# adding audience 'ova' on test client
kcadm.sh create clients/1908a444-1f81-4e45-8036-7779abd71165/protocol-mappers/models -r xctsso -s name=ova-audience -s protocol=openid-connect -s protocolMapper=oidc-audience-mapper -s consentRequired=false -s config='{"included.client.audience": "ova","id.token.claim": "false","access.token.claim": "true"}'

kcadm.sh update clients/1908a444-1f81-4e45-8036-7779abd71165/management/permissions -r xctsso -s enabled=true
kcadm.sh create clients/${rmid}/authz/resource-server/policy/client -r xctsso -s name=resttest-client-exchange -s 'clients=["1908a444-1f81-4e45-8036-7779abd71163"]'
permissionId=`kcadm.sh get clients/${rmid}/authz/resource-server/permission -r xctsso --fields id,name | grep -B 1 "token-exchange.permission.client.1908a444-1f81-4e45-8036-7779abd71165"|head -1|sed 's/.*"\(.*\)".*/\1/'| tr -d '\n'`
echo "Adding policy 'resttest-client-exchange' to permssion with $permissionId"
sleep 5
kcadm.sh update clients/${rmid}/authz/resource-server/permission/${permissionId} -r xctsso -s 'policies=["resttest-client-exchange"]'
sleep 5

##### User management
echo "creating bva1 user"
kcadm.sh create users -r xctsso -s  username=bva1 -s  enabled=true\
    -s  "attributes.user-name-1=bva1"\
    -s  "attributes.bank-groud-id=OPFBankgroup"\
    -s  "attributes.bank-name-1=UK BANK-2"\
    -s  "attributes.banking-entity-name-1=Admin department"\
    -s  "attributes.roles-1-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-2=bva1"\
    -s  "attributes.bank-name-2=UK BANK-1"\
    -s  "attributes.banking-entity-name-2=Admin department"\
    -s  "attributes.roles-2-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-3=bva1"\
    -s  "attributes.bank-name-3=AU BANK-1"\
    -s  "attributes.banking-entity-name-3=Admin department"\
    -s  "attributes.roles-3-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-4=bva1"\
    -s  "attributes.bank-name-4=XCT BANK-2"\
    -s  "attributes.banking-entity-name-4=Admin department"\
    -s  "attributes.roles-4-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-5=bva1"\
    -s  "attributes.bank-name-5=XCT BANK-1"\
    -s  "attributes.banking-entity-name-5=Admin department"\
    -s  "attributes.roles-5-role-name-1=Group System Administrator"
kcadm.sh set-password -r xctsso --username bva1 --new-password password --temporary=false

echo "creating bva2 user"
# Create user
kcadm.sh create users -r xctsso -s  username=bva2 -s  enabled=true\
    -s  "attributes.user-name-1=bva2"\
    -s  "attributes.bank-groud-id=OPFBankgroup"\
    -s  "attributes.bank-name-1=UK BANK-2"\
    -s  "attributes.banking-entity-name-1=Admin department"\
    -s  "attributes.roles-1-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-2=bva2"\
    -s  "attributes.bank-name-2=UK BANK-1"\
    -s  "attributes.banking-entity-name-2=Admin department"\
    -s  "attributes.roles-2-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-3=bva2"\
    -s  "attributes.bank-name-3=AU BANK-1"\
    -s  "attributes.banking-entity-name-3=Admin department"\
    -s  "attributes.roles-3-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-4=bva2"\
    -s  "attributes.bank-name-4=XCT BANK-2"\
    -s  "attributes.banking-entity-name-4=Admin department"\
    -s  "attributes.roles-4-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-5=bva2"\
    -s  "attributes.bank-name-5=XCT BANK-1"\
    -s  "attributes.banking-entity-name-5=Admin department"\
    -s  "attributes.roles-5-role-name-1=Group System Administrator"
kcadm.sh set-password -r xctsso --username bva2 --new-password password --temporary=false

echo "creating bva3 user"
# Create user
kcadm.sh create users -r xctsso -s  username=bva3 -s  enabled=true\
    -s  "attributes.user-name-1=bva3"\
    -s  "attributes.bank-groud-id=OPFBankgroup"\
    -s  "attributes.bank-name-1=UK BANK-2"\
    -s  "attributes.banking-entity-name-1=Admin department"\
    -s  "attributes.roles-1-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-2=bva3"\
    -s  "attributes.bank-name-2=UK BANK-1"\
    -s  "attributes.banking-entity-name-2=Admin department"\
    -s  "attributes.roles-2-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-3=bva3"\
    -s  "attributes.bank-name-3=AU BANK-1"\
    -s  "attributes.banking-entity-name-3=Admin department"\
    -s  "attributes.roles-3-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-4=bva3"\
    -s  "attributes.bank-name-4=XCT BANK-2"\
    -s  "attributes.banking-entity-name-4=Admin department"\
    -s  "attributes.roles-4-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-5=bva3"\
    -s  "attributes.bank-name-5=XCT BANK-1"\
    -s  "attributes.banking-entity-name-5=Admin department"\
    -s  "attributes.roles-5-role-name-1=Group System Administrator"
kcadm.sh set-password -r xctsso --username bva3 --new-password password --temporary=false

echo "creating bva4 user"
# Create user
kcadm.sh create users -r xctsso -s  username=bva4 -s  enabled=true\
    -s  "attributes.user-name-1=bva4"\
    -s  "attributes.bank-groud-id=OPFBankgroup"\
    -s  "attributes.bank-name-1=UK BANK-2"\
    -s  "attributes.banking-entity-name-1=Admin department"\
    -s  "attributes.roles-1-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-2=bva4"\
    -s  "attributes.bank-name-2=UK BANK-1"\
    -s  "attributes.banking-entity-name-2=Admin department"\
    -s  "attributes.roles-2-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-3=bva4"\
    -s  "attributes.bank-name-3=AU BANK-1"\
    -s  "attributes.banking-entity-name-3=Admin department"\
    -s  "attributes.roles-3-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-4=bva4"\
    -s  "attributes.bank-name-4=XCT BANK-2"\
    -s  "attributes.banking-entity-name-4=Admin department"\
    -s  "attributes.roles-4-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-5=bva4"\
    -s  "attributes.bank-name-5=XCT BANK-1"\
    -s  "attributes.banking-entity-name-5=Admin department"\
    -s  "attributes.roles-5-role-name-1=Group System Administrator"
kcadm.sh set-password -r xctsso --username bva4 --new-password password --temporary=false


echo "creating bva5 user"
# Create user
kcadm.sh create users -r xctsso -s  username=bva5 -s  enabled=true\
    -s  "attributes.user-name-1=bva5"\
    -s  "attributes.bank-groud-id=OPFBankgroup"\
    -s  "attributes.bank-name-1=UK BANK-2"\
    -s  "attributes.banking-entity-name-1=Admin department"\
    -s  "attributes.roles-1-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-2=bva5"\
    -s  "attributes.bank-name-2=UK BANK-1"\
    -s  "attributes.banking-entity-name-2=Admin department"\
    -s  "attributes.roles-2-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-3=bva5"\
    -s  "attributes.bank-name-3=AU BANK-1"\
    -s  "attributes.banking-entity-name-3=Admin department"\
    -s  "attributes.roles-3-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-4=bva5"\
    -s  "attributes.bank-name-4=XCT BANK-2"\
    -s  "attributes.banking-entity-name-4=Admin department"\
    -s  "attributes.roles-4-role-name-1=Group System Administrator"\
    -s  "attributes.user-name-5=bva5"\
    -s  "attributes.bank-name-5=XCT BANK-1"\
    -s  "attributes.banking-entity-name-5=Admin department"\
    -s  "attributes.roles-5-role-name-1=Group System Administrator"
kcadm.sh set-password -r xctsso --username bva5 --new-password password --temporary=false

echo "DONE"
