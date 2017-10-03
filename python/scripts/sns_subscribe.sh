#!/usr/bin/env bash

# Create a topic (if necessary) and then subscribe the user

DEFAULT_PREFIX="${ARTHUR_DEFAULT_PREFIX-$USER}"

set -e -u

# === Command line args ===

show_usage_and_exit() {
    echo "Usage: `basename $0` [<environment>] <email_address>"
    echo "The environment defaults to \"$DEFAULT_PREFIX\"."
    exit ${1-0}
}

while getopts ":h" opt; do
  case $opt in
    h)
      show_usage_and_exit
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
  esac
done

if [[ $# -eq 1 ]]; then
    PROJ_ENVIRONMENT="$DEFAULT_PREFIX"
    NOTIFICATION_ENDPOINT="$1"
elif [[ $# -eq 2 ]]; then
    PROJ_ENVIRONMENT="$1"
    NOTIFICATION_ENDPOINT="$2"
else
    show_usage_and_exit 1
fi

set -x

# === Configuration ===

STATUS_NAME="redshift-etl-status_$PROJ_ENVIRONMENT"
PAGE_NAME="redshift-etl-page_$PROJ_ENVIRONMENT"
VALIDATION_NAME="redshift-etl-validation_$PROJ_ENVIRONMENT"

# ===  Create topic and subscription ===

TOPIC_ARN_FILE="/tmp/topic_arn_${USER}$$.json"

for TOPIC in "$STATUS_NAME" "$PAGE_NAME" "$VALIDATION_NAME"; do
    aws sns create-topic --name "$TOPIC" | tee "$TOPIC_ARN_FILE"
    TOPIC_ARN=`jq --raw-output < "$TOPIC_ARN_FILE" '.TopicArn'`
    if [[ -z "$TOPIC_ARN" ]]; then
        set +x
        echo "Failed to find topic arn in output. Check your settings, including VPN etc."
        exit 1
    fi
    aws sns subscribe --topic-arn "$TOPIC_ARN" --protocol email --notification-endpoint "$NOTIFICATION_ENDPOINT"
done

aws sns list-topics | jq --raw-output '.Topics[].TopicArn' | grep 'redshift-etl-[^_]*_tom'