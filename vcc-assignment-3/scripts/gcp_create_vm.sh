#!/bin/bash

VM_NAME="auto-scale-vm-$(date +%s)"

echo "[INFO] Creating VM: $VM_NAME"

gcloud compute instances create $VM_NAME \
    --zone=us-central1-a \
    --machine-type=e2-medium \
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --tags=http-server

if [ $? -eq 0 ]; then
    echo "[SUCCESS] VM $VM_NAME created"
else
    echo "[ERROR] Failed to create VM"
fi