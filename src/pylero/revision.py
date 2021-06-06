# -*- coding: utf8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pylero.base_polarion import BasePolarion
from pylero.subterra_uri import ArrayOfSubterraURI
from pylero.subterra_uri import SubterraURI


class Revision(BasePolarion):
    """Object to handle the Polarion WSDL tns4:Revision class

    Attributes:
        author (string)
        created (dateTime)
        internal_commit (boolean)
        linked_work_item_uris (ArrayOfSubterraURI)
        message (string)
        name (string)
        repository_name (string)
"""
    _cls_suds_map = {"author": "author",
                     "created": "created",
                     "internal_commit": "internalCommit",
                     "linked_work_item_uris":
                     {"field_name": "linkedWorkItemURIs",
                      "is_array": True,
                      "cls": SubterraURI,
                      "arr_cls": ArrayOfSubterraURI,
                      "inner_field_name": "SubterraURI"},
                     "message": "message",
                     "name": "name",
                     "repository_name": "repositoryName",
                     "uri": "_uri",
                     "_unresolved": "_unresolved"}
    _obj_client = "builder_client"
    _obj_struct = "tns4:Revision"

    @classmethod
    def query(cls, query, sort="name", fields=["name"], query_uris=False):
        """Searches revisions

        Args:
            query: query, Lucene
            sort: Lucene sort string, default - name
            fields: list of field names to fill in the returned
                    Revision (can be null). For nested structures in
                    the lists you can use following syntax to include only
                    subset of fields: myList.LIST.key
                    (e.g. linkedWorkItems.LIST.role).
                    For custom fields you can specify which fields you want to
                    be filled using following syntax:
                    customFields.CUSTOM_FIELD_ID (e.g. customFields.risk).
                    Default - list containing "name"
            query_uris: if True, returns a list of URIs instead of Revision
                        objects. default - False

        Returns:
            list of Revisions

        References:
            Tracker.queryRevisions
        """
        if query_uris:
            return cls.session.tracker_client.service.queryRevisionUris(
                query, sort, False)
        else:
            revs = cls.session.tracker_client.service.queryRevisions(
                query, sort, fields)
            lst_rev = [Revision(suds_object=rev) for rev in revs]
            return lst_rev


class ArrayOfRevision(BasePolarion):
    _obj_client = "builder_client"
    _obj_struct = "tns4:ArrayOfRevision"
