# Cocktail Hour with Apache Airflow

## Introduction

Welcome to our Apache Airflow project! If you love data, automation, and a good drink, you're in the right place. This project leverages the power of Apache Airflow to orchestrate a fun workflow that fetches random drink recipes from The Cocktail DB API and displays them on a sleek, static website hosted on AWS S3. Every 30 minutes, a new drink recipe is up for grabs – perfect for your next happy hour!

## How It Works

The workflow is simple:
1. **Fetch Drink Data**: Every 30 minutes, Airflow executes a task that pulls a random drink recipe from The Cocktail DB.
2. **Publish to S3**: The recipe is formatted as an HTML file and uploaded to an S3 bucket.
3. **Static Website**: The S3 bucket is set up as a static website, making the drink recipes accessible to anyone on the internet.

## Getting Started

### Prerequisites
- An Apache Airflow setup
- AWS account with permissions to create and manage S3 buckets
- Basic knowledge of Python for understanding the DAG script

### Setting Up Your Environment

#### Configure Airflow

Make sure Apache Airflow is up and running in your environment. You'll place the DAG file from this repository into your Airflow DAGs folder.

#### Set Up AWS S3

1. Create an S3 bucket if you haven't already.
2. Enable static website hosting on the bucket.
3. Add the following policy to your bucket to allow public access:

   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": "*",
         "Action": "s3:GetObject",
         "Resource": "arn:aws:s3:::your-bucket-name/*"
       }
     ]
   }
