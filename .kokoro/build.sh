#!/bin/bash

# This file runs tests for merges, PRs, and nightlies.
# There are a few rules for what tests are run:
#  * PRs run all non-acceptance tests for every library.
#  * Merges run all non-acceptance tests for every library, and acceptance tests for all altered libraries.
#  * Nightlies run all acceptance tests for every library.

set -eo pipefail

# Debug: show build environment
env | grep KOKORO

cd $REPO_DIR

# Print out Ruby version
ruby --version

# Temporary workaround for a known bundler+docker issue:
# https://github.com/bundler/bundler/issues/6154
export BUNDLE_GEMFILE=

versions=($RUBY_VERSIONS)

# Capture failures
EXIT_STATUS=0 # everything passed
function set_failed_status {
    EXIT_STATUS=1
}

if [ "$JOB_TYPE" = "nightly" ]; then
    for version in "${versions[@]}"; do
        rbenv global "$version"
        (bundle update && bundle exec rake kokoro:nightly) || set_failed_status
    done
elif [ "$JOB_TYPE" = "continuous" ]; then
    git fetch --depth=10000
    for version in "${versions[@]}"; do
        rbenv global "$version"
        (bundle update && bundle exec rake kokoro:continuous) || set_failed_status
    done
elif [ "$JOB_TYPE" = "release" ]; then
    export DOCS_CREDENTIALS=${KOKORO_KEYSTORE_DIR}/73713_docuploader_service_account
    git fetch --depth=10000
    python3 -m pip install git+https://github.com/googleapis/releasetool
    python3 -m releasetool publish-reporter-script > /tmp/publisher-script; source /tmp/publisher-script
    (bundle update && bundle exec rake kokoro:release) || set_failed_status
else
    for version in "${versions[@]}"; do
        rbenv global "$version"
        (bundle update && bundle exec rake kokoro:presubmit) || set_failed_status
    done
fi

exit $EXIT_STATUS
