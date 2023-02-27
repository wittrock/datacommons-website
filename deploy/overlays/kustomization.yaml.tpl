# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization

nameSuffix:
namespace: website

resources:
  - ../../base

generatorOptions:
 disableNameSuffixHash: true

configMapGenerator:
  - name: website-configmap
    behavior: merge
    literals:
      - flaskEnv=
      - secretProject=
      - enableModel=
  - name: mixer-configmap
    behavior: create
    literals:
      - mixerProject=
      - serviceName=

patchesStrategicMerge:
  - |-
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: website-app
    spec:
      replicas:
