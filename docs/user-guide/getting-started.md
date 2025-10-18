# Quick start

## Python


## Using Piper


## Using AWS Polly

When using AWS Polly as your voice provider, you will need to provide AWS credentials to access your AWS account.

These are loaded in the typical way used by `aws-cli` and are not interacted with by OpenVoicePacks at all, they are loaded directly by the `boto3` library for AWS API calls.

```bash
# Load AWS credentials directly from environment variable
export AWS_ACCESS_KEY_ID=<ACCESS KEY ID>
export AWS_SECRET_ACCESS_KEY=<SECRET ACCESS KEY>

# Alternatively load an AWS_PROFILE with keys stored in ~/.aws/credentials
export AWS_PROFILE=<YOUR PROFILE>
```

!!! notice "AWS Polly pricing"
    Although AWS Polly is a billable service (outside of the generous free tier) it is reasonably cheap and one of the better options for a natural sounding voice. You can check out the [current AWS Polly pricing](https://aws.amazon.com/polly/pricing/) for more information.
