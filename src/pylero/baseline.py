# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.project import Project
from pylero.user import User


class Baseline(BasePolarion):
    """Object to handle the Polarion WSDL tns3:Baseline class

    Attributes:
        author (User)
        base_revision (string)
        description (string)
        baseline_id (string)
        name (string)
        project (Project)"""

    _cls_suds_map = {
        "author": {"field_name": "author", "cls": User},
        "base_revision": "baseRevision",
        "description": "description",
        "baseline_id": "id",
        "name": "name",
        "project": {"field_name": "project", "cls": Project},
        "uri": "_uri",
        "_unresolved": "_unresolved",
    }
    _obj_client = "tracker_client"
    _obj_struct = "tns3:Baseline"

    @classmethod
    def create(cls, project_id, name, description, revision):
        """class method create Creates a Baseline from head or particular
        revision.

        Args:
            project_id
            name: baseline name (not None)
            description: baseline description (can be None)
            revision: revision or null value for head revision

        Returns:
            Baseline object

        References:
            Tracker.createBaseline
        """
        suds_object = cls.session.tracker_client.service.createBaseline(
            project_id, name, description, revision
        )
        return cls(suds_object=suds_object)

    @classmethod
    def query(cls, query, sort="baseline_id"):
        """Queries for baselines.

        Args:
            query: the lucene query to be used.
            sort: the field to be used for sorting.

        Returns:
            list of Baselines

        References:
            Tracker.queryBaselines
        """
        baselines = []
        for suds_base in cls.session.tracker_client.service.queryBaselines(query, sort):
            baselines.append(Baseline(suds_object=suds_base))
        return baselines
