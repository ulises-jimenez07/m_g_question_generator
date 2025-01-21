BUCKET_NAME="unique-bucket-name"
REGION=us-central1

gcloud storage buckets create gs://$BUCKET_NAME --location=$REGION
gcloud storage cp mg_questions_ds.pdf gs://$BUCKET_NAME/