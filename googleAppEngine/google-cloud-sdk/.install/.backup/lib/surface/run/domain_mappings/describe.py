# -*- coding: utf-8 -*- #
# Copyright 2019 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Surface for creating domain mappings."""

from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

from googlecloudsdk.calliope import base
from googlecloudsdk.command_lib.run import connection_context
from googlecloudsdk.command_lib.run import flags
from googlecloudsdk.command_lib.run import resource_args
from googlecloudsdk.command_lib.run import serverless_operations
from googlecloudsdk.command_lib.util.concepts import concept_parsers
from googlecloudsdk.command_lib.util.concepts import presentation_specs


@base.ReleaseTracks(base.ReleaseTrack.BETA)
class Describe(base.Command):
  """Describe domain mappings."""

  detailed_help = {
      'DESCRIPTION':
          '{description}',
      'EXAMPLES':
          """\
          To describe a Cloud Run domain mapping, run:

              $ {command} --domain www.example.com
          """,
  }

  @staticmethod
  def CommonArgs(parser):
    # Flags specific to managed CR
    managed_group = flags.GetManagedArgGroup(parser)
    flags.AddRegionArg(managed_group)
    # Flags specific to CRoGKE
    gke_group = flags.GetGkeArgGroup(parser)
    concept_parsers.ConceptParser([resource_args.CLUSTER_PRESENTATION
                                  ]).AddToParser(gke_group)
    # Flags specific to connecting to a Kubernetes cluster (kubeconfig)
    kubernetes_group = flags.GetKubernetesArgGroup(parser)
    flags.AddKubeconfigFlags(kubernetes_group)
    # Flags not specific to any platform
    domain_mapping_presentation = presentation_specs.ResourcePresentationSpec(
        '--domain',
        resource_args.GetDomainMappingResourceSpec(),
        'Domain name is the ID of DomainMapping resource.',
        required=True,
        prefixes=False)
    concept_parsers.ConceptParser([
        domain_mapping_presentation]).AddToParser(parser)
    flags.AddPlatformArg(parser)
    parser.display_info.AddFormat('yaml')

  @staticmethod
  def Args(parser):
    Describe.CommonArgs(parser)

  def Run(self, args):
    """Describe a domain mapping."""
    conn_context = connection_context.GetConnectionContext(
        args, self.ReleaseTrack())
    domain_mapping_ref = args.CONCEPTS.domain.Parse()
    with serverless_operations.Connect(conn_context) as client:
      domain_mapping = client.GetDomainMapping(domain_mapping_ref)
      if not domain_mapping:
        raise flags.ArgumentError(
            'Cannot find domain mapping for domain name [{}]'.format(
                domain_mapping_ref.domainmappingsId))
      return domain_mapping


@base.ReleaseTracks(base.ReleaseTrack.ALPHA)
class AlphaDescribe(Describe):
  """Describe domain mappings."""

  @staticmethod
  def Args(parser):
    Describe.CommonArgs(parser)

AlphaDescribe.__doc__ = Describe.__doc__
