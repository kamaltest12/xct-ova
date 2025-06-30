**OPF Hashicorp Chart**  
This chart is intended to ease the deployment of an Hashicorp vault and loading application secrets in it.

It has a dependency on the Hashicorp chart itself and adds the required service account, role binding and token for the vault to be able to serve the application credentials to K8s services.

In order to load credentials in it, you can set the "provisioning" entry in the values.yaml file you'll provide at installation time. 
The value should correspond to a script load the required credentials using vault CLI and creating the required vault roles and policy.
For example, the following command with load the username and password for the auth admin.  
```
vault kv put secret/opf-secrets auth.admin.password=password auth.admin.username=admin
```

In order to load keystores in the vault, you'll first need to mount them as files in the vault for the script to be able to access them. 
In order to do that, 
* deploy them in K8s secrets
* define a volume called "tls-secrets" in the "vault.server.volumes" entry point in your values.yaml file pointing to the secrets your just created.

```
vault:
    server:
        volumes:
          - name : tls-secrets
            secret:
              secretName: my-tls-secret
```
This will make the keystores defined in the tls-secrets in the /init/tls folder. 
Note that if you have multiple secrets to mount to the vault, you can used projected volumes. 
```
vault:
    server:
      volumes:
      - name: tls-secrets
        projected:
          sources:
          - secret:
              name: my-tls-secret
          - secret:
              name: another-tls-secret
```
* add one line in your provisioning script in order to load them in the vault. 
```
base64 /init/tls/my-keystore.jks | vault kv put secret/my-keystore my-keystore.jks=-
```

Finally, you'll need to create the required hashicorp vault policy and roles to grant access to your services to the secrets they need.
A vault policy defines as set of access to some secrets in the vault. 
```
  vault policy write my-policy - <<EOF
    path "secret/data/my-secrets" {
      capabilities = ["read"]
    }
    path "secret/data/my-keystore" {
      capabilities = ["read"]
    }
    EOF 
```

A vault roles links a kubernetes service account to a vault policy. 
For example, this role tells the vault to grant access to the secrets/credentials defined in my-policy to the service account called my-application-sa and defined in the namespace called app-namespace. 
```
vault write auth/kubernetes/role/my-application-role \
            bound_service_account_names=my-application-sa \
            bound_service_account_namespaces=app-namespace \
            policies=my-policy \
            ttl=24h 
```

Note that for this to work, you need to create a service account for you application container. 

Now that the credentials are available in the vault and that the vault is ready to serve them, let's see how to inject them into your container.
This is done by using pod annotations. 

To open Vault UI for dev setup

kubectl port-forward --request-timeout=60s service/dev-vault 8200:8200

with URL

http://localhost:8200/ui/vault/secrets/secret/list

loging ase -> Token/root

To be continued


 
 

