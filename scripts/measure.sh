#!/usr/bin/env bash
# Usage: ./scripts/measure.sh   -> prints the numbers needed for the cost table
echo "== Image sizes =="
docker images --format '{{.Repository}}:{{.Tag}}  {{.Size}}' | grep -E 'visitor-counter'
echo; echo "== Replicas =="
kubectl get deploy web -o custom-columns=NAME:.metadata.name,REPLICAS:.spec.replicas
echo; echo "== Requests / limits =="
kubectl get deploy web -o jsonpath='{.spec.template.spec.containers[0].resources}'; echo
echo; echo "== Actual usage (needs metrics-server) =="
kubectl top pods
