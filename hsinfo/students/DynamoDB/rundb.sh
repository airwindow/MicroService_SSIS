#!/bin/bash

LIBPATH="./DynamoDBLocal_lib"
DBPORT=8888

java -Djava.library.path=$LIBPATH -jar DynamoDBLocal.jar -sharedDb -port $DBPORT
