# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import synthtool.languages.ruby as ruby
import logging
import os
import re

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()

v1_library = gapic.ruby_library(
    'containeranalysis', 'v1', artman_output_name='google-cloud-ruby/google-cloud-containeranalysis',
    config_path='/google/devtools/containeranalysis/artman_containeranalysis_v1.yaml'
)

s.copy(v1_library / 'lib')
s.copy(v1_library / 'test')
s.copy(v1_library / 'LICENSE')
s.copy(v1_library / '.gitignore')
s.copy(v1_library / '.yardopts')
s.copy(v1_library / 'google-cloud-container_analysis.gemspec', merge=ruby.merge_gemspec)

# Copy common templates
templates = gcp.CommonTemplates().ruby_library()
s.copy(templates)

# Hack grpc service class name and location
s.replace(
    'lib/google/devtools/containeranalysis/v1/containeranalysis_services_pb.rb',
    '  module ContainerAnalysis\n',
    '  module ContainerAnalysisService\n'
)
s.replace(
    [
        'lib/google/cloud/container_analysis/v1/container_analysis_client.rb',
        'test/google/cloud/container_analysis/v1/container_analysis_client_test.rb'
    ],
    'Google::Devtools::Containeranalysis::V1::ContainerAnalysis::',
    'Google::Cloud::ContainerAnalysis::V1::ContainerAnalysisService::'
)

# Support for service_address
s.replace(
    [
        'lib/google/cloud/container_analysis.rb',
        'lib/google/cloud/container_analysis/v*.rb',
        'lib/google/cloud/container_analysis/v*/*_client.rb'
    ],
    '\n(\\s+)#(\\s+)@param exception_transformer',
    '\n\\1#\\2@param service_address [String]\n' +
        '\\1#\\2  Override for the service hostname, or `nil` to leave as the default.\n' +
        '\\1#\\2@param service_port [Integer]\n' +
        '\\1#\\2  Override for the service port, or `nil` to leave as the default.\n' +
        '\\1#\\2@param exception_transformer'
)
s.replace(
    [
        'lib/google/cloud/container_analysis/v*.rb',
        'lib/google/cloud/container_analysis/v*/*_client.rb'
    ],
    '\n(\\s+)metadata: nil,\n\\s+exception_transformer: nil,\n',
    '\n\\1metadata: nil,\n\\1service_address: nil,\n\\1service_port: nil,\n\\1exception_transformer: nil,\n'
)
s.replace(
    [
        'lib/google/cloud/container_analysis/v*.rb',
        'lib/google/cloud/container_analysis/v*/*_client.rb'
    ],
    ',\n(\\s+)lib_name: lib_name,\n\\s+lib_version: lib_version',
    ',\n\\1lib_name: lib_name,\n\\1service_address: service_address,\n\\1service_port: service_port,\n\\1lib_version: lib_version'
)
s.replace(
    'lib/google/cloud/container_analysis/v*/*_client.rb',
    'service_path = self\\.class::SERVICE_ADDRESS',
    'service_path = service_address || self.class::SERVICE_ADDRESS'
)
s.replace(
    'lib/google/cloud/container_analysis/v*/*_client.rb',
    'port = self\\.class::DEFAULT_SERVICE_PORT',
    'port = service_port || self.class::DEFAULT_SERVICE_PORT'
)

# Container analysis should depend on grafeas-client for now
s.replace(
    'google-cloud-container_analysis.gemspec',
    '\n\n  gem.add_dependency "google-gax", "~> 1\\.[\\d\\.]+"',
    '\n\n  gem.add_dependency "grafeas-client", "~> 0.1"\n  gem.add_dependency "google-gax", "~> 1.7"',
)
s.replace(
    'lib/google/cloud/container_analysis.rb',
    '\n\nrequire "google/gax"\n',
    '\n\nrequire "grafeas"\nrequire "google/gax"\n'
)

# Expose the grafeas client as an attribute of the container_analysis client
s.replace(
    'lib/google/cloud/container_analysis/v*/*_client.rb',
    '\n\n(\\s+)(credentials \\|\\|= \\S+)\n',
    '\n\n\\1\\2\n\n\\1@grafeas_client = ::Grafeas.new(\n\\1  credentials: credentials, scopes: scopes, client_config: client_config,\n\\1  timeout: timeout, lib_name: lib_name, lib_version: lib_version,\n\\1  service_address: service_address, service_port: service_port, metadata: metadata)\n'
)
s.replace(
    'lib/google/cloud/container_analysis/v*/*_client.rb',
    '\n(\\s+)attr_reader :container_analysis_stub\n',
    '\n\\1attr_reader :container_analysis_stub\n\n\\1# @return [Grafeas::V1::GrafeasClient] a client for the Grafeas service\n\\1attr_reader :grafeas_client\n'
)

# Credentials env vars
s.replace(
    'lib/**/credentials.rb',
    'CONTAINERANALYSIS_',
    'CONTAINER_ANALYSIS_'
)

# https://github.com/googleapis/gapic-generator/issues/2196
s.replace(
    [
      'README.md',
      'lib/google/cloud/container_analysis.rb',
      'lib/google/cloud/container_analysis/v1.rb'
    ],
    '\\[Product Documentation\\]: https://cloud\\.google\\.com/containeranalysis\n',
    '[Product Documentation]: https://cloud.google.com/container-registry/docs/container-analysis\n')

# https://github.com/googleapis/gapic-generator/issues/2242
def escape_braces(match):
    expr = re.compile('^([^`]*(`[^`]*`[^`]*)*)([^`#\\$\\\\])\\{([\\w,]+)\\}')
    content = match.group(0)
    while True:
        content, count = expr.subn('\\1\\3\\\\\\\\{\\4}', content)
        if count == 0:
            return content
s.replace(
    'lib/google/cloud/container_analysis/v1/**/*.rb',
    '\n(\\s+)#[^\n]*[^\n#\\$\\\\]\\{[\\w,]+\\}',
    escape_braces)

# https://github.com/googleapis/gapic-generator/issues/2243
s.replace(
    'lib/google/cloud/container_analysis/*/*_client.rb',
    '(\n\\s+class \\w+Client\n)(\\s+)(attr_reader :\\w+_stub)',
    '\\1\\2# @private\n\\2\\3')

# https://github.com/googleapis/gapic-generator/issues/2279
s.replace(
    'lib/google/**/*.rb',
    '\\A(((#[^\n]*)?\n)*# (Copyright \\d+|Generated by the protocol buffer compiler)[^\n]+\n(#[^\n]*\n)*\n)([^\n])',
    '\\1\n\\6')

# https://github.com/googleapis/gapic-generator/issues/2323
s.replace(
    [
        'lib/**/*.rb',
        'README.md'
    ],
    'https://github\\.com/GoogleCloudPlatform/google-cloud-ruby',
    'https://github.com/googleapis/google-cloud-ruby'
)
s.replace(
    [
        'lib/**/*.rb',
        'README.md'
    ],
    'https://googlecloudplatform\\.github\\.io/google-cloud-ruby',
    'https://googleapis.github.io/google-cloud-ruby'
)

# https://github.com/googleapis/gapic-generator/issues/2393
s.replace(
    'google-cloud-container_analysis.gemspec',
    'gem.add_development_dependency "rubocop".*$',
    'gem.add_development_dependency "rubocop", "~> 0.64.0"'
)

s.replace(
    'google-cloud-container_analysis.gemspec',
    '"README.md", "LICENSE"',
    '"README.md", "AUTHENTICATION.md", "LICENSE"'
)
s.replace(
    '.yardopts',
    'README.md\n',
    'README.md\nAUTHENTICATION.md\nLICENSE\n'
)

# https://github.com/googleapis/google-cloud-ruby/issues/3058
s.replace(
    'google-cloud-container_analysis.gemspec',
    '\nGem::Specification.new do',
    'require File.expand_path("../lib/google/cloud/container_analysis/version", __FILE__)\n\nGem::Specification.new do'
)
s.replace(
    'google-cloud-container_analysis.gemspec',
    '(gem.version\s+=\s+).\d+.\d+.\d.*$',
    '\\1Google::Cloud::ContainerAnalysis::VERSION'
)
s.replace(
    'lib/google/cloud/container_analysis/v1/*_client.rb',
    '(require \".*credentials\"\n)\n',
    '\\1require "google/cloud/container_analysis/version"\n\n'
)
s.replace(
    'lib/google/cloud/container_analysis/v1/*_client.rb',
    'Gem.loaded_specs\[.*\]\.version\.version',
    'Google::Cloud::ContainerAnalysis::VERSION'
)

# Fix links for devsite migration
s.replace(
    'lib/**/*.rb',
    'https://googleapis.github.io/google-cloud-ruby/#/docs/google-cloud-logging/latest/google/cloud/logging/logger',
    'https://googleapis.dev/ruby/google-cloud-logging/latest'
)
s.replace(
    'lib/**/*.rb',
    'https://googleapis.github.io/google-cloud-ruby/#/docs/.*/authentication',
    'https://googleapis.dev/ruby/google-cloud-container_analysis/latest/file.AUTHENTICATION.html'
)
