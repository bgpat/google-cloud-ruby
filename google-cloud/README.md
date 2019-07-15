# google-cloud

The [google-cloud](https://github.com/googleapis/google-cloud-ruby/tree/master/google-cloud)
gem is a convenience package that lazily loads the vast majority of the
[google-cloud-*](https://github.com/googleapis/google-cloud-ruby) gems.
Because there are now so many google-cloud-* gems, instead of using this gem in
your production application, we encourage you to directly require only the
individual google-cloud-* gems that you need.

- [google-cloud API documentation](https://googleapis.dev/ruby/docs/google-cloud/latest)
- [google-cloud on RubyGems](https://rubygems.org/gems/google-cloud)

## List of dependencies

This gem depends on and lazily loads the following google-cloud-* gems:

- [google-cloud-asset](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-asset)
- [google-cloud-bigquery](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-bigquery)
- [google-cloud-bigquery-data_transfer](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-bigquery-data_transfer)
- [google-cloud-bigtable](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-bigtable)
- [google-cloud-container](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-container)
- [google-cloud-dataproc](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-dataproc)
- [google-cloud-datastore](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-datastore)
- [google-cloud-dialogflow](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-dialogflow)
- [google-cloud-dlp](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-dlp)
- [google-cloud-dns](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-dns)
- [google-cloud-error_reporting](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-error_reporting)
- [google-cloud-firestore](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-firestore)
- [google-cloud-kms](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-kms)
- [google-cloud-language](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-language)
- [google-cloud-logging](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-logging)
- [google-cloud-monitoring](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-monitoring)
- [google-cloud-os_login](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-os_login)
- [google-cloud-pubsub](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-pubsub)
- [google-cloud-redis](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-redis)
- [google-cloud-resource_manager](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-resource_manager)
- [google-cloud-scheduler](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-scheduler)
- [google-cloud-spanner](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-spanner)
- [google-cloud-speech](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-speech)
- [google-cloud-storage](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-storage)
- [google-cloud-tasks](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-tasks)
- [google-cloud-text_to_speech](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-text_to_speech)
- [google-cloud-trace](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-trace)
- [google-cloud-translate](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-translate)
- [google-cloud-video_intelligence](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-video_intelligence)
- [google-cloud-vision](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud-vision)

## Quick Start

```sh
$ gem install google-cloud
```

## Authentication

Instructions and configuration options are covered in the [Authentication
Guide](./AUTHENTICATION.md).

## Example

As shown in the example below, the google-cloud gem lazily loads its
google-cloud-* dependencies only as needed.

```ruby
require "google-cloud"

gcloud = Google::Cloud.new

Google::Cloud::Bigquery #=> NameError: uninitialized constant Google::Cloud::Bigquery

bigquery = gcloud.bigquery

Google::Cloud::Bigquery #=> Google::Cloud::Bigquery
Google::Cloud::Logging #=> NameError: uninitialized constant Google::Cloud::Logging

dataset = bigquery.dataset "my-dataset"
table = dataset.table "my-table"
table.data.each do |row|
  puts row
end
```

## Supported Ruby Versions

This library is supported on Ruby 2.3+.

Google provides official support for Ruby versions that are actively supported
by Ruby Core—that is, Ruby versions that are either in normal maintenance or in
security maintenance, and not end of life. Currently, this means Ruby 2.3 and
later. Older versions of Ruby _may_ still work, but are unsupported and not
recommended. See https://www.ruby-lang.org/en/downloads/branches/ for details
about the Ruby support schedule.

## Versioning

This library follows [Semantic Versioning](http://semver.org/).

It is currently in major version zero (0.y.z), which means that anything may
change at any time and the public API should not be considered stable.

## Contributing

Contributions to this library are always welcome and highly encouraged.

See the [Contributing
Guide](./CONTRIBUTING.md)
for more information on how to get started.

Please note that this project is released with a Contributor Code of Conduct. By
participating in this project you agree to abide by its terms. See [Code of
Conduct](./CODE_OF_CONDUCT.md)
for more information.

## License

This library is licensed under Apache 2.0. Full license text is available in
[LICENSE](https://googleapis.github.io/google-cloud-ruby/docs/google-cloud/latest/file.LICENSE).

## Support

Please [report bugs at the project on
Github](https://github.com/googleapis/google-cloud-ruby/issues). Don't
hesitate to [ask
questions](http://stackoverflow.com/questions/tagged/google-cloud-platform+ruby)
about the client or APIs on [StackOverflow](http://stackoverflow.com).
