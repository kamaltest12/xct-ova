#!/bin/bash

cat <&0 > all.yaml

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

mv all.yaml ${SCRIPT_DIR}/all.yaml

export PATH="$(dirname $(find ${KUSTOMIZE_HOME} -type f -name kustomize -executable)):${PATH}"

kustomize build  ${SCRIPT_DIR} && rm ${SCRIPT_DIR}/all.yaml
