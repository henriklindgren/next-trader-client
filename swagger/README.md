# Swagger support
Nordnet nExt API is described by swagger 1.2 and as such swagger can be used to generate the client stub.

The current code is generated with the following command together with the configuration file in this directory:

```java -jar swagger-codegen-cli-2.2.2.jar generate -i https://api.test.nordnet.se/next/2/api-docs/swagger -l python -o next_trader -c swagger/config.json```

You can download swagger-codegen directly from the central Maven repos:
http://central.maven.org/maven2/io/swagger/swagger-codegen-cli/

